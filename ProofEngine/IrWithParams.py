import sys
sys.path.insert(0, "../ChironCore/ChironAST/")
from ChironAST import ChironAST

def IrWithParams(params):
    ir = []
    for var,value in params.items():
        var = ChironAST.Var(f"{var}")
        num = ChironAST.Num(value)
        assignNode = ChironAST.AssignmentCommand(var, num)
        ir.append((assignNode,1))
    return ir