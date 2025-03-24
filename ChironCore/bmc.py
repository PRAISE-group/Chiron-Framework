'''
This file is used to convert the SSA IR to SMT-LIB format.
'''
import z3
from ChironSSA import ChironSSA
from cfg import cfgBuilder

class BMC:
    def __init__(self, cfg):
        self.solver = z3.Solver()
        self.solver_without_cond = z3.Solver()
        self.angle_conditions = z3.BoolVal(True)
        self.assert_conditions = z3.BoolVal(True)
        self.cfg = cfg

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
                    lvar = z3.Int(stmt.lvar.name)
                    rvars = [z3.Int(rvar.name) for rvar in stmt.rvars]
                    
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
                        lvar = z3.Int(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Int(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.Num):
                            rvar1 = z3.IntVal(stmt.rvar1.value)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Int(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.Num):
                            rvar2 = z3.IntVal(stmt.rvar2.value)
                    elif stmt.op in ["<", ">", "<=", ">=", "==", "!="]:
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Int(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.Num):
                            rvar1 = z3.IntVal(stmt.rvar1.value)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Int(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.Num):
                            rvar2 = z3.IntVal(stmt.rvar2.value)
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
                            self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], lvar == (rvar1 % rvar2)))
                            if stmt.lvar.name.startswith(":turtleThetaDeg$"):
                                self.angle_conditions = z3.And(self.angle_conditions, z3.Implies(self.varConditions[stmt.lvar.name], z3.Or(lvar == 0, lvar == 90, lvar == 180, lvar == 270)))
                        elif self.varConditions[stmt.lvar.name] is not False:
                            self.solver.add(lvar == (rvar1 % rvar2))
                            if stmt.lvar.name.startswith(":turtleThetaDeg$"):
                                self.angle_conditions = z3.And(self.angle_conditions, z3.Or(lvar == 0, lvar == 90, lvar == 180, lvar == 270))
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
                    self.assert_conditions = z3.And(self.assert_conditions, cond)

                elif isinstance(stmt, ChironSSA.CosCommand): # Only for 0, 90, 180, 270 degree
                    rvar = z3.Int(stmt.rvar.name)
                    rhs_expr = z3.If(rvar == 0, 1, z3.If(rvar == 90, 0, z3.If(rvar == 180, -1, 0)))
                    if self.varConditions[stmt.lvar.name] not in (None, True, False):
                        self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], z3.Int(stmt.lvar.name) == rhs_expr))
                    elif self.varConditions[stmt.lvar.name] is not False:
                        self.solver.add(z3.Int(stmt.lvar.name) == rhs_expr)

                elif isinstance(stmt, ChironSSA.SinCommand):
                    rvar = z3.Int(stmt.rvar.name)
                    rhs_expr = z3.If(rvar == 0, 0, z3.If(rvar == 90, 1, z3.If(rvar == 180, 0, -1)))
                    if self.varConditions[stmt.lvar.name] not in (None, True, False):
                        self.solver.add(z3.Implies(self.varConditions[stmt.lvar.name], z3.Int(stmt.lvar.name) == rhs_expr))
                    elif self.varConditions[stmt.lvar.name] is not False:
                        self.solver.add(z3.Int(stmt.lvar.name) == rhs_expr)

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

    def solve(self, inputVars):
        self.solver.add(z3.Not(self.assert_conditions))
        self.solver.add(self.angle_conditions)

        # print("The clauses are:")
        # print(self.solver, end="\n\n")

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
            solver_with_angle = z3.Solver()
            solver_with_angle.add(self.solver_without_cond.assertions())
            solver_with_angle.add(self.angle_conditions)
            sat_angle = solver_with_angle.check()

            # solver_with_assert = z3.Solver()
            # solver_with_assert.add(self.solver_without_cond.assertions())
            # solver_with_assert.add(z3.Not(self.assert_conditions))
            # sat_assert = solver_with_assert.check()

            if sat_angle == z3.unsat:
                print("Angle not 0, 90, 180, 270 degrees for all cases")
            elif sat_angle != z3.unknown: # sat_assert is unsat
                print("Condition satisfied for all inputs!")
            else:
                print("Unknown")
        else:
            print("Unknown")

