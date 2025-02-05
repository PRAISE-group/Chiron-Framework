import sys

sys.path.insert(0, "../ChironCore/ChironAST/")

from ChironAST import ChironAST

def IrToSmtlib(irList):
    for item in irList:
        if(type(item[0]) != ChironAST.AssignmentCommand):
            print("Only Assignment commands are supported")
            return
        else:
            print(f"assert({item[0]})")