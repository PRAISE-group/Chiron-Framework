"""
Sparse Conditional Constant Propagation (SCCP) for Kachua IR.

Uses SSA metadata to propagate constants and determine reachable branches.
Two worklists: CFG edges (reachability) and SSA values (constant propagation).
"""

import sys
sys.path.insert(0, "../ChironCore/")

import ChironAST.ChironAST as AST
from ssa import vars_used_in, var_defined_by, get_block_instr


# ---------------------------------------------------------------------------
# Lattice
# ---------------------------------------------------------------------------

UNDEF = "UNDEF"       # Top: not yet known (optimistic)
OVERDEF = "OVERDEF"    # Bottom: not a single constant


class ConstVal:
    """Represents a known constant value."""
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return isinstance(other, ConstVal) and self.val == other.val

    def __hash__(self):
        return hash(("ConstVal", self.val))

    def __repr__(self):
        return f"Const({self.val})"


def meet(a, b):
    """Meet operation: UNDEF ⊓ x = x, OVERDEF ⊓ x = OVERDEF,
    Const(c1) ⊓ Const(c2) = Const(c1) if c1==c2 else OVERDEF."""
    if a == UNDEF:
        return b
    if b == UNDEF:
        return a
    if a == OVERDEF or b == OVERDEF:
        return OVERDEF
    if a == b:
        return a
    return OVERDEF


# ---------------------------------------------------------------------------
# SCCP Engine
# ---------------------------------------------------------------------------

class SCCP:
    def __init__(self, cfg, ssa_info):
        self.cfg = cfg
        self.ssa = ssa_info

        # Lattice values for each SSA definition: (var, version) -> lattice value
        self.cell = {}

        # Reachability tracking
        self.executable_edges = set()   # set of (pred_block, succ_block)
        self.executable_blocks = set()  # set of blocks

        # Worklists
        self._cfg_worklist = []   # edges: (pred, succ)
        self._ssa_worklist = []   # (var, version)

    def run(self):
        """Execute SCCP algorithm."""
        self._initialize()
        self._solve()

    # -------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------

    def _initialize(self):
        # All SSA definitions start at UNDEF
        for (var, ver), block in self.ssa.def_site.items():
            self.cell[(var, ver)] = UNDEF

        # Input parameters (version -1) are OVERDEF
        for (var, block), ver in self.ssa.var_version_use.items():
            if ver == -1 and (var, -1) not in self.cell:
                self.cell[(var, -1)] = OVERDEF

        # Seed: evaluate START block and mark its outgoing edges
        start = self.ssa._start
        self.executable_blocks.add(start)
        self._eval_block(start)

    # -------------------------------------------------------------------
    # Main solve loop
    # -------------------------------------------------------------------

    def _solve(self):
        while self._cfg_worklist or self._ssa_worklist:
            # Process CFG edges first
            while self._cfg_worklist:
                pred, succ = self._cfg_worklist.pop()
                if (pred, succ) in self.executable_edges:
                    continue
                self.executable_edges.add((pred, succ))

                first_visit = succ not in self.executable_blocks
                self.executable_blocks.add(succ)

                # Evaluate phi functions at succ
                self._eval_phis(succ)

                # If first time visiting, evaluate instruction
                if first_visit:
                    self._eval_block(succ)

            # Process SSA value changes
            while self._ssa_worklist:
                var, ver = self._ssa_worklist.pop()
                # Re-evaluate all blocks that use this (var, version)
                for use_block in self.ssa.uses.get((var, ver), set()):
                    if use_block in self.executable_blocks:
                        # Check if it's a phi use
                        if var in self.ssa.phi_nodes.get(use_block, {}):
                            self._eval_phis(use_block)
                        # Check if it's an instruction use
                        instr = get_block_instr(use_block)
                        if instr is not None:
                            used_vars = vars_used_in(instr)
                            if var in used_vars:
                                self._eval_block(use_block)

    # -------------------------------------------------------------------
    # Evaluate phi functions at a block
    # -------------------------------------------------------------------

    def _eval_phis(self, block):
        for var, preds in self.ssa.phi_nodes.get(block, {}).items():
            phi_ver = self.ssa.var_version_def.get((var, block))
            if phi_ver is None:
                continue
            old_val = self.cell.get((var, phi_ver), UNDEF)

            # Meet over all executable incoming edges
            new_val = UNDEF
            for phi_pred, pred_ver in preds.items():
                if (phi_pred, block) in self.executable_edges:
                    pred_val = self.cell.get((var, pred_ver), UNDEF)
                    new_val = meet(new_val, pred_val)

            if new_val != old_val:
                self.cell[(var, phi_ver)] = new_val
                self._ssa_worklist.append((var, phi_ver))

    # -------------------------------------------------------------------
    # Evaluate the instruction in a block
    # -------------------------------------------------------------------

    def _eval_block(self, block):
        instr = get_block_instr(block)
        if instr is None:
            # Empty block (START/END) — propagate flow
            for succ in self.cfg.successors(block):
                self._cfg_worklist.append((block, succ))
            return

        if isinstance(instr, AST.AssignmentCommand):
            var = instr.lvar.varname
            ver = self.ssa.var_version_def.get((var, block))
            if ver is None:
                # This def might be from a phi, not instruction.
                # Propagate flow.
                for succ in self.cfg.successors(block):
                    self._cfg_worklist.append((block, succ))
                return

            old_val = self.cell.get((var, ver), UNDEF)
            new_val = self._eval_expr(instr.rexpr, block)
            # Monotonic: can only go down in lattice
            merged = meet(old_val, new_val)
            if merged != old_val:
                self.cell[(var, ver)] = merged
                self._ssa_worklist.append((var, ver))

            # Propagate flow (assignments always fall through)
            for succ in self.cfg.successors(block):
                self._cfg_worklist.append((block, succ))

        elif isinstance(instr, AST.ConditionCommand):
            cond_val = self._eval_expr(instr.cond, block)

            for succ in self.cfg.successors(block):
                label = self.cfg.get_edge_label(block, succ)
                if isinstance(cond_val, ConstVal):
                    # Known branch direction
                    if cond_val.val == True and label == 'Cond_True':
                        self._cfg_worklist.append((block, succ))
                    elif cond_val.val == False and label == 'Cond_False':
                        self._cfg_worklist.append((block, succ))
                    elif cond_val.val == True and label == 'Cond_False':
                        pass  # dead edge
                    elif cond_val.val == False and label == 'Cond_True':
                        pass  # dead edge
                elif cond_val == OVERDEF:
                    # Both edges executable
                    self._cfg_worklist.append((block, succ))
                # If UNDEF, don't mark any edges (optimistic)

        else:
            # MoveCommand, PenCommand, GotoCommand, NoOpCommand, PauseCommand
            # Always propagate flow
            for succ in self.cfg.successors(block):
                self._cfg_worklist.append((block, succ))

    # -------------------------------------------------------------------
    # Evaluate an expression over the lattice
    # -------------------------------------------------------------------

    def _eval_expr(self, expr, block):
        if isinstance(expr, AST.Num):
            return ConstVal(expr.val)

        elif isinstance(expr, AST.Var):
            ver = self.ssa.var_version_use.get((expr.varname, block))
            if ver is None or ver == -1:
                return OVERDEF  # input parameter or undefined
            return self.cell.get((expr.varname, ver), UNDEF)

        elif isinstance(expr, AST.BoolTrue):
            return ConstVal(True)

        elif isinstance(expr, AST.BoolFalse):
            return ConstVal(False)

        elif isinstance(expr, AST.Sum):
            return self._eval_binop(expr, block, lambda a, b: a + b)

        elif isinstance(expr, AST.Diff):
            return self._eval_binop(expr, block, lambda a, b: a - b)

        elif isinstance(expr, AST.Mult):
            return self._eval_binop(expr, block, lambda a, b: a * b)

        elif isinstance(expr, AST.Div):
            l = self._eval_expr(expr.lexpr, block)
            r = self._eval_expr(expr.rexpr, block)
            if l == OVERDEF or r == OVERDEF:
                return OVERDEF
            if l == UNDEF or r == UNDEF:
                return UNDEF
            if r.val == 0:
                return OVERDEF  # division by zero
            return ConstVal(l.val // r.val)

        elif isinstance(expr, AST.UMinus):
            v = self._eval_expr(expr.expr, block)
            if v == OVERDEF:
                return OVERDEF
            if v == UNDEF:
                return UNDEF
            return ConstVal(-v.val)

        # Comparison operators
        elif isinstance(expr, AST.LT):
            return self._eval_cmp(expr, block, lambda a, b: a < b)
        elif isinstance(expr, AST.GT):
            return self._eval_cmp(expr, block, lambda a, b: a > b)
        elif isinstance(expr, AST.LTE):
            return self._eval_cmp(expr, block, lambda a, b: a <= b)
        elif isinstance(expr, AST.GTE):
            return self._eval_cmp(expr, block, lambda a, b: a >= b)
        elif isinstance(expr, AST.EQ):
            return self._eval_cmp(expr, block, lambda a, b: a == b)
        elif isinstance(expr, AST.NEQ):
            return self._eval_cmp(expr, block, lambda a, b: a != b)

        # Logical operators
        elif isinstance(expr, AST.AND):
            l = self._eval_expr(expr.lexpr, block)
            r = self._eval_expr(expr.rexpr, block)
            if l == OVERDEF or r == OVERDEF:
                return OVERDEF
            if l == UNDEF or r == UNDEF:
                return UNDEF
            return ConstVal(bool(l.val) and bool(r.val))

        elif isinstance(expr, AST.OR):
            l = self._eval_expr(expr.lexpr, block)
            r = self._eval_expr(expr.rexpr, block)
            if l == OVERDEF or r == OVERDEF:
                return OVERDEF
            if l == UNDEF or r == UNDEF:
                return UNDEF
            return ConstVal(bool(l.val) or bool(r.val))

        elif isinstance(expr, AST.NOT):
            v = self._eval_expr(expr.expr, block)
            if v == OVERDEF:
                return OVERDEF
            if v == UNDEF:
                return UNDEF
            return ConstVal(not bool(v.val))

        elif isinstance(expr, AST.PenStatus):
            return OVERDEF  # runtime-dependent

        return OVERDEF

    def _eval_binop(self, expr, block, op):
        l = self._eval_expr(expr.lexpr, block)
        r = self._eval_expr(expr.rexpr, block)
        if l == OVERDEF or r == OVERDEF:
            return OVERDEF
        if l == UNDEF or r == UNDEF:
            return UNDEF
        return ConstVal(op(l.val, r.val))

    def _eval_cmp(self, expr, block, op):
        l = self._eval_expr(expr.lexpr, block)
        r = self._eval_expr(expr.rexpr, block)
        if l == OVERDEF or r == OVERDEF:
            return OVERDEF
        if l == UNDEF or r == UNDEF:
            return UNDEF
        return ConstVal(op(l.val, r.val))

    # -------------------------------------------------------------------
    # Debug
    # -------------------------------------------------------------------

    def dump(self):
        """Print SCCP results for debugging."""
        print("\n===== SCCP RESULTS =====")
        print(f"\nExecutable blocks: {sorted(b.name for b in self.executable_blocks)}")

        print("\nLattice values:")
        for (var, ver), val in sorted(self.cell.items(), key=lambda x: (x[0][0], x[0][1])):
            print(f"  {var}_v{ver} = {val}")

        print("\nExecutable edges:")
        for pred, succ in sorted(self.executable_edges, key=lambda x: (x[0].name, x[1].name)):
            label = self.cfg.get_edge_label(pred, succ)
            print(f"  {pred.name} -> {succ.name} ({label})")
        print("========================\n")
