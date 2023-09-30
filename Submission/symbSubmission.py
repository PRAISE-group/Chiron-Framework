from z3 import *
import argparse
import json
import sys

sys.path.insert(0, "../ChironCore/")

from interfaces.sExecutionInterface import *
from ChironAST.builder import astGenPass
import z3solver as zs
from irhandler import *
from interpreter import *
import ast

# This is an example program showing the use
# of Z3 Solver in python.
def example(s):
    # To add symbolic variable x to solver
    s.addSymbVar("x")
    s.addSymbVar("y")
    # To add constraint in form of string
    s.addConstraint("x==5+y")
    s.addConstraint("And(x==y,x>5)")
    # s.addConstraint('Implies(x==4,y==x+8')
    # To access solvers directly use s.s.<function of z3>()
    print("constraints added till now", s.s.assertions())
    # To assign z=x+y
    s.addAssignment("z", "x+y")
    # To get any variable assigned
    print("variable assignment of z =", s.getVar("z"))

# IMPLEMENT THIS
# FEEL FREE TO MODIFIY THIS CODE.
def checkEq(args, ir):
    file1 = open("testData.json", "r+")
    testData = json.loads(file1.read())
    file1.close()

    solver = zs.z3Solver()
    testData = convertTestData(testData)

    # to see what test data has been read.
    # print(testData)

    # This is the data read from the "-e" flag
    output = args.output
    # example(s)
    # TODO: write code to check equivalence


if __name__ == "__main__":
    # you are free to add your own arguments and use them
    # in the functions of this file.
    cmdparser = argparse.ArgumentParser(
        description="symbSubmission for assignment Program Synthesis using Symbolic Execution"
    )
    cmdparser.add_argument("progfl")
    cmdparser.add_argument("-b", "--bin", action="store_true", help="load binary IR")
    cmdparser.add_argument(
        "-e",
        "--output",
        default=list(),
        type=ast.literal_eval,
        help="pass variables to Chiron program in python dictionary format",
    )
    # This object is use to store and pass the ir around.
    irHandler2 = IRHandler(None)
    args = cmdparser.parse_args()

    # generate IR of the program given
    # or load it from .kw file.
    if args.bin:
        ir = irHandler2.loadIR(args.progfl)
    else:
        parseTree = getParseTree(args.progfl)
        astgen = astGenPass()
        ir = astgen.visitStart(parseTree)

    irHandler2.pretty_print(irHandler2.ir)

    checkEq(args, ir)
    exit()
