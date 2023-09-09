from z3 import *

class z3Solver(object):
    """docstring for z3Solver."""

    def __init__(self):
        super(z3Solver, self).__init__()
        self.s = Solver()
        self.tmp = None

    def addSymbVar(self,var):
        exec("global %s; %s = Int(\"%s\")"%(var,var,var))

    def addConstraint(self,constraint):
        exec("self.s.add(%s)"%(constraint))

    def addAssignment(self,lhs,rhs):
        exec("global %s;%s=%s"%(lhs,lhs,rhs))

    def assignSymbolicEncoding(self,exp):
        exec("self.tmp = %s"%(exp))
        return self.tmp

    def getVar(self,var):
        _locals = locals()
        exec("exp = %s"%(var),globals(),_locals)
        exp = _locals['exp']
        return exp
