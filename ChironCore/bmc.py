'''
This file is used to convert the Kachua IR to SMT-LIB format.
'''
import z3
from ChironAST import ChironAST

def parseExpression(node):
    if isinstance(node, ChironAST.ArithExpr):
        if isinstance(node, ChironAST.BinArithOp):
            left = parseExpression(node.lexpr)
            right = parseExpression(node.rexpr)
            if isinstance(node, ChironAST.Sum):
                return left.__add__(right)
            elif isinstance(node, ChironAST.Diff):
                return left.__sub__(right)
            elif isinstance(node, ChironAST.Mult):
                return left.__mul__(right)
            elif isinstance(node, ChironAST.Div):
                return left.__div__(right)
        elif isinstance(node, ChironAST.UnaryArithOp):
            if isinstance(node, ChironAST.UMinus):
                left = parseExpression(node.expr)
                return left.__neg__()
            
    elif isinstance(node, ChironAST.BoolExpr):
        if isinstance(node, ChironAST.BinCondOp):
            left = parseExpression(node.lexpr)
            right = parseExpression(node.rexpr)
            if isinstance(node, ChironAST.AND):
                return left.__and__(right)
            elif isinstance(node, ChironAST.OR):
                return left.__or__(right)
            elif isinstance(node, ChironAST.LT):
                return left.__lt__(right)
            elif isinstance(node, ChironAST.GT):
                return left.__gt__(right)
            elif isinstance(node, ChironAST.LTE):
                return left.__le__(right)
            elif isinstance(node, ChironAST.GTE):
                return left.__ge__(right)
            elif isinstance(node, ChironAST.EQ):
                return left.__eq__(right)
            elif isinstance(node, ChironAST.NEQ):
                return left.__ne__(right)
        elif isinstance(node, ChironAST.NOT):
            left = parseExpression(node.expr)
            return left.__invert__()
        elif isinstance(node, ChironAST.BoolTrue):
            return z3.BoolVal(True)
        elif isinstance(node, ChironAST.BoolFalse):
            return z3.BoolVal(False)
        
    else:
        if isinstance(node, ChironAST.Num):
            return z3.IntVal(node.val)
        elif isinstance(node, ChironAST.Var):
            return z3.Int(node.varname)


class BMC:
    def __init__(self, ir):
        self.solver = z3.Solver()
        self.ir = ir

    def convert(self):
        for instruction, jumpTarget in self.ir:
            if isinstance(instruction, ChironAST.AssignmentCommand):
                left = z3.Int(instruction.lvar.varname)
                right = parseExpression(instruction.rexpr)
                self.solver.add(left == right)

            elif isinstance(instruction, ChironAST.AssertCommand):
                condition = parseExpression(instruction.cond)
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