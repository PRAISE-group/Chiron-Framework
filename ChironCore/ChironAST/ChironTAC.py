# Three Address Code (TAC) generation for Chiron 
class TAC(object):
    pass

# Instruction Classes
class TAC_Instruction(TAC):
    pass

class TAC_AssignmentCommand(TAC_Instruction):
    def __init__(self, lvar, rvar1, rvar2, op):
        self.lvar = lvar
        self.rvar1 = rvar1
        self.rvar2 = rvar2
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " = " + self.rvar1.__str__() + " " + self.op + " " + self.rvar2.__str__()
    
class TAC_ConditionCommand(TAC_Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return "BRANCH: " + self.cond.__str__()
    
class TAC_AssertCommand(TAC_Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return "ASSERT: " + self.cond.__str__()
    
class TAC_MoveCommand(TAC_Instruction):
    def __init__(self, motion, var):
        self.direction = motion
        self.var = var

    def __str__(self):
        return "MOVE: " + self.direction + " " + self.var.__str__()
    
class TAC_PenCommand(TAC_Instruction):
    def __init__(self, penstat):
        self.status = penstat

    def __str__(self):
        return "PEN: " + self.status
    
class TAC_GotoCommand(TAC_Instruction):
    def __init__(self, x, y):
        self.xcor = x
        self.ycor = y

    def __str__(self):
        return "goto " + str(self.xcor) + " " + str(self.ycor)
    
class TAC_NoOpCommand(TAC_Instruction):
    def __str__(self):
        return "NoOp"
    
class TAC_PauseCommand(TAC_Instruction):
    def __str__(self):
        return "Pause"
    

class TAC_Expression(TAC):
    pass
# -- Arithmetic Expressions ------------------------------------------
class TAC_ArithExpr(TAC_Expression):
    pass

class TAC_BinArithOp(TAC_ArithExpr):
    def __init__(self, lvar, rvar, op):
        self.lvar = lvar
        self.rvar = rvar
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " " + self.op + " " + self.rvar.__str__()

class TAC_Sum(TAC_BinArithOp):
    def __init__(self, lvar, rvar):
        TAC_BinArithOp.__init__(self, lvar, rvar, "+")

class TAC_Sub(TAC_BinArithOp):
    def __init__(self, lvar, rvar):
        TAC_BinArithOp.__init__(self, lvar, rvar, "-")

class TAC_Mul(TAC_BinArithOp):
    def __init__(self, lvar, rvar):
        TAC_BinArithOp.__init__(self, lvar, rvar, "*")

class TAC_Div(TAC_BinArithOp):
    def __init__(self, lvar, rvar):
        TAC_BinArithOp.__init__(self, lvar, rvar, "/")


class TAC_UnaryArithOp(TAC_ArithExpr):
    def __init__(self, op, var):
        self.op = op
        self.var = var

    def __str__(self):
        return self.op + " " + self.var.__str__()

class TAC_UMinus(TAC_UnaryArithOp):
    def __init__(self, var):
        TAC_UnaryArithOp.__init__(self, "-", var)


# -- Boolean Expressions --------------------------------------------
class TAC_BoolExpr(TAC_Expression):
    pass

class TAC_BinBoolOp(TAC_BoolExpr):
    def __init__(self, lvar, rvar, op):
        self.lvar = lvar
        self.rvar = rvar
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " " + self.op + " " + self.rvar.__str__()
    
class TAC_And(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, "and")

class TAC_Or(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, "or")

class TAC_LT(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, "<")

class TAC_GT(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, ">")

class TAC_LTE(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, "<=")

class TAC_GTE(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, ">=")

class TAC_EQ(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, "==")

class TAC_NEQ(TAC_BinBoolOp):
    def __init__(self, lvar, rvar):
        TAC_BinBoolOp.__init__(self, lvar, rvar, "!=")

class TAC_Not(TAC_BoolExpr):
    def __init__(self, var):
        self.var = var

    def __str__(self):
        return "not " + self.var.__str__()
    
class TAC_PenStatus(TAC_Expression):
    def __str__(self):
        return "penstatus"
    
class TAC_BoolTrue(TAC_Expression):
    def __str__(self):
        return "true"
    
class TAC_BoolFalse(TAC_Expression):
    def __str__(self):
        return "false"
    
# -- Value Expressions ----------------------------------------------
class TAC_Value(TAC_Expression):
    pass

class TAC_Num(TAC_Value):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class TAC_Var(TAC_Value):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
class TAC_Unused(TAC_Value):
    def __str__(self):
        return ""
