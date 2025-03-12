'''
This file is used to convert the SSA IR to SMT-LIB format.
'''
import z3
from ChironSSA import ChironSSA
from cfg import cfgBuilder

class BMC:
    def __init__(self, ir):
        self.solver = z3.Solver()
        self.ir = ir
        self.cfg, self.line_to_bb_map = cfgBuilder.buildCFG(ir)

        self.bbConditions = {} # bbConditions[bb] = condition for bb
        for bb in self.cfg:
            self.bbConditions[bb] = None

        self.buildConditions()

        self.varConditions = {} # varConditions[var] = condition for var
        for (stmt, _), line in zip(self.ir, range(len(self.ir))):
            if isinstance(stmt, ChironSSA.AssignmentCommand):
                self.varConditions[stmt.lvar.name] = self.bbConditions[self.line_to_bb_map[line]]

    def buildConditions(self):
        topological_order = list(self.cfg.get_topological_order())
        start = topological_order[0]
        start.setCondition(z3.BoolVal(True))
        topological_order.pop(0)
        for node in topological_order:
            for pred in self.cfg.predecessors(node):
                instr = pred.instrlist[-1][0]
                current_cond = node.get_condition()
                if isinstance(instr, ChironSSA.ConditionCommand) and type(instr.cond) == ChironSSA.Var:
                    cond = z3.Bool(instr.cond.name)
                    label = self.cfg.get_edge_label(pred, node)
                    if label == 'Cond_True':
                        node.setCondition(z3.Or(current_cond, z3.And(pred.get_condition(), cond)))
                    elif label == 'Cond_False':
                        node.setCondition(z3.Or(current_cond, z3.And(pred.get_condition(), z3.Not(cond))))
                else:
                    node.setCondition(z3.Or(pred.get_condition(), current_cond))
            
            t = z3.Tactic('ctx-simplify').apply(node.get_condition()).as_expr()
            node.setCondition(t)
            self.bbConditions[node] = node.get_condition()

    def convertSSAtoSMT(self):
        for stmt, _ in self.ir:
            if isinstance(stmt, ChironSSA.PhiCommand):
                lvar = z3.Int(stmt.lvar.name)
                rvars = [z3.Int(rvar.name) for rvar in stmt.rvars]
                
                rhs_expr = rvars[0]
                for i in range(1, len(stmt.rvars)):
                    rhs_expr = z3.If(self.varConditions[stmt.rvars[i].name], rvars[i], (rhs_expr))

                self.solver.add(lvar == rhs_expr)

            elif isinstance(stmt, ChironSSA.AssignmentCommand):
                lvar = None
                rvar1 = ChironSSA.Unused()
                rvar2 = ChironSSA.Unused()
                if stmt.op in ["+", "-", "*", "/"]:
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
                    self.solver.add(lvar == (rvar1 + rvar2))
                elif stmt.op == "-":
                    self.solver.add(lvar == (rvar1 - rvar2))
                elif stmt.op == "*":
                    self.solver.add(lvar == (rvar1 * rvar2))
                elif stmt.op == "/":
                    self.solver.add(lvar == (rvar1 / rvar2))
                elif stmt.op == "<":
                    self.solver.add(lvar == (rvar1 < rvar2))
                elif stmt.op == ">":
                    self.solver.add(lvar == (rvar1 > rvar2))
                elif stmt.op == "<=":
                    self.solver.add(lvar == (rvar1 <= rvar2))
                elif stmt.op == ">=":
                    self.solver.add(lvar == (rvar1 >= rvar2))
                elif stmt.op == "==":
                    self.solver.add(lvar == (rvar1 == rvar2))
                elif stmt.op == "!=":
                    self.solver.add(lvar == (rvar1 != rvar2))
                elif stmt.op == "and":
                    self.solver.add(lvar == z3.And(rvar1, rvar2))
                elif stmt.op == "or":
                    self.solver.add(lvar == z3.Or(rvar1, rvar2))
                elif stmt.op == "not":
                    self.solver.add(lvar == z3.Not(rvar2))

            elif isinstance(stmt, ChironSSA.AssertCommand):
                cond = None
                if isinstance(stmt.cond, ChironSSA.BoolTrue):
                    cond = z3.BoolVal(True)
                elif isinstance(stmt.cond, ChironSSA.BoolFalse):
                    cond = z3.BoolVal(False)
                elif isinstance(stmt.cond, ChironSSA.Var):
                    cond = z3.Bool(stmt.cond.name)
                self.solver.add(z3.Not(cond))

            # TODO add support for other SSA instructions
            # elif isinstance(stmt, ChironSSA.SSA_ConditionCommand):
            # elif isinstance(stmt, ChironSSA.SSA_MoveCommand):
            # elif isinstance(stmt, ChironSSA.SSA_PenCommand):
            # elif isinstance(stmt, ChironSSA.SSA_GotoCommand):
            # elif isinstance(stmt, ChironSSA.SSA_NoOpCommand):
            # elif isinstance(stmt, ChironSSA.SSA_PauseCommand):
            # else:
            #     raise Exception("Unknown SSA instruction")

    def solve(self, inputVars):
        print("Assertions are:")
        print(self.solver.assertions())
        print()
        sat = self.solver.check()
        if sat == z3.sat:
            print("Condition not satisfied! Bug found for the following input:")
            model = self.solver.model()
            for var in model:
                varname = str(var)[:-3]
                if varname in inputVars:
                    print(varname + " = " + str(model[var]))

        else:
            print("Condition always holds true!")

