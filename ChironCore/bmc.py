'''
This file is used to convert the SSA IR to SMT-LIB format.
'''
import z3
from ChironSSA import ChironSSA

class BMC:
    def __init__(self, ir):
        self.solver = z3.Solver()
        self.ir = ir

    def convert_SSA_to_SMT(self):
        for stmt, tgt in self.ir:
            if isinstance(stmt, ChironSSA.SSA_PhiCommand): # TODO: Add support for Phi commands
                lvar = z3.Int(stmt.lvar.name)
                rvars = []
                for rvar in stmt.rvars:
                    if isinstance(rvar, ChironSSA.SSA_Var):
                        rvars.append(z3.Int(rvar.name))
                    elif isinstance(rvar, ChironSSA.SSA_Num):
                        rvars.append(z3.IntVal(rvar.value))
                    elif isinstance(rvar, ChironSSA.SSA_BoolTrue):
                        rvars.append(z3.BoolVal(True))
                    elif isinstance(rvar, ChironSSA.SSA_BoolFalse):
                        rvars.append(z3.BoolVal(False))
                or_expr = z3.Or([lvar == rvar for rvar in rvars])
                self.solver.add(or_expr)

            elif isinstance(stmt, ChironSSA.SSA_AssignmentCommand):
                lvar = None
                rvar1 = None
                rvar2 = None
                if stmt.op in ["+", "-", "*", "/"]:
                    lvar = z3.Int(stmt.lvar.name)
                    if isinstance(stmt.rvar1, ChironSSA.SSA_Var):
                        rvar1 = z3.Int(stmt.rvar1.name)
                    elif isinstance(stmt.rvar1, ChironSSA.SSA_Num):
                        rvar1 = z3.IntVal(stmt.rvar1.value)
                    if isinstance(stmt.rvar2, ChironSSA.SSA_Var):
                        rvar2 = z3.Int(stmt.rvar2.name)
                    elif isinstance(stmt.rvar2, ChironSSA.SSA_Num):
                        rvar2 = z3.IntVal(stmt.rvar2.value)
                elif stmt.op in ["<", ">", "<=", ">=", "==", "!="]:
                    lvar = z3.Bool(stmt.lvar.name)
                    if isinstance(stmt.rvar1, ChironSSA.SSA_Var):
                        rvar1 = z3.Int(stmt.rvar1.name)
                    elif isinstance(stmt.rvar1, ChironSSA.SSA_Num):
                        rvar1 = z3.IntVal(stmt.rvar1.value)
                    if isinstance(stmt.rvar2, ChironSSA.SSA_Var):
                        rvar2 = z3.Int(stmt.rvar2.name)
                    elif isinstance(stmt.rvar2, ChironSSA.SSA_Num):
                        rvar2 = z3.IntVal(stmt.rvar2.value)
                elif stmt.op in ["and", "or"]:
                    lvar = z3.Bool(stmt.lvar.name)
                    if isinstance(stmt.rvar1, ChironSSA.SSA_Var):
                        rvar1 = z3.Bool(stmt.rvar1.name)
                    elif isinstance(stmt.rvar1, ChironSSA.SSA_BoolTrue):
                        rvar1 = z3.BoolVal(True)
                    if isinstance(stmt.rvar2, ChironSSA.SSA_Var):
                        rvar2 = z3.Bool(stmt.rvar2.name)
                    elif isinstance(stmt.rvar2, ChironSSA.SSA_BoolFalse):
                        rvar2 = z3.BoolVal(False)
                elif stmt.op == "not":
                    lvar = z3.Bool(stmt.lvar.name)
                    if isinstance(stmt.rvar1, ChironSSA.SSA_Var):
                        rvar1 = z3.Bool(stmt.rvar1.name)
                    elif isinstance(stmt.rvar1, ChironSSA.SSA_BoolTrue):
                        rvar1 = z3.BoolVal(True)
                    elif isinstance(stmt.rvar1, ChironSSA.SSA_BoolFalse):
                        rvar1 = z3.BoolVal(False)
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
                    self.solver.add(lvar == z3.Not(rvar1))

            elif isinstance(stmt, ChironSSA.SSA_AssertCommand):
                cond = None
                if isinstance(stmt.cond, ChironSSA.SSA_BoolTrue):
                    cond = z3.BoolVal(True)
                elif isinstance(stmt.cond, ChironSSA.SSA_BoolFalse):
                    cond = z3.BoolVal(False)
                elif isinstance(stmt.cond, ChironSSA.SSA_Var):
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