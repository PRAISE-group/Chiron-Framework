""" Sparse Simple Constant Propagation for ChironLang"""
from collections import deque, defaultdict
from typing import Dict, List, Set
from ChironAST.ChironAST import (
    AssignmentCommand, PhiCommand, Var, BinArithOp, UnaryArithOp,
    BinCondOp, NOT, Num, BoolTrue, BoolFalse, ConditionCommand, MoveCommand,
    GotoCommand
)
from cfg.ChironCFG import ChironCFG, BasicBlock
from ssa.latticeValue import LatticeValue
        
class SSCP:
    """Sparse Simple Constant Propagation driver class."""
    def __init__(self, cfg: ChironCFG):
        self.cfg = cfg
        self.lattice: Dict[str, LatticeValue] = {}
        self.def_use = defaultdict(list)  # var -> list of dependent instructions
        self.worklist = deque()

        self._build_def_use_chains()
        self._initialize_lattice()
        self.run()

    def _build_def_use_chains(self):
        """Populate def-use chains by scanning all instructions."""
        for bb in self.cfg.nodes():
            for instr, _ in bb.instrlist:
                if isinstance(instr, AssignmentCommand):
                    used_vars = self._get_used_vars(instr.rexpr)
                    for var in used_vars:
                        self.def_use[var].append(instr)
                    lhs_var = instr.lvar.varname
                    self.lattice.setdefault(lhs_var, LatticeValue.top())
                elif isinstance(instr, PhiCommand):
                    for operand in instr.operands:
                        if operand: 
                            self.def_use[operand].append(instr)
                    self.lattice.setdefault(instr.var, LatticeValue.top())
                elif isinstance(instr, (MoveCommand, ConditionCommand)):
                    used_vars = self._get_used_vars(instr.expr) if isinstance(instr, MoveCommand) else self._get_used_vars(instr.cond)
                    for var in used_vars:
                        self.def_use[var].append(instr)
                elif isinstance(instr, GotoCommand):
                    used_vars = self._get_used_vars(instr.xcor)
                    used_vars.update(self._get_used_vars(instr.ycor))
                    for var in used_vars:
                        self.def_use[var].append(instr)

    def _get_used_vars(self, expr) -> Set[str]:
        """Extract variables from an expression."""
        if isinstance(expr, Var):
            return {expr.varname}
        elif isinstance(expr, (BinArithOp, BinCondOp)):
            return self._get_used_vars(expr.lexpr) | self._get_used_vars(expr.rexpr)
        elif isinstance(expr, (UnaryArithOp, NOT)):
            return self._get_used_vars(expr.expr)
        elif isinstance(expr, (Num, BoolTrue, BoolFalse)):
            return set()
        else:
            return set()

    def _initialize_lattice(self):
        """Initialize lattice values and evaluate initial constants."""
        # Set all variables to TOP initially
        for var in self.lattice:
            self.lattice[var] = LatticeValue.top()

        # Evaluate each instruction to compute initial values
        for bb in self.cfg.nodes():
            for instr, _ in bb.instrlist:
                if isinstance(instr, AssignmentCommand):
                    self._evaluate_assignment(instr)
                elif isinstance(instr, PhiCommand):
                    self._evaluate_phi(instr)

    def _evaluate_assignment(self, instr: AssignmentCommand):
        """Evaluate AssignmentCommand and update lattice."""
        lhs_var = instr.lvar.varname
        rhs_val = self._evaluate_expr(instr.rexpr)
        self._update_lattice(lhs_var, rhs_val)

    def _evaluate_phi(self, instr: PhiCommand):
        """Evaluate PhiCommand by meeting all operands."""
        lhs_var = instr.var
        current = self.lattice[lhs_var]
        new_val = LatticeValue.top()
        for operand in instr.operands:
            if not operand:
                continue
            operand_val = self.lattice.get(operand, LatticeValue.bottom())
            new_val = self._meet(new_val, operand_val)
        self._update_lattice(lhs_var, new_val)

    def _evaluate_expr(self, expr) -> LatticeValue:
        """Evaluate an expression to a lattice value."""
        if isinstance(expr, Num):
            return LatticeValue.constant(expr.val)
        elif isinstance(expr, Var):
            return self.lattice.get(expr.varname, LatticeValue.bottom())
        elif isinstance(expr, BinArithOp):
            left = self._evaluate_expr(expr.lexpr)
            right = self._evaluate_expr(expr.rexpr)
            if left.is_constant() and right.is_constant():
                try:
                    op = expr.symbol
                    a, b = left.constant, right.constant
                    if op == '+':
                        val = a + b
                    elif op == '-':
                        val = a - b
                    elif op == '*':
                        val = a * b
                    elif op == '/':
                        val = a / b if b != 0 else LatticeValue.bottom()
                    else:
                        return LatticeValue.bottom()
                    return LatticeValue.constant(val)
                except:
                    return LatticeValue.bottom()
            elif left.is_bottom() or right.is_bottom():
                return LatticeValue.bottom()
            else:
                return LatticeValue.top()
        elif isinstance(expr, UnaryArithOp):
            val = self._evaluate_expr(expr.expr)
            if val.is_constant():
                return LatticeValue.constant(-val.constant) if expr.symbol == '-' else val
            else:
                return val
        elif isinstance(expr, BinCondOp):
            left = self._evaluate_expr(expr.lexpr)
            right = self._evaluate_expr(expr.rexpr)
            # Apply special meet rules for && and ||
            if expr.symbol == '&&':
                if left.is_constant() and left.constant is False:
                    return LatticeValue.constant(False)
                if right.is_constant() and right.constant is False:
                    return LatticeValue.constant(False)
            elif expr.symbol == '||':
                if left.is_constant() and left.constant is True:
                    return LatticeValue.constant(True)
                if right.is_constant() and right.constant is True:
                    return LatticeValue.constant(True)
            # General case
            if left.is_constant() and right.is_constant():
                op = expr.symbol
                a, b = left.constant, right.constant
                try:
                    if op == '<':
                        res = a < b
                    elif op == '>':
                        res = a > b
                    elif op == '==':
                        res = a == b
                    elif op == '!=':
                        res = a != b
                    elif op == '<=':
                        res = a <= b
                    elif op == '>=':
                        res = a >= b
                    else:
                        return LatticeValue.bottom()
                    return LatticeValue.constant(res)
                except:
                    return LatticeValue.bottom()
            elif left.is_bottom() or right.is_bottom():
                return LatticeValue.bottom()
            else:
                return LatticeValue.top()
        elif isinstance(expr, NOT):
            val = self._evaluate_expr(expr.expr)
            if val.is_constant():
                return LatticeValue.constant(not val.constant)
            else:
                return val
        else:
            return LatticeValue.top()

    def _meet(self, a: LatticeValue, b: LatticeValue) -> LatticeValue:
        """Compute the meet of two lattice values."""
        if a.is_top():
            return b
        elif b.is_top():
            return a
        elif a.is_bottom() or b.is_bottom():
            return LatticeValue.bottom()
        elif a.is_constant() and b.is_constant():
            return a if a.constant == b.constant else LatticeValue.bottom()
        else:
            return LatticeValue.bottom()

    def _update_lattice(self, var: str, new_val: LatticeValue):
        """Update the lattice value and enqueue if changed."""
        current = self.lattice.get(var, LatticeValue.top())
        if new_val != current:
            self.lattice[var] = new_val
            if var not in self.worklist:
                self.worklist.append(var)

    def run(self):
        """Run the SSCP algorithm until worklist is empty."""
        while self.worklist:
            var = self.worklist.popleft()
            for instr in self.def_use.get(var, []):
                if isinstance(instr, AssignmentCommand):
                    self._evaluate_assignment(instr)
                elif isinstance(instr, PhiCommand):
                    self._evaluate_phi(instr)

    def get_constant(self, var: str):
        """Return the constant value if known, else None."""
        val = self.lattice.get(var, LatticeValue.bottom())
        return val.constant if val.is_constant() else None

    def get_results(self) -> Dict[str, LatticeValue]:
        """Return the computed lattice values for all variables."""
        print("\nLattice Values of All variables")
        for var in self.lattice.keys():
            print(var, self.lattice[var])
        return self.lattice
    
class SSCPOptimizer:
    """Replaces constant variables with the corresponding constants in the IR."""

    def __init__(self, cfg: ChironCFG, sscp: SSCP, ir, sscp_results:  Dict[str, LatticeValue]):
        self.cfg = cfg
        self.sscp = sscp
        self.ir = ir
        self.constants: Dict[str, LatticeValue] = sscp_results

    def optimize(self):
        """Replace variables with constants in the IR."""
        for i, (instr, offset) in enumerate(self.ir):
            optimized_instr = self._optimize_instruction(instr)
            self.ir[i] = (optimized_instr, offset)

    def _optimize_instruction(self, instr):
        """Replace constant variables by the corresponding constant in a single instruction."""
        if isinstance(instr, AssignmentCommand):
            return self._optimize_assignment(instr)
        elif isinstance(instr, PhiCommand):
            return self._optimize_phi(instr)
        elif isinstance(instr, (MoveCommand, ConditionCommand, GotoCommand)):
            return self._optimize_expr_instr(instr)
        return instr  # Other instructions remain unchanged

    def _optimize_assignment(self, instr: AssignmentCommand) -> AssignmentCommand:
        """Replace variables in AssignmentCommand with constants. """
        lhs_var = instr.lvar.varname
        optimized_rexpr = self._replace_vars_in_expr(instr.rexpr)

        # If LHS is a constant, replace RHS with the constant value
        if self.constants.get(lhs_var, LatticeValue.bottom()).is_constant():
            const_val = self.constants[lhs_var].constant
            return AssignmentCommand(instr.lvar, Num(const_val))
        else:
            return AssignmentCommand(instr.lvar, optimized_rexpr)

    def _optimize_phi(self, instr: PhiCommand):
        """Replace PhiCommand with AssignmentCommand if resolved to a constant."""
        lhs_var = instr.var
        if self.constants.get(lhs_var, LatticeValue.bottom()).is_constant():
            const_val = self.constants[lhs_var].constant
            return AssignmentCommand(Var(lhs_var), Num(const_val))
        else:
            return instr

    def _optimize_expr_instr(self, instr):
        """Replace variables in expressions."""
        if isinstance(instr, MoveCommand):
            optimized_expr = self._replace_vars_in_expr(instr.expr)
            return MoveCommand(instr.direction, optimized_expr)
        elif isinstance(instr, ConditionCommand):
            optimized_cond = self._replace_vars_in_expr(instr.cond)
            return ConditionCommand(optimized_cond)
        elif isinstance(instr, GotoCommand):
            optimized_xcor = self._replace_vars_in_expr(instr.xcor)
            optimized_ycor = self._replace_vars_in_expr(instr.ycor)
            return GotoCommand(optimized_xcor, optimized_ycor)
        return instr

    def _replace_vars_in_expr(self, expr):
        """Recursively replace variables in an expression with constants."""
        if isinstance(expr, Var):
            const_val = self.constants.get(expr.varname, LatticeValue.bottom())
            if const_val.is_constant():
                return Num(const_val.constant)
            else:
                return expr
        elif isinstance(expr, BinArithOp):
            new_lexpr = self._replace_vars_in_expr(expr.lexpr)
            new_rexpr = self._replace_vars_in_expr(expr.rexpr)
            return BinArithOp(new_lexpr, new_rexpr, expr.symbol)
        elif isinstance(expr, UnaryArithOp):
            new_expr = self._replace_vars_in_expr(expr.expr)
            return UnaryArithOp(new_expr, expr.symbol)
        elif isinstance(expr, BinCondOp):
            new_lexpr = self._replace_vars_in_expr(expr.lexpr)
            new_rexpr = self._replace_vars_in_expr(expr.rexpr)
            return BinCondOp(new_lexpr, new_rexpr, expr.symbol)
        elif isinstance(expr, NOT):
            new_expr = self._replace_vars_in_expr(expr.expr)
            return NOT(new_expr)
        return expr

def optimize_ir(cfg: ChironCFG, sscp: SSCP, ir, sscp_results:  Dict[str, LatticeValue]):
    """Interface to run optimization after sparse simple constant propagation."""
    optimizer = SSCPOptimizer(cfg, sscp, ir, sscp_results)
    optimizer.optimize()