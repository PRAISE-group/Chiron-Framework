# Static Single Assignment (SSA) generation for Chiron 
class SSA(object):
    pass

# Instruction Classes
class SSA_Instruction(SSA):
    pass

class SSA_PhiCommand(SSA_Instruction):
    def __init__(self, lvar, rvars):
        self.lvar = lvar
        self.rvars = rvars
    
    def __str__(self):
        return self.lvar.__str__() + " = PHI " + ", ".join([var.__str__() for var in list(self.rvars)])

class SSA_AssignmentCommand(SSA_Instruction):
    def __init__(self, lvar, rvar1, rvar2, op):
        self.lvar = lvar
        self.rvar1 = rvar1
        self.rvar2 = rvar2
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " = " + self.rvar1.__str__() + " " + self.op + " " + self.rvar2.__str__()
    
class SSA_ConditionCommand(SSA_Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return "BRANCH: " + self.cond.__str__()
    
class SSA_AssertCommand(SSA_Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return "ASSERT: " + self.cond.__str__()
    
class SSA_MoveCommand(SSA_Instruction):
    def __init__(self, motion, var):
        self.direction = motion
        self.var = var

    def __str__(self):
        return "MOVE: " + self.direction + " " + self.var.__str__()
    
class SSA_PenCommand(SSA_Instruction):
    def __init__(self, penstat):
        self.status = penstat

    def __str__(self):
        return "PEN: " + self.status
    
class SSA_GotoCommand(SSA_Instruction):
    def __init__(self, x, y):
        self.xcor = x
        self.ycor = y

    def __str__(self):
        return "goto " + str(self.xcor) + " " + str(self.ycor)
    
class SSA_NoOpCommand(SSA_Instruction):
    def __str__(self):
        return "NoOp"
    
class SSA_PauseCommand(SSA_Instruction):
    def __str__(self):
        return "Pause"
    

class SSA_Expression(SSA):
    pass
# -- Arithmetic Expressions ------------------------------------------
class SSA_ArithExpr(SSA_Expression):
    pass

class SSA_BinArithOp(SSA_ArithExpr):
    def __init__(self, lvar, rvar, op):
        self.lvar = lvar
        self.rvar = rvar
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " " + self.op + " " + self.rvar.__str__()

class SSA_Sum(SSA_BinArithOp):
    def __init__(self, lvar, rvar):
        SSA_BinArithOp.__init__(self, lvar, rvar, "+")

class SSA_Sub(SSA_BinArithOp):
    def __init__(self, lvar, rvar):
        SSA_BinArithOp.__init__(self, lvar, rvar, "-")

class SSA_Mul(SSA_BinArithOp):
    def __init__(self, lvar, rvar):
        SSA_BinArithOp.__init__(self, lvar, rvar, "*")

class SSA_Div(SSA_BinArithOp):
    def __init__(self, lvar, rvar):
        SSA_BinArithOp.__init__(self, lvar, rvar, "/")


class SSA_UnaryArithOp(SSA_ArithExpr):
    def __init__(self, op, var):
        self.op = op
        self.var = var

    def __str__(self):
        return self.op + " " + self.var.__str__()

class SSA_UMinus(SSA_UnaryArithOp):
    def __init__(self, var):
        SSA_UnaryArithOp.__init__(self, "-", var)


# -- Boolean Expressions --------------------------------------------
class SSA_BoolExpr(SSA_Expression):
    pass

class SSA_BinBoolOp(SSA_BoolExpr):
    def __init__(self, lvar, rvar, op):
        self.lvar = lvar
        self.rvar = rvar
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " " + self.op + " " + self.rvar.__str__()
    
class SSA_And(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, "and")

class SSA_Or(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, "or")

class SSA_LT(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, "<")

class SSA_GT(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, ">")

class SSA_LTE(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, "<=")

class SSA_GTE(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, ">=")

class SSA_EQ(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, "==")

class SSA_NEQ(SSA_BinBoolOp):
    def __init__(self, lvar, rvar):
        SSA_BinBoolOp.__init__(self, lvar, rvar, "!=")

class SSA_Not(SSA_BoolExpr):
    def __init__(self, var):
        self.var = var

    def __str__(self):
        return "not " + self.var.__str__()
    
class SSA_PenStatus(SSA_Expression):
    def __str__(self):
        return "penstatus"
    
class SSA_BoolTrue(SSA_Expression):
    def __str__(self):
        return "true"
    
class SSA_BoolFalse(SSA_Expression):
    def __str__(self):
        return "false"
    
# -- Value Expressions ----------------------------------------------
class SSA_Value(SSA_Expression):
    pass

class SSA_Num(SSA_Value):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class SSA_Var(SSA_Value):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
class SSA_Unused(SSA_Value):
    def __str__(self):
        return ""
