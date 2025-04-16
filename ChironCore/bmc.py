'''
This file is used to convert the SSA IR to SMT-LIB format.
'''
import z3
from ChironSSA import ChironSSA
from cfg import cfgBuilder

class BMC:
    def __init__(self, cfg, angle_conf):
        self.solver = z3.Solver()
        self.solver_without_cond = z3.Solver()
        self.angle_conditions = z3.BoolVal(True)
        self.assert_conditions = z3.BoolVal(True)
        self.assume_conditions = z3.BoolVal(True)
        self.cfg = cfg
        self.angle_conf = angle_conf

        self.bbConditions = {} # bbConditions[bb] = condition for bb
        for bb in self.cfg:
            self.bbConditions[bb] = None

        self.buildConditions()

        self.varConditions = {} # varConditions[var] = condition for var
        for bb in self.cfg.nodes():
            for stmt, _ in bb.instrlist:
                if isinstance(stmt, (ChironSSA.PhiCommand, ChironSSA.AssignmentCommand, ChironSSA.SinCommand, ChironSSA.CosCommand)):
                    self.varConditions[stmt.lvar.name] = self.bbConditions[bb] if self.bbConditions[bb] is not None else z3.BoolVal(True)

    def buildConditions(self):
        topological_order = list(self.cfg.get_topological_order())
        start = topological_order[0]
        start.set_condition(z3.BoolVal(True))
        topological_order.pop(0)
        for node in topological_order:
            for pred in self.cfg.predecessors(node):
                instr = pred.instrlist[-1][0]
                current_cond = node.get_condition()
                if isinstance(instr, ChironSSA.ConditionCommand) and type(instr.cond) == ChironSSA.Var:
                    cond = z3.Bool(instr.cond.name)
                    label = self.cfg.get_edge_label(pred, node)
                    if label == 'Cond_True':
                        node.set_condition(z3.Or(current_cond, z3.And(pred.get_condition(), cond)))
                    elif label == 'Cond_False':
                        node.set_condition(z3.Or(current_cond, z3.And(pred.get_condition(), z3.Not(cond))))
                else:
                    node.set_condition(z3.Or(pred.get_condition(), current_cond))
            
            t = z3.Tactic('ctx-simplify').apply(node.get_condition()).as_expr()
            node.set_condition(t)
            self.bbConditions[node] = node.get_condition()

    def convertSSAtoSMT(self):
        for bb in self.cfg.nodes():
            for stmt, _ in bb.instrlist:
                if isinstance(stmt, ChironSSA.PhiCommand):
                    lvar = z3.Real(stmt.lvar.name)
                    rvars = [z3.Real(rvar.name) for rvar in stmt.rvars]
                    
                    rhs_expr = rvars[0]
                    for i in range(1, len(stmt.rvars)):
                        rhs_expr = z3.If(self.varConditions[stmt.rvars[i].name], rvars[i], (rhs_expr))

                    if self.varConditions[stmt.lvar.name] not in (None, True, False):
                        self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == rhs_expr))
                    elif self.varConditions[stmt.lvar.name] is not False:
                        self.solver.add(lvar == rhs_expr)
                        
                elif isinstance(stmt, ChironSSA.AssignmentCommand):
                    lvar = None
                    rvar1 = ChironSSA.Unused()
                    rvar2 = ChironSSA.Unused()

                    if stmt.op in ["+", "-", "*", "/", "%"]:
                        lvar = z3.Real(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Real(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.Num):
                            rvar1 = z3.RealVal(stmt.rvar1.value)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Real(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.Num):
                            rvar2 = z3.RealVal(stmt.rvar2.value)
                    elif stmt.op in ["<", ">", "<=", ">=", "==", "!="]:
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Real(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.Num):
                            rvar1 = z3.RealVal(stmt.rvar1.value)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Real(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.Num):
                            rvar2 = z3.RealVal(stmt.rvar2.value)
                    elif stmt.op in ["and", "or"]:
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Bool(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.BoolTrue):
                            rvar1 = z3.BoolVal(True)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Bool(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.BoolFalse):
                            rvar2 = z3.BoolVal(False)
                    elif stmt.op == "not":
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Bool(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.BoolTrue):
                            rvar2 = z3.BoolVal(True)
                        elif isinstance(stmt.rvar2, ChironSSA.BoolFalse):
                            rvar2 = z3.BoolVal(False)
                    elif stmt.op == "":
                        continue
                    else:
                        raise Exception("Unknown SSA instruction")
    
                    if stmt.op == "+":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 + rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 + rvar2))
                    elif stmt.op == "-":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 - rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 - rvar2))
                    elif stmt.op == "*":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 * rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 * rvar2))
                    elif stmt.op == "/":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 / rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 / rvar2))
                    elif stmt.op == "%":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (z3.ToInt(rvar1) % z3.ToInt(rvar2))))
                            if stmt.lvar.name.startswith(":turtleThetaDeg$"):
                                condition = z3.BoolVal(False)
                                for (angle, _, _) in self.angle_conf:
                                    condition = z3.Or(condition, lvar == angle)
                                self.angle_conditions = z3.And(self.angle_conditions, z3.Implies(self.varConditions[stmt.lvar.name], condition))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (z3.ToInt(rvar1) % z3.ToInt(rvar2)))
                            if stmt.lvar.name.startswith(":turtleThetaDeg$"):
                                condition = z3.BoolVal(False)
                                for (angle, _, _) in self.angle_conf:
                                    condition = z3.Or(condition, lvar == angle)
                                self.angle_conditions = z3.And(self.angle_conditions, condition)

                    elif stmt.op == "<":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 < rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 < rvar2))
                    elif stmt.op == ">":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 > rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 > rvar2))
                    elif stmt.op == "<=":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 <= rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 <= rvar2))
                    elif stmt.op == ">=":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 >= rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 >= rvar2))
                    elif stmt.op == "==":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 == rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 == rvar2))
                    elif stmt.op == "!=":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 != rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 != rvar2))
                    elif stmt.op == "and":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == z3.And(rvar1, rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == z3.And(rvar1, rvar2))
                    elif stmt.op == "or":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == z3.Or(rvar1, rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == z3.Or(rvar1, rvar2))
                    elif stmt.op == "not":
                        if self.varConditions[stmt.lvar.name] not in (None, True, False):
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == z3.Not(rvar2)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == z3.Not(rvar2))
    
                elif isinstance(stmt, ChironSSA.AssertCommand):
                    cond = None
                    if isinstance(stmt.cond, ChironSSA.BoolTrue):
                        cond = z3.BoolVal(True)
                    elif isinstance(stmt.cond, ChironSSA.BoolFalse):
                        cond = z3.BoolVal(False)
                    elif isinstance(stmt.cond, ChironSSA.Var):
                        cond = z3.Bool(stmt.cond.name)
                    if self.varConditions[stmt.cond.name] not in (None, True, False):
                        self.assert_conditions = z3.And(self.assert_conditions, z3.Implies(self.varConditions[stmt.cond.name], cond))
                    elif self.varConditions[stmt.cond.name] is not False:
                        self.assert_conditions = z3.And(self.assert_conditions, cond)

                elif isinstance(stmt, ChironSSA.AssumeCommand):
                    cond = None
                    if isinstance(stmt.cond, ChironSSA.BoolTrue):
                        cond = z3.BoolVal(True)
                    elif isinstance(stmt.cond, ChironSSA.BoolFalse):
                        cond = z3.BoolVal(False)
                    elif isinstance(stmt.cond, ChironSSA.Var):
                        cond = z3.Bool(stmt.cond.name)
                    if self.varConditions[stmt.cond.name] not in (None, True, False):
                        self.assume_conditions = z3.And(self.assume_conditions, z3.Implies(self.varConditions[stmt.cond.name], cond))
                    elif self.varConditions[stmt.cond.name] is not False:
                        self.assume_conditions = z3.And(self.assume_conditions, cond)

                elif isinstance(stmt, ChironSSA.CosCommand): # Only for angles given in angle_conf
                    rvar = z3.Real(stmt.rvar.name)
                    # rhs_expr = z3.If(rvar == 0, 1, z3.If(rvar == 90, 0, z3.If(rvar == 180, -1, 0)))
                    rhs_expr = 0
                    for (angle, cos, _) in self.angle_conf:
                        rhs_expr = z3.If(rvar == angle, cos, rhs_expr)
                    if self.varConditions[stmt.lvar.name] not in (None, True, False):
                        self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], z3.Real(stmt.lvar.name) == rhs_expr))
                    elif self.varConditions[stmt.lvar.name] is not False:
                        self.solver.add(z3.Real(stmt.lvar.name) == rhs_expr)

                elif isinstance(stmt, ChironSSA.SinCommand):
                    rvar = z3.Real(stmt.rvar.name)
                    # rhs_expr = z3.If(rvar == 0, 0, z3.If(rvar == 90, 1, z3.If(rvar == 180, 0, -1)))
                    rhs_expr = 0
                    for (angle, _, sin) in self.angle_conf:
                        rhs_expr = z3.If(rvar == angle, sin, rhs_expr)

                    if self.varConditions[stmt.lvar.name] not in (None, True, False):
                        self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], z3.Real(stmt.lvar.name) == rhs_expr))
                    elif self.varConditions[stmt.lvar.name] is not False:
                        self.solver.add(z3.Real(stmt.lvar.name) == rhs_expr)

                elif isinstance(stmt, ChironSSA.MoveCommand):
                    pass
                elif isinstance(stmt, ChironSSA.PenCommand):
                    pass
                elif isinstance(stmt, ChironSSA.GotoCommand):
                    pass
                elif isinstance(stmt, ChironSSA.ConditionCommand):
                    pass
                elif isinstance(stmt, ChironSSA.NoOpCommand):
                    pass
                elif isinstance(stmt, ChironSSA.PauseCommand):
                    pass
                else:
                    raise Exception("Unknown SSA instruction")
                
        self.solver_without_cond.add(self.solver.assertions())
        self.assert_conditions = z3.Tactic('ctx-simplify').apply(self.assert_conditions).as_expr()
        self.angle_conditions = z3.Tactic('ctx-simplify').apply(self.angle_conditions).as_expr()
        self.assume_conditions = z3.Tactic('ctx-simplify').apply(self.assume_conditions).as_expr()

    def solve(self, inputVars):
        # Uncomment following lines if input variables are restricted to be integers.
        # for var in inputVars:
        #     # should be integer
        #     varname = var + "$0"
        #     self.solver_without_cond.add(z3.ToInt(z3.Real(varname)) == z3.Real(varname))
        #     self.solver.add(z3.ToInt(z3.Real(varname)) == z3.Real(varname))

        
        checker_with_assume = z3.Solver()
        checker_with_assume.add(self.solver_without_cond.assertions())
        checker_with_assume.add(self.assume_conditions)

        assume_check = checker_with_assume.check()
        if assume_check == z3.unsat:
            print("The program cannot execute within the provided bounds. Consider increasing the bounds and trying again..")
            return
        elif assume_check == z3.unknown:
            print("Cannot determine if bounds are sufficient")
            return

        checker_with_angles = z3.Solver()
        checker_with_angles.add(self.solver_without_cond.assertions())
        checker_with_angles.add(self.angle_conditions)
        checker_with_angles.add(self.assume_conditions)

        angles_check = checker_with_angles.check()
        if angles_check == z3.unsat:
            print("Angle not in angles.conf for all cases")
            return
        elif angles_check == z3.unknown:
            print("Cannot determine if angles are as per configuration file")
            return
        
        self.solver.add(z3.Not(self.assert_conditions))
        self.solver.add(self.angle_conditions)
        self.solver.add(self.assume_conditions)
        
        sat = self.solver.check()

        if sat == z3.sat:
            print("Condition not satisfied! Bug found for the following input:")
            model = self.solver.model()

            solution = {}
            for var in model:
                varname, index = str(var).split("$")
                if varname in inputVars and index == "0":
                    solution[varname] = model[var]
            for var in solution:
                    print(var + " = " + str(solution[var]))

        elif sat == z3.unsat:
            print("Condition satisfied for all inputs!")
        else:
            print("Unknown")

