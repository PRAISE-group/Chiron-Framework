from z3 import *
from ChironAST import ChironAST
# sys.path.insert(0, '../Submission/')
# import submission


def handleVar(z3Vars, lhs, var):
    right = var.__str__()
    setAttr(z3Vars,lhs,right.strip().replace(":", "z3Vars."))

def handleSum(z3Vars, lhs, expr):
    if isinstance(expr.lexpr, ChironAST.Var):
        left = expr.lexpr.__str__()
    if isinstance(expr.lexpr, ChironAST.Num):
        left = expr.lexpr.__str__()

    if isinstance(expr.rexpr, ChironAST.Var):
        right = expr.rexpr.__str__()
    if isinstance(expr.rexpr, ChironAST.Num):
        right = expr.rexpr.__str__()
    exp = left.strip().replace(":", "z3Vars.")+"+"+right.strip().replace(":", "z3Vars.")
    setAttr(z3Vars,lhs,convertExp(z3Vars,exp))

def handleAssignment(z3Vars,stmt):
    lhs = str(stmt.lvar).replace(":","")
    rhs = str(stmt.rexpr).strip().replace(":", "z3Vars.")
    setAttr(z3Vars,lhs,convertExp(z3Vars,rhs))



class z3Context:
    pass

def convertExp(z3Vars,temp):
    _locals = locals()
    exec("exp = %s"%(temp),globals(),_locals)
    exp = _locals['exp']
    return exp

def convertTestData(testData):
    for tests in testData:
        testData[tests]["params"] = convertExp(None,testData[tests]["params"])
        testData[tests]["constparams"] = convertExp(None,testData[tests]["constparams"])
        testData[tests]["coverage"] = convertExp(None,testData[tests]["coverage"])
        testData[tests]["pc"] = convertExp(None,testData[tests]["pc"])
        testData[tests]["pcEval"] = convertExp(None,testData[tests]["pcEval"])
        testData[tests]["symbEnc"] = convertExp(None,testData[tests]["symbEnc"])
        testData[tests]["constraints"] = testData[tests]["constraints"][1:-1].split(",\n")
        # print(testData[tests]["constparams"],type(testData[tests]["constparams"]))
    return testData

def setAttr(cls,lhs,rhs):
    # print("setAttr",cls,lhs,rhs)
    setattr(cls,lhs,rhs)
    # exec("setattr(cls,%s,%s)"%("lhs","rhs"))



def getVarName():
    pass


class z3Solver():
    def __init__(self, ir):
        self.s = Solver()
        self.ir = ir
        self.z3Vars = z3Context()
        self.z3VarMap = {} # mapping between variable string and z3 variable
    def resetSolver(self,):
        self.s.reset()


    def initProgramContext(self, params):
        del self.z3Vars
        self.z3Vars = z3Context()
        for key,val in params.items():
            var = key.replace(":","")
            setAttr(self.z3Vars,var,Int(var))

    def handleCondition(self, stmt,negation):
        temp = str(stmt).replace(":","self.z3Vars.")
        _locals = locals()
        try:
            exec("exp = %s"%(temp),globals(),_locals)
        except:
            print("Statement \"",stmt,"\" not supported for symbolic execution")
            exit()
        exp = _locals['exp']
        if negation:
            self.s.add(Not(exp))
            pass
        else:
            self.s.add(exp)
            pass
        return str(stmt).replace(":","s.z3Vars.")

    def handleMove(self, stmt):
        # TODO
        pass

    def handlePen(self, stmt):
        # TODO
        pass

    def handleGotoCommand(self, stmt):
        # TODO
        pass

    def handleNoOpCommand(self, stmt):
        # TODO
        pass

    def eval(self, stmt):
        if isinstance(stmt, ChironAST.AssignmentCommand):
            handleAssignment(self.z3Vars,stmt)
        elif str(stmt)=="False":
            pass
        elif isinstance(stmt, ChironAST.MoveCommand):
            self.handleMove(stmt)
        elif isinstance(stmt, ChironAST.PenCommand):
            self.handlePen(stmt)
        elif isinstance(stmt, ChironAST.GotoCommand):
            self.handleGotoCommand(stmt)
        elif isinstance(stmt, ChironAST.NoOpCommand):
            self.handleNoOpCommand(stmt)
        else:
            raise NotImplementedError("Unknown instruction: %s, %s."%(type(stmt), stmt))
        pass
