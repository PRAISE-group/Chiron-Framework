# Test case generation with the help of Symbolic Execution
import sys
import time
from z3 import *
from interpreter import *
# sys.path.insert(0, '../Submission/')

from interfaces.sExecutionInterface import *
import json

def genPC(pc,pcEval, flipPC):
    # print("pc and pcEval")
    # print(pcEval)
    # print(flipPC)
    while len(flipPC)!=0:
        if flipPC[len(flipPC)-1]==1:
            flipPC = flipPC[:-1]
            pc = pc[:-1]
            pcEval = pcEval[:-1]
            continue
        pcEval[len(flipPC)-1] = not pcEval[len(flipPC)-1]
        flipPC[len(flipPC)-1] = 1
        # print(flipPC)
        # print(pc,pcEval,flipPC)
        return pc, pcEval, flipPC, False
    # print(pc,pcEval,flipPC)
    return None, None, None, True

def generateConditions(s,pcIndex,pc,params,coverage,ir,pcEval):
    print("\n\n For Parameters:",params)
    s.initProgramContext(params)
    s.resetSolver()
    for i in range(0,len(coverage)):
        if pcIndex>=len(pc):
            break
        irIndexPC = pc[pcIndex] if len(pc)!=0 else -1
        irIndexCoverage = coverage[i]
        stmt, tgt = ir[irIndexCoverage]
        if irIndexPC==irIndexCoverage or isinstance(ir[irIndexCoverage][0], ChironAST.ConditionCommand):
            if irIndexPC==irIndexCoverage:
                encPC = s.handleCondition(stmt,not pcEval[pcIndex])
            else:
                if str(ir[irIndexCoverage][0])=="False":
                    encPC = s.handleCondition(stmt,True)
                else:
                    encPC = s.handleCondition(stmt,False)
            print("stmt ",stmt)
            if isinstance(stmt.cond, ChironAST.NEQ):
                if str(stmt.cond.lexpr).startswith(":__rep_counter_"):
                    exec("s.s.add(s.z3Vars.%s>=0)"%str(stmt.cond.lexpr).replace(":",""))
            print(stmt, irIndexCoverage, ir[irIndexCoverage][0])
            print("symbEnc", vars(s.z3Vars),"\n")
            print("assertions", (s.s.assertions()),"\n")
            # if pcIndex<len(pc)-1:
            pcIndex+=1
            if pcIndex>=len(pc):
                break

        else:
            s.eval(stmt)
            print(stmt)
            print("symbEnc else", vars(s.z3Vars),"\n")
    return pc, pcIndex


def generateEncryption(s,pcIndex,pc,params,coverage,ir,pcEval):
    print("\n\n For Parameters:",params)
    s.initProgramContext(params)
    s.resetSolver()
    for i in range(0,len(coverage)):
        irIndexPC = pc[pcIndex] if len(pc)!=0 else -1
        irIndexCoverage = coverage[i]
        stmt, tgt = ir[irIndexCoverage]
        if irIndexPC==irIndexCoverage or isinstance(ir[irIndexCoverage][0], ChironAST.ConditionCommand):
            if irIndexPC==irIndexCoverage:
                encPC = s.handleCondition(stmt,not pcEval[pcIndex])
            else:
                if str(ir[irIndexCoverage][0])=="False":
                    encPC = s.handleCondition(stmt,True)
                else:
                    encPC = s.handleCondition(stmt,False)
            print("stmt ",stmt)
            if isinstance(stmt.cond, ChironAST.NEQ):
                if str(stmt.cond.lexpr).startswith(":__rep_counter_"):
                    exec("s.s.add(s.z3Vars.%s>=0)"%str(stmt.cond.lexpr).replace(":",""))
            print(stmt, irIndexCoverage, ir[irIndexCoverage][0])
            print("symbEnc", vars(s.z3Vars),"\n")
            print("assertions", (s.s.assertions()),"\n")
            if pcIndex<len(pc)-1:
                pcIndex+=1
        else:
            s.eval(stmt)
            print(stmt)
            print("symbEnc else", vars(s.z3Vars),"\n")
    return pc, pcIndex

def symbolicExecutionMain(irHandler, params, constparams, timeLimit=10):
    """[summary]

    Args:
        ir (List): List of program IR statments
        params (dict): Mapped variables with initial assignments.
        timeLimit (float/int): Total time(sec) to run the fuzzer loop for.

    Returns:
        tuple (coverageInfo, corpus) : Return coverage information and corpus of inputs.
    """
    print(f"[Symbolic Execution] Starting symbolic execution : init args -> {params}")
    for k in constparams:
        params[k]=constparams[k]
    # Initial Seed values from user.
    # temp_input = InputObject(data=params)
    start_time = time.time()
    # symbolic execution ends at this timestamp.
    endTime = time.time() + timeLimit
    flipPC = []
    s = z3Solver(irHandler.ir)
    s.initProgramContext(params)
    # The maximum time for symbolic execution of the
    # program must be less than end time.
    rnd1=0
    res = "sat"
    tmplist = []
    testData = {}
    while time.time() <= endTime:
        if str(res)=="sat":
            # print("Testcase: ",rnd1)
            rnd1+=1
            coverage = [] # coverage for current path
            pc = []
            pcEval = []
            inptr = ConcreteInterpreter(irHandler)
            inptr.pc = 0
            terminated = False
            inptr.initProgramContext(params)
            while time.time() <= endTime :
                coverage.append(inptr.pc)
                stmt, tgt = irHandler.ir[inptr.pc]
                if isinstance(stmt, ChironAST.ConditionCommand):
                    pc.append(inptr.pc)
                terminated = inptr.interpret()
                if isinstance(stmt, ChironAST.ConditionCommand):
                    pcEval.append(inptr.cond_eval)
                if terminated:
                    break
        # print("pc coverage",pc,coverage)
        if time.time() > endTime:
            break
        flipPC += [0 for i in range(len(flipPC),len(pc))]
        # print(flipPC)
        if str(pcEval) not in tmplist:
            tmplist.append(pcEval)
        # print("Coverage: ",coverage,"\nParameters: ",params,"\n\n")
        s.initProgramContext(params)
        s.resetSolver()
        pcIndex=0
        # print("testdata ",testData,pc,pcEval,coverage)
        pc, pcIndex =generateEncryption(s,pcIndex,pc,params,coverage,irHandler.ir,pcEval)
        if str(res)=="sat":
            data = {}
            params1={}
            for k in params:
                params1[k[1:]]=params[k]
            data['params']=str(params1)
            data['constparams']=str(list(constparams.keys()))
            data['coverage']=str(coverage)
            data['pc']=str(pc)
            data['pcEval']=str(pcEval)
            symbEnc1={}
            symbEnc = vars(s.z3Vars)
            for k in symbEnc:
                symbEnc1[k]=str(symbEnc[k])
            data['symbEnc']=str(symbEnc1)
            data['constraints']=str(s.s.assertions())
            testData[rnd1] = data
        print("pc before ",pc,pcEval,flipPC)
        pc, pcEval, flipPC, done = genPC(pc, pcEval, flipPC)
        print(s.s.assertions())
        print("pc after ",pc,pcEval,flipPC)
        if done:
            print("done break\n\n")
            break
        pcIndex=0
        s.initProgramContext(params)
        s.resetSolver()
        pc, pcIndex =generateConditions(s,pcIndex,pc,params,coverage,irHandler.ir,pcEval)
        res = s.s.check()
        print(s.s.assertions())
        print("res ",res)
        if str(res)=="sat":
            m = s.s.model()
            print("model printing",m,type(m))
            for x in m:
                for key in params:
                    if ":"+str(x) == key:
                        params[key] = m[x].as_long()
            print(params,"end")
    json_obj = json.dumps(testData,indent=4)
    print(json_obj)
    file1 = open("../Submission/testData.json","w+")
    file1.write(json_obj)
    file1.close()

    if time.time() >= endTime:
        print(f" Program took too long to execute. Terminated")
    else:
        print("All possible paths covered.")
    # exit()
    pass
