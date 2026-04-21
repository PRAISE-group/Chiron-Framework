import sys
sys.path.insert(0, "../ChironCore/")

import ChironAST.ChironAST as AST
import cfg.cfgBuilder as cfgB

def vars_in_expr(expr):
    """Recursively extract variable names from an expression AST node."""
    if isinstance(expr, AST.Var):
        return {expr.varname}
    elif isinstance(expr, AST.BinArithOp) or isinstance(expr, AST.BinCondOp):
        return vars_in_expr(expr.lexpr) | vars_in_expr(expr.rexpr)
    elif isinstance(expr, AST.UnaryArithOp):
        return vars_in_expr(expr.expr)
    elif isinstance(expr, AST.NOT):
        return vars_in_expr(expr.expr)
    return set()


def vars_used_in(instr):
    """Return set of variable names USED (read) by an instruction."""
    if isinstance(instr, AST.AssignmentCommand):
        return vars_in_expr(instr.rexpr)
    elif isinstance(instr, AST.ConditionCommand):
        return vars_in_expr(instr.cond)
    elif isinstance(instr, AST.MoveCommand):
        return vars_in_expr(instr.expr)
    elif isinstance(instr, AST.GotoCommand):
        return vars_in_expr(instr.xcor) | vars_in_expr(instr.ycor)
    return set()


def var_defined_by(instr):
    """Return variable name defined by instruction, or None."""
    if isinstance(instr, AST.AssignmentCommand):
        return instr.lvar.varname
    return None


def get_block_instr(block):
    """Get the instruction from a single-statement basic block, or None."""
    if block.instrlist:
        return block.instrlist[0][0]
    return None


def get_block_ir_idx(block):
    """Get the original IR index from a single-statement basic block, or None."""
    if block.instrlist:
        return block.instrlist[0][1]
    return None


class SSAInfo:
    """Side-table SSA metadata over the existing CFG."""

    def __init__(self, cfg):
        self.cfg = cfg

        self.idom = {}
        self.dom_children = {}

        self.dom_frontier = {}

        self.phi_nodes = {}

        # Phi-def and instruction-def metadata are stored separately so that
        # a block with both a phi for x and an instruction defining x can
        # expose both versions unambiguously.
        self.phi_version_def = {}    # (block, var) -> ver from the phi at block
        self.instr_version_def = {}  # (block, var) -> ver from the instruction at block
        self.var_version_use = {}
        self.def_site = {}
        self.uses = {}

        self.all_vars = set()
        self.def_blocks = {}

        self.rpo = []
        self._start = None
        self._end = None

    def build(self):
        self._find_special_blocks()
        self._collect_var_info()
        self._compute_rpo()
        self._compute_dominators()
        self._compute_dom_frontiers()
        self._place_phi_functions()
        self._rename_variables()

    def _find_special_blocks(self):
        for block in self.cfg.nodes():
            if block.name == "START":
                self._start = block
            elif block.name == "END":
                self._end = block

    def _collect_var_info(self):
        for block in self.cfg.nodes():
            instr = get_block_instr(block)
            if instr is None:
                continue
            
            for var in vars_used_in(instr):
                self.all_vars.add(var)

            d = var_defined_by(instr)
            if d is not None:
                self.all_vars.add(d)
                if d not in self.def_blocks:
                    self.def_blocks[d] = set()
                self.def_blocks[d].add(block)

    def _compute_rpo(self):
        visited = set()
        post_order = []

        def dfs(block):
            visited.add(block)
            for succ in self.cfg.successors(block):
                if succ not in visited:
                    dfs(succ)
            post_order.append(block)

        dfs(self._start)
        self.rpo = list(reversed(post_order))

    def _compute_dominators(self):
        rpo_index = {b: i for i, b in enumerate(self.rpo)}
        all_blocks = set(self.rpo)

        dom = {}
        for b in self.rpo:
            dom[b] = set(all_blocks)
        dom[self._start] = {self._start}

        changed = True
        while changed:
            changed = False
            for b in self.rpo:
                if b == self._start:
                    continue
                preds = list(self.cfg.predecessors(b))
                if not preds:
                    continue
                new_dom = set.intersection(*(dom[p] for p in preds if p in dom))
                new_dom = new_dom | {b}
                if new_dom != dom[b]:
                    dom[b] = new_dom
                    changed = True

        self.idom = {}
        self.dom_children = {b: [] for b in self.rpo}

        for b in self.rpo:
            if b == self._start:
                continue

            strict = dom[b] - {b}
            if not strict:
                continue

            idom_b = None
            for d in strict:
            # d is the immediate dominator if no other strict dominator
            # is strictly below it.
                if all(o == d or d not in dom[o] for o in strict):
                    idom_b = d
                    break

            if idom_b is None:
                raise RuntimeError(f"Could not determine idom for block {b.name}")

            self.idom[b] = idom_b
            self.dom_children[idom_b].append(b)


    def _compute_dom_frontiers(self):
        self.dom_frontier = {b: set() for b in self.rpo}

        for b in self.rpo:
            preds = list(self.cfg.predecessors(b))
            if len(preds) < 2:
                continue
            for p in preds:
                runner = p
                while runner is not None and runner != self.idom.get(b):
                    self.dom_frontier[runner].add(b)
                    runner = self.idom.get(runner)

    def _place_phi_functions(self):
        self.phi_nodes = {b: {} for b in self.rpo}

        for var in self.all_vars:
            if var not in self.def_blocks:
                continue
            worklist = list(self.def_blocks[var])
            ever_on_worklist = set(worklist)
            has_phi = set()

            while worklist:
                d = worklist.pop()
                for b in self.dom_frontier.get(d, set()):
                    if b not in has_phi:
                        has_phi.add(b)
                        self.phi_nodes[b][var] = {}
                        if b not in ever_on_worklist:
                            ever_on_worklist.add(b)
                            worklist.append(b)

    def _rename_variables(self):
        version_counter = {var: 0 for var in self.all_vars}
        version_stack = {var: [] for var in self.all_vars}

        self.phi_version_def = {}
        self.instr_version_def = {}
        self.var_version_use = {}
        self.def_site = {}
        self.uses = {}

        def fresh_version(var):
            ver = version_counter[var]
            version_counter[var] += 1
            version_stack[var].append(ver)
            return ver

        def current_version(var):
            if version_stack[var]:
                return version_stack[var][-1]
            return -1

        def rename_block(block):
            pushed = {var: 0 for var in self.all_vars}

            # Phi-defs act at the top of the block and must be pushed before
            # the instruction's uses so the instruction sees the phi version.
            for var in self.phi_nodes.get(block, {}):
                ver = fresh_version(var)
                self.phi_version_def[(block, var)] = ver
                self.def_site[(var, ver)] = block
                pushed[var] += 1

            instr = get_block_instr(block)
            if instr is not None:
                for var in vars_used_in(instr):
                    ver = current_version(var)
                    self.var_version_use[(var, block)] = ver
                    key = (var, ver)
                    if key not in self.uses:
                        self.uses[key] = set()
                    self.uses[key].add(block)

                # Instruction-def gets a fresh version AFTER its uses and is
                # recorded separately from the phi-def, so a block that has
                # both a phi-def and an instruction-def for the same variable
                # keeps both versions accessible.
                d = var_defined_by(instr)
                if d is not None:
                    ver = fresh_version(d)
                    self.instr_version_def[(block, d)] = ver
                    self.def_site[(d, ver)] = block
                    pushed[d] += 1

            for succ in self.cfg.successors(block):
                for var in self.phi_nodes.get(succ, {}):
                    ver = current_version(var)
                    self.phi_nodes[succ][var][block] = ver
                    key = (var, ver)
                    if key not in self.uses:
                        self.uses[key] = set()
                    self.uses[key].add(succ)

            for child in self.dom_children.get(block, []):
                rename_block(child)

            for var in self.all_vars:
                for _ in range(pushed[var]):
                    version_stack[var].pop()

        rename_block(self._start)

    # -------------------------------------------------------------------
    # Accessors
    # -------------------------------------------------------------------

    def get_phi_def_version(self, block, var):
        return self.phi_version_def.get((block, var))

    def get_instr_def_version(self, block, var):
        return self.instr_version_def.get((block, var))

    def block_has_phi_def(self, block, var):
        return (block, var) in self.phi_version_def

    def dump(self):
        """Print SSA metadata for debugging."""
        print("\n===== SSA INFO =====")
        print(f"\nAll variables: {self.all_vars}")

        print("\nPhi functions:")
        for block in self.rpo:
            phis = self.phi_nodes.get(block, {})
            if phis:
                for var, preds in phis.items():
                    pred_str = ", ".join(
                        f"{p.name}:v{v}" for p, v in preds.items()
                    )
                    ver = self.phi_version_def.get((block, var), "?")
                    print(f"  [{block.name}] {var}_v{ver} = phi({pred_str})")

        print("\nPhi definitions:")
        for (block, var), ver in sorted(
            self.phi_version_def.items(), key=lambda x: (x[0][1], x[1])
        ):
            print(f"  {var}_v{ver} defined at [{block.name}] (phi)")

        print("\nInstruction definitions:")
        for (block, var), ver in sorted(
            self.instr_version_def.items(), key=lambda x: (x[0][1], x[1])
        ):
            instr = get_block_instr(block)
            print(f"  {var}_v{ver} defined at [{block.name}] ({instr})")

        print("\nUses:")
        for (var, block), ver in sorted(
            self.var_version_use.items(), key=lambda x: (x[0][0], x[1])
        ):
            print(f"  [{block.name}] uses {var}_v{ver}")
        print("====================\n")
