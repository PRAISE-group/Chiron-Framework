'''
This file is used to convert the 3 address code IR to SMT-LIB format.
'''
import z3
from ChironAST import ChironTAC

# def parseExpression(node):
#     if isinstance(node, ChironTAC.TAC_ArithExpr):
#         if isinstance(node, ChironTAC.TAC_BinArithOp):
#             if isinstance(node.lvar, ChironTAC.TAC_Num):
#                 left = z3.IntVal(node.lvar.value)
#             else:
#                 left = z3.Int(node.lvar.name)
                
#             if isinstance(node.rvar, ChironTAC.TAC_Num):
#                 right = z3.IntVal(node.rvar.value)
#             else:
#                 right = z3.Int(node.rvar.name)
                
#             if isinstance(node, ChironTAC.TAC_Sum):
#                 return left.__add__(right)
#             elif isinstance(node, ChironTAC.TAC_Diff):
#                 return left.__sub__(right)
#             elif isinstance(node, ChironTAC.TAC_Mult):
#                 return left.__mul__(right)
#             elif isinstance(node, ChironTAC.TAC_Div):
#                 return left.__div__(right)
            
#         elif isinstance(node, ChironTAC.TAC_UnaryArithOp):
#             if isinstance(node, ChironTAC.TAC_UMinus):
#                 if isinstance(node.lvar, ChironTAC.TAC_Num):
#                     left = z3.IntVal(node.lvar.value)
#                 else:
#                     left = z3.Int(node.lvar.name)
                
#                 return left.__neg__()
            
#     elif isinstance(node, ChironTAC.TAC_BoolExpr):
#         if isinstance(node, ChironTAC.TAC_BinBoolOp):
#             if isinstance(node.lvar, ChironTAC.TAC_BoolFalse):
#                 left = z3.BoolVal(False)
#             elif isinstance(node.lvar, ChironTAC.TAC_BoolTrue):
#                 left = z3.BoolVal(True)
#             else:
#                 left = z3.Bool(node.lvar.name)
                
#             if isinstance(node.rvar, ChironTAC.TAC_BoolFalse):
#                 right = z3.BoolVal(False)
#             elif isinstance(node.rvar, ChironTAC.TAC_BoolTrue):
#                 right = z3.BoolVal(True)
#             else:
#                 right = z3.Bool(node.rvar.name)
            
#             if isinstance(node, ChironTAC.TAC_And):
#                 return left.__and__(right)
#             elif isinstance(node, ChironTAC.TAC_Or):
#                 return left.__or__(right)
#             elif isinstance(node, ChironTAC.TAC_LT):
#                 return left.__lt__(right)
#             elif isinstance(node, ChironTAC.TAC_GT):
#                 return left.__gt__(right)
#             elif isinstance(node, ChironTAC.TAC_LTE):
#                 return left.__le__(right)
#             elif isinstance(node, ChironTAC.TAC_GTE):
#                 return left.__ge__(right)
#             elif isinstance(node, ChironTAC.TAC_EQ):
#                 return left.__eq__(right)
#             elif isinstance(node, ChironTAC.TAC_NEQ):
#                 return left.__ne__(right)
#         elif isinstance(node, ChironTAC.TAC_Not):
#             if isinstance(node.var, ChironTAC.TAC_BoolFalse):
#                 left = z3.BoolVal(False)
#             elif isinstance(node.var, ChironTAC.TAC_BoolTrue):
#                 left = z3.BoolVal(True)
#             else:
#                 left = z3.Bool(node.var.name)
                
#             return left.__invert__()
#         elif isinstance(node, ChironTAC.BoolTrue):
#             return z3.BoolVal(True)
#         elif isinstance(node, ChironTAC.BoolFalse):
#             return z3.BoolVal(False)
        
#     else:
#         if isinstance(node, ChironTAC.Num):
#             return z3.IntVal(node.value)
#         elif isinstance(node, ChironTAC.Var):
#             return z3.Int(node.name)


class BMC:
    def __init__(self, ir):
        self.solver = z3.Solver()
        self.ir = ir

    def convert(self):
        for instruction, jumpTarget in self.ir:
            if isinstance(instruction, ChironTAC.TAC_AssignmentCommand):
                lhs = z3.Int(instruction.lvar.name)
                if isinstance(instruction.rvar1, ChironTAC.TAC_Num):
                    rvar1 = z3.IntVal(instruction.rvar1.value)
                elif isinstance(instruction.rvar1, ChironTAC.TAC_Var):
                    rvar1 = z3.Int(instruction.rvar1.name)
                    
                if isinstance(instruction.rvar2, ChironTAC.TAC_Num):
                    rvar2 = z3.IntVal(instruction.rvar2.value)
                elif isinstance(instruction.rvar2, ChironTAC.TAC_Var):
                    rvar2 = z3.Int(instruction.rvar2.name)
                    
                if instruction.op == "+":
                    self.solver.add(lhs == rvar1 + rvar2)
                elif instruction.op == "-":
                    self.solver.add(lhs == rvar1 - rvar2)
                elif instruction.op == "*":
                    self.solver.add(lhs == rvar1 * rvar2)
                elif instruction.op == "/":
                    self.solver.add(lhs == rvar1 / rvar2)

            elif isinstance(instruction, ChironTAC.TAC_AssertCommand):
                if isinstance(instruction.cond, ChironTAC.TAC_BinBoolOp):
                    if isinstance(instruction.cond.lvar, ChironTAC.TAC_BoolFalse):
                        left = z3.BoolVal(False)
                    elif isinstance(instruction.cond.lvar, ChironTAC.TAC_BoolTrue):
                        left = z3.BoolVal(True)
                    else:
                        left = z3.Bool(instruction.cond.lvar.name)
                        
                self.solver.add(z3.Not(condition))
                
            # TODO: Implement the rest of the commands
    
    def solve(self):
        print("Assertions are:")
        print(self.solver.assertions())
        sat = self.solver.check()
        if sat == z3.sat:
            print("Bug found!")
            print(self.solver.model())
        else:
            print("No bug found!")