#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Abstract syntax tree for ChironLang

class AST(object):
    pass


# --Instruction Classes-----------------------------------------------

class Instruction(AST):
    pass


class PrintCommand(Instruction):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return self.expr.__str__()


class AssignmentCommand(Instruction):
    def __init__(self, leftvar, rexpr):
        self.lvar = leftvar
        self.rexpr = rexpr

    def __str__(self):
        return self.lvar.__str__() + " = " + self.rexpr.__str__()


class ClassDeclarationCommand(Instruction):

    def __init__(self, className, attributes):
        self.className = className  # Class name as a string
        self.attributes = attributes  # List of AssignmentCommand objects

    def __str__(self):
        attr_str = "\n    ".join(str(attr) for attr in self.attributes)
        return f"class {self.className} {{\n    {attr_str if attr_str else '    // No attributes'}\n}}"


class ConditionCommand(Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return self.cond.__str__()

# Not Implemented Yet.


class AssertCommand(Instruction):
    def __init__(self, condition):
        self.cond = condition

    def __str__(self):
        return self.cond.__str__()


class MoveCommand(Instruction):
    def __init__(self, motion, expr):
        self.direction = motion
        self.expr = expr

    def __str__(self):
        return self.direction + " " + self.expr.__str__()


class PenCommand(Instruction):
    def __init__(self, penstat):
        self.status = penstat

    def __str__(self):
        return self.status


class GotoCommand(Instruction):
    def __init__(self, x, y):
        self.xcor = x
        self.ycor = y

    def __str__(self):
        return "goto " + str(self.xcor) + " " + str(self.ycor)


class NoOpCommand(Instruction):
    def __init__(self):
        pass

    def __str__(self):
        return "NOP"


class PauseCommand(Instruction):
    def __init__(self):
        pass

    def __str__(self):
        return "pause"


class FunctionDeclarationCommand(Instruction):
    def __init__(self, fname, params=None, body=None):
        self.name = fname
        self.params = params if params is not None else []
        self.body = body if body is not None else []

    def __str__(self):
        params_str = ", ".join(self.params)
        body_str = "\n    ".join(str(stmt) for stmt in self.body)
        return f"def {self.name}({params_str}):\n    {body_str}"


class FunctionCallCommand(Instruction):
    def __init__(self, fname, arguments=None):
        self.name = fname
        self.args = arguments if arguments is not None else []

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"


class ReturnCommand(Instruction):
    def __init__(self, numParams):
        self.numParams = numParams

    def __str__(self):
        return f"return {self.numParams}"


class ParametersPassingCommand(Instruction):
    def __init__(self, parameters):
        self.params = parameters

    def __str__(self):
        return ", ".join(str(param) for param in self.params)


class Expression(AST):
    pass

# --Arithmetic Expressions--------------------------------------------


class ArithExpr(Expression):
    pass


class BinArithOp(ArithExpr):
    def __init__(self, expr1, expr2, opsymbol):
        self.lexpr = expr1
        self.rexpr = expr2
        self.symbol = opsymbol

    def __str__(self):
        return "(" + self.lexpr.__str__() + " " + self.symbol + " " + self.rexpr.__str__() + ")"


class UnaryArithOp(ArithExpr):
    def __init__(self, expr1, opsymbol):
        self.expr = expr1
        self.symbol = opsymbol

    def __str__(self):
        return self.symbol + self.expr.__str__()


class UMinus(UnaryArithOp):
    def __init__(self, lexpr):
        super().__init__(lexpr, "-")


class Sum(BinArithOp):
    def __init__(self, lexpr, rexpr):
        super().__init__(lexpr, rexpr, "+")


class Diff(BinArithOp):
    def __init__(self, lexpr, rexpr):
        super().__init__(lexpr, rexpr, "-")


class Mult(BinArithOp):
    def __init__(self, lexpr, rexpr):
        super().__init__(lexpr, rexpr, "*")


class Div(BinArithOp):
    def __init__(self, lexpr, rexpr):
        super().__init__(lexpr, rexpr, "/")


# --Boolean Expressions-----------------------------------------------

class BoolExpr(Expression):
    pass


class BinCondOp(BoolExpr):
    def __init__(self, expr1, expr2, opsymbol):
        self.lexpr = expr1
        self.rexpr = expr2
        self.symbol = opsymbol

    def __str__(self):
        return "(" + self.lexpr.__str__() + ' ' + self.symbol + ' ' + self.rexpr.__str__() + ")"


class AND(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, "and")


class OR(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, "or")


class LT(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, "<")


class GT(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, ">")


class LTE(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, "<=")


class GTE(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, ">=")


class EQ(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, "==")


class NEQ(BinCondOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, "!=")


class NOT(BoolExpr):
    def __init__(self, uexpr):
        self.expr = uexpr
        self.symbol = "not"

    def __str__(self):
        return self.symbol + self.expr.__str__()


class PenStatus(BoolExpr):
    def __init__(self):
        pass

    def __str__(self):
        return "pendown?"


class BoolTrue(BoolExpr):
    def __init__(self):
        pass

    def __str__(self):
        return "True"


class BoolFalse(BoolExpr):
    def __init__(self):
        pass

    def __str__(self):
        return "False"


class Value(Expression):
    pass


class Num(Value):
    def __init__(self, v):
        self.val = int(v)

    def __str__(self):
        return str(self.val)


class Var(Value):
    def __init__(self, vname):
        self.varname = vname

    def __str__(self):
        return self.varname


class Array(Value):
    def __init__(self, vname):
        self.arr = vname

    def __str__(self):
        return self.arr

# class ArrayAccess(Value):
#     def __init__(self, var, index):
#         self.var = var
#         self.idx = index

#     def __str__(self):
#         indices_str = "".join(f"[{idx}]" for idx in self.idx)  # Format multiple indices
#         return f"{self.var}{indices_str}"
#     #     return self.var.__str__() + "[" + self.idx.__str__() + "]"


class ObjectOrArrayAccess(Value):
    def __init__(self, var, accesses):
        self.var = var
        self.accesses = accesses  # List of attribute names or indices

    def __str__(self):
        result = self.var
        for access in self.accesses:
            if isinstance(access, list):  # Array indexing
                indices_str = "".join(f"[{idx}]" for idx in access)
                result += indices_str
            else:  # Object attribute access
                result += f".{access}"
        return result


class ObjectInstantiationCommand(Instruction):
    def __init__(self, target, class_name):
        self.target = target  # Variable name or Object/Array Access
        self.class_name = class_name  # The class being instantiated

    def __str__(self):
        return f"{self.target} = new {self.class_name}()"
