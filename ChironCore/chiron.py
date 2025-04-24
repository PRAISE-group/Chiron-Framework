#!/usr/bin/env python3
Release = "Chiron v1.0.4"

import ast
import sys
from ChironAST.builder import astGenPass
import abstractInterpretation as AI
import dataFlowAnalysis as DFA
import ssa.SSATransformation as SSA
import ssa.outOfSSA as OutSSA
import ssa.SSCP as SSCP
from sbfl import testsuiteGenerator
from ChironAST.ChironAST import (
    Instruction, PhiCommand, AssignmentCommand, ConditionCommand, BoolExpr, BoolFalse, Var as VarExpr, Num
)

sys.path.insert(0, "../Submission/")
sys.path.insert(0, "ChironAST/")
sys.path.insert(0, "cfg/")

import pickle
import time
import turtle
import argparse
from interpreter import *
from irhandler import *
from fuzzer import *
import sExecution as se
import cfg.cfgBuilder as cfgB
import submissionDFA as DFASub
import submissionAI as AISub
from sbflSubmission import computeRanks
import csv


def cleanup():
    pass


def stopTurtle():
    turtle.bye()


if __name__ == "__main__":
    print(Release)
    print(
        """
    ░█████╗░██╗░░██╗██╗██████╗░░█████╗░███╗░░██╗
    ██╔══██╗██║░░██║██║██╔══██╗██╔══██╗████╗░██║
    ██║░░╚═╝███████║██║██████╔╝██║░░██║██╔██╗██║
    ██║░░██╗██╔══██║██║██╔══██╗██║░░██║██║╚████║
    ╚█████╔╝██║░░██║██║██║░░██║╚█████╔╝██║░╚███║
    ░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝
    """
    )

    # process the command-line arguments
    cmdparser = argparse.ArgumentParser(
        description="Program Analysis Framework for ChironLang Programs."
    )

    # add arguments for parsing command-line arguments
    cmdparser.add_argument(
        "-p",
        "--ir",
        action="store_true",
        help="pretty printing the IR of a Chiron program to stdout (terminal)",
    )
    cmdparser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="execute Chiron program, the figure/shapes the turle draws is shown in a UI.",
    )

    cmdparser.add_argument(
        "-gr",
        "--fuzzer_gen_rand",
        action="store_true",
        help="Generate random input seeds for the fuzzer before fuzzing starts.",
    )

    cmdparser.add_argument(
        "-b", "--bin", action="store_true", help="load binary IR of a Chiron program"
    )
    
    cmdparser.add_argument(
        "-k", "--hooks", action="store_true", help="Run hooks for Kachua."
    )

    cmdparser.add_argument(
        "-z",
        "--fuzz",
        action="store_true",
        help="Run fuzzer on a Chiron program (seed values with '-d' or '--params' flag needed.)",
    )
    cmdparser.add_argument(
        "-t",
        "--timeout",
        default=10,
        type=float,
        help="Timeout Parameter for Analysis (in secs). This is the total timeout.",
    )
    cmdparser.add_argument("progfl")

    # passing variable values via command line. E.g.
    # ./chiron.py -r <program file> --params '{":x" : 10, ":z" : 20, ":w" : 10, ":k" : 2}'
    cmdparser.add_argument(
        "-d",
        "--params",
        default=dict(),
        type=ast.literal_eval,
        help="pass variable values to Chiron program in python dictionary format",
    )
    cmdparser.add_argument(
        "-c",
        "--constparams",
        default=dict(),
        type=ast.literal_eval,
        help="pass variable(for which you have to find values using circuit equivalence) values to Chiron program in python dictionary format",
    )
    cmdparser.add_argument(
        "-se",
        "--symbolicExecution",
        action="store_true",
        help="Run Symbolic Execution on a Chiron program (seed values with '-d' or '--params' flag needed) to generate test cases along all possible paths.",
    )
    # TODO: add additional arguments for parsing command-line arguments

    cmdparser.add_argument(
        "-ai",
        "--abstractInterpretation",
        action="store_true",
        help="Run abstract interpretation on a Chiron Program.",
    )
    cmdparser.add_argument(
        "-dfa",
        "--dataFlowAnalysis",
        action="store_true",
        help="Run data flow analysis using worklist algorithm on a Chiron Program.",
    )

    #added by Sarthak Motwani
    cmdparser.add_argument(
        "-ssa",
        "--ssa_transformation",
        action="store_true",
        help="Run SSA Transformation",
    )

    cmdparser.add_argument(
        "-outssa",
        "--out_of_ssa",
        action="store_true",
        help="Run Out of SSA Transformation",
    )

    cmdparser.add_argument(
        "-sscp",
        "--sparse_simple_const_prop",
        action="store_true",
        help="Perform SSCP optimization",
    )

    # adding ends here
    cmdparser.add_argument(
        "-sbfl",
        "--SBFL",
        action="store_true",
        help="Run Spectrum-basedFault localizer on Chiron program",
    )
    cmdparser.add_argument("-bg", "--buggy", help="buggy Chiron program path", type=str)
    cmdparser.add_argument(
        "-vars",
        "--inputVarsList",
        help="A list of input variables of given Chiron program",
        type=str,
    )
    cmdparser.add_argument(
        "-nt", "--ntests", help="number of tests to generate", default=10, type=int
    )
    cmdparser.add_argument(
        "-pop",
        "--popsize",
        help="population size for Genetic Algorithm.",
        default=100,
        type=int,
    )
    cmdparser.add_argument(
        "-cp", "--cxpb", help="cross-over probability", default=1.0, type=float
    )
    cmdparser.add_argument(
        "-mp", "--mutpb", help="mutation probability", default=1.0, type=float
    )
    cmdparser.add_argument(
        "-cfg_gen",
        "--control_flow",
        help="Generate the CFG of the given turtle program",
        action="store_true",
    )
    cmdparser.add_argument(
        "-cfg_dump",
        "--dump_cfg",
        help="Generate the CFG of the given turtle program",
        action="store_true",
    )
    cmdparser.add_argument(
        "-dump",
        "--dump_ir",
        help="Dump the IR to a .kw (pickle file)",
        action="store_true",
    )
    cmdparser.add_argument(
        "-ng",
        "--ngen",
        help="number of times Genetic Algorithm iterates",
        default=100,
        type=int,
    )
    cmdparser.add_argument(
        "-vb",
        "--verbose",
        help="To display computation to Console",
        default=True,
        type=bool,
    )

    args = cmdparser.parse_args()
    ir = ""

    if not (type(args.params) is dict):
        raise ValueError("Wrong type for command line arguement '-d' or '--params'.")

    # Instantiate the irHandler
    # this object is passed around everywhere.
    irHandler = IRHandler(ir)

    # generate IR
    if args.bin:
        ir = irHandler.loadIR(args.progfl)
    else:
        parseTree = getParseTree(args.progfl)
        astgen = astGenPass()
        ir = astgen.visitStart(parseTree)

    # Set the IR of the program.
    irHandler.setIR(ir)

    # generate control_flow_graph from IR statements.
    if args.control_flow:
        cfg = cfgB.buildCFG(ir, "control_flow_graph")
        irHandler.setCFG(cfg)
    else:
        irHandler.setCFG(None)

    if args.dump_cfg:
        cfgB.dumpCFG(cfg, "cfg0_simple")
        # set the cfg of the program.

    #Added by Sarthak Motwani for SSA Transformation + Out-of-SSA + SSCP
    if args.ssa_transformation:
        # Handling parameters
        if args.params:
            for var in args.params.keys():
                if not isinstance(args.params[var], (int, float)):
                    raise ValueError(f"{args.params[var]} is not a number")
                rhs_val = Num(args.params[var])
                if not var.startswith(':'):
                    var = ':'+ var
                # print(var, args.params[var])
                lhs_var = VarExpr(var)
                assignment = AssignmentCommand(lhs_var, rhs_val)
                ir.insert(0, (assignment, 1))
            args.params = {}

        cfg = cfgB.buildCFG(ir, "control_flow_graph")
        irHandler.setCFG(cfg)
        ssa_cfg = SSA.build_ssa(ir, cfg)
        sscp_cfg = ssa_cfg
        result_sscp = None
        
        if args.sparse_simple_const_prop:
            sscp_obj = SSCP.SSCP(ssa_cfg)
            result_sscp = sscp_obj.get_results()
            SSCP.optimize_ir(ssa_cfg, sscp_obj, ir, result_sscp)
            sscp_cfg = cfgB.buildCFG(ir, "cfg_sscp")
            cfgB.dumpCFG(sscp_cfg, "cfg6_new_sscp")
            
        if args.out_of_ssa:
            OutSSA.out_of_ssa(ir, sscp_cfg, result_sscp)

    #Adding ends

    if args.ir:
        irHandler.pretty_print(irHandler.ir)

    if args.abstractInterpretation:
        AISub.analyzeUsingAI(irHandler)
        print("== Abstract Interpretation ==")

    if args.dataFlowAnalysis:
        irOpt = DFASub.optimizeUsingDFA(irHandler)
        print("== Optimized IR ==")
        irHandler.pretty_print(irHandler.ir)

    if args.dump_ir:
        irHandler.pretty_print(irHandler.ir)
        irHandler.dumpIR("optimized.kw", irHandler.ir)

    if args.symbolicExecution:
        print("symbolicExecution")
        if not args.params:
            raise RuntimeError(
                "Symbolic Execution needs initial seed values. Specify using '-d' or '--params' flag."
            )
        """
        How to run symbolicExecution?
        # ./chiron.py -t 100 --symbolicExecution example/example2.tl -d '{":dir": 10, ":move": -90}'
        """
        se.symbolicExecutionMain(
            irHandler, args.params, args.constparams, timeLimit=args.timeout
        )

    if args.fuzz:
        if not args.params:
            raise RuntimeError(
                "Fuzzing needs initial seed values. Specify using '-d' or '--params' flag."
            )
        """
        How to run fuzzer?
        # ./chiron.py -t 100 --fuzz example/example1.tl -d '{":x": 5, ":y": 100}'
        # ./chiron.py -t 100 --fuzz example/example2.tl -d '{":dir": 3, ":move": 5}'
        """
        fuzzer = Fuzzer(irHandler, args)
        cov, corpus = fuzzer.fuzz(
            timeLimit=args.timeout, generateRandom=args.fuzzer_gen_rand
        )
        print(f"Coverage : {cov.total_metric},\nCorpus:")
        for index, x in enumerate(corpus):
            print(f"\tInput {index} : {x.data}")

    if args.run:
        # for stmt,pc in ir:
        #     print(str(stmt.__class__.__bases__[0].__name__),pc)

        inptr = ConcreteInterpreter(irHandler, args)
        terminated = False
        inptr.initProgramContext(args.params)
        while True:
            terminated = inptr.interpret()
            if terminated:
                break
        print("Program Ended.")
        print()
        print("Press ESCAPE to exit")
        turtle.listen()
        turtle.onkeypress(stopTurtle, "Escape")
        turtle.mainloop()

    if args.SBFL:
        if not args.buggy:
            raise RuntimeError(
                "test-suite generator needs buggy program also. Specify using '--buggy' flag."
            )
        if not args.inputVarsList:
            raise RuntimeError(
                "please specify input variable list. Specify using '--inputVarsList'  or '-vars' flag."
            )
        """
        How to run SBFL?
        Consider we have :
            a correct program = sbfl1.tl
            corresponding buggy program sbfl1_buggy.tl
            input variables = :x, :y :z
            initial test-suite size = 20.
            Maximum time(in sec) to run a test-case = 10.
        Since we want to generate optimized test suite using genetic-algorithm,
        therefore we also need to provide:
            the intial population size = 100
            cross-over probabiliy = 1.0
            mutation probability = 1.0
            number of times GA to iterate = 100, therefore
        command : ./chiron.py --SBFL ./example/sbfl1.tl --buggy ./example/sbfl1_buggy.tl \
            -vars '[":x", ":y", ":z"]' --timeout 1 --ntests 20 --popsize 100 --cxpb 1.0 --mutpb 1.0 --ngen 100 --verbose True
        Note : if a program doesn't take any input vars them pass argument -vars as '[]'
        """

        print("SBFL...")
        # generate IR of correct program
        parseTree = getParseTree(args.progfl)
        astgen = astGenPass()
        ir1 = astgen.visitStart(parseTree)

        # generate IR of buggy program
        parseTree = getParseTree(args.buggy)
        astgen = astGenPass()
        ir2 = astgen.visitStart(parseTree)

        irhandler1 = IRHandler(ir1)
        irhandler2 = IRHandler(ir2)

        # Generate Optimized Test Suite.
        (
            original_testsuite,
            original_test,
            optimized_testsuite,
            optimized_test,
            spectrum,
        ) = testsuiteGenerator(
            irhandler1=irhandler1,
            irhandler2=irhandler2,
            inputVars=eval(args.inputVarsList),
            Ntests=args.ntests,
            timeLimit=args.timeout,
            popsize=args.popsize,
            cxpb=args.cxpb,
            mutpb=args.mutpb,
            ngen=args.ngen,
            verbose=args.verbose,
        )
        # compute ranks of components and write to file
        computeRanks(
            spectrum=spectrum,
            outfilename="{}_componentranks.csv".format(args.buggy.replace(".tl", "")),
        )

        # write all output data.
        with open(
            "{}_tests-original_act-mat.csv".format(args.buggy.replace(".tl", "")), "w"
        ) as file:
            writer = csv.writer(file)
            writer.writerows(original_testsuite)

        with open(
            "{}_tests-original.csv".format(args.buggy.replace(".tl", "")), "w"
        ) as file:
            writer = csv.writer(file)
            for test in original_test:
                writer.writerow([test])

        with open(
            "{}_tests-optimized_act-mat.csv".format(args.buggy.replace(".tl", "")), "w"
        ) as file:
            writer = csv.writer(file)
            writer.writerows(optimized_testsuite)

        with open(
            "{}_tests-optimized.csv".format(args.buggy.replace(".tl", "")), "w"
        ) as file:
            writer = csv.writer(file)
            for test in optimized_test:
                writer.writerow([test])

        with open("{}_spectrum.csv".format(args.buggy.replace(".tl", "")), "w") as file:
            writer = csv.writer(file)
            writer.writerows(spectrum)
        print("DONE..")
