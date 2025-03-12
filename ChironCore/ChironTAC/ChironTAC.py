# Three Address Code (TAC) generation for Chiron 
class TAC(object):
    pass

# Instruction Classes
class Instruction(TAC):
    pass

class CosCommand(Instruction):
    def __init__(self, lvar, rvar): # lvar = cos(rvar)
        self.lvar = lvar
        self.rvar = rvar
    
    def __str__(self):
        return self.lvar.__str__() + " = cos(" + self.rvar.__str__() + ")"

class SinCommand(Instruction):
    def __init__(self, lvar, rvar): # lvar = sin(rvar)
        self.lvar = lvar
        self.rvar = rvar
    
    def __str__(self):
        return self.lvar.__str__() + " = sin(" + self.rvar.__str__() + ")"

class AssignmentCommand(Instruction):
    def __init__(self, lvar, rvar1, rvar2, op):
        self.lvar = lvar
        self.rvar1 = rvar1
        self.rvar2 = rvar2
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " = " + self.rvar1.__str__() + " " + self.op + " " + self.rvar2.__str__()
    
class ConditionCommand(Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return "BRANCH: " + self.cond.__str__()
    
class AssertCommand(Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return "ASSERT: " + self.cond.__str__()
    
class MoveCommand(Instruction):
    def __init__(self, motion, var):
        self.direction = motion
        self.var = var

    def __str__(self):
        return "MOVE: " + self.direction + " " + self.var.__str__()
    
class PenCommand(Instruction):
    def __init__(self, penstat):
        self.status = penstat

    def __str__(self):
        return "PEN: " + self.status
    
class GotoCommand(Instruction):
    def __init__(self, x, y):
        self.xcor = x
        self.ycor = y

    def __str__(self):
        return "goto " + str(self.xcor) + " " + str(self.ycor)
    
class NoOpCommand(Instruction):
    def __str__(self):
        return "NoOp"
    
class PauseCommand(Instruction):
    def __str__(self):
        return "Pause"
    

class Expression(TAC):
    pass
# -- Arithmetic Expressions ------------------------------------------
class ArithExpr(Expression):
    pass

class BinArithOp(ArithExpr):
    def __init__(self, lvar, rvar, op):
        self.lvar = lvar
        self.rvar = rvar
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " " + self.op + " " + self.rvar.__str__()

class Sum(BinArithOp):
    def __init__(self, lvar, rvar):
        BinArithOp.__init__(self, lvar, rvar, "+")

class Sub(BinArithOp):
    def __init__(self, lvar, rvar):
        BinArithOp.__init__(self, lvar, rvar, "-")

class Mul(BinArithOp):
    def __init__(self, lvar, rvar):
        BinArithOp.__init__(self, lvar, rvar, "*")

class Div(BinArithOp):
    def __init__(self, lvar, rvar):
        BinArithOp.__init__(self, lvar, rvar, "/")


class UnaryArithOp(ArithExpr):
    def __init__(self, op, var):
        self.op = op
        self.var = var

    def __str__(self):
        return self.op + " " + self.var.__str__()

class UMinus(UnaryArithOp):
    def __init__(self, var):
        UnaryArithOp.__init__(self, "-", var)


# -- Boolean Expressions --------------------------------------------
class BoolExpr(Expression):
    pass

class BinBoolOp(BoolExpr):
    def __init__(self, lvar, rvar, op):
        self.lvar = lvar
        self.rvar = rvar
        self.op = op

    def __str__(self):
        return self.lvar.__str__() + " " + self.op + " " + self.rvar.__str__()
    
class And(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, "and")

class Or(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, "or")

class LT(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, "<")

class GT(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, ">")

class LTE(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, "<=")

class GTE(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, ">=")

class EQ(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, "==")

class NEQ(BinBoolOp):
    def __init__(self, lvar, rvar):
        BinBoolOp.__init__(self, lvar, rvar, "!=")

class Not(BoolExpr):
    def __init__(self, var):
        self.var = var

    def __str__(self):
        return "not " + self.var.__str__()
    
class PenStatus(Expression):
    def __str__(self):
        return "penstatus"
    
class BoolTrue(Expression):
    def __str__(self):
        return "true"
    
class BoolFalse(Expression):
    def __str__(self):
        return "false"
    
# -- Value Expressions ----------------------------------------------
class Value(Expression):
    pass

class Num(Value):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Var(Value):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
class Unused(Value):
    def __str__(self):
        return ""
