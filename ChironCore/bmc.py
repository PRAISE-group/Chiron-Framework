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
        self.bbConditions[self.line_to_bb_map[0]] = z3.BoolVal(True)

        self.setConditions(self.line_to_bb_map[len(self.ir)])

        self.varConditions = {} # varConditions[var] = condition for var
        for (stmt, tgt), line in zip(self.ir, range(len(self.ir))):
            if isinstance(stmt, ChironSSA.AssignmentCommand):
                self.varConditions[stmt.lvar.name] = self.bbConditions[self.line_to_bb_map[line]]

    def setConditions(self, node):        
        for pred in self.cfg.predecessors(node):
            if self.bbConditions[pred] == None:
                self.setConditions(pred)
            instr = pred.instrlist[-1][0]
            temp_cond = None
            if isinstance(instr, ChironSSA.ConditionCommand) and type(instr.cond) == ChironSSA.Var:
                edge_label = self.cfg.get_edge_label(pred, node)
                if edge_label == 'Cond_True':
                    temp_cond = z3.And(self.bbConditions[pred], z3.Bool(instr.cond.name))
                elif edge_label == 'Cond_False':
                    temp_cond = z3.And(self.bbConditions[pred], z3.Not(z3.Bool(instr.cond.name)))
            else:
                temp_cond = self.bbConditions[pred]
            if self.bbConditions[node] == None:
                self.bbConditions[node] = temp_cond
            else:
                self.bbConditions[node] = z3.Or(self.bbConditions[node], temp_cond)

    def convertSSAtoSMT(self):
        for stmt, tgt in self.ir:
            if isinstance(stmt, ChironSSA.PhiCommand): # TODO: Add support for Phi commands
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

    def solve(self):
        print("Assertions are:")
        print(self.solver.assertions())
        print()
        sat = self.solver.check()
        if sat == z3.sat:
            print("Condition not satisfied!")
            print(self.solver.model())
        else:
            print("Condition always holds true!")

