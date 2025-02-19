#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ChironLang Abstract Syntax Tree Builder

from ChironAST import ChironAST
from antlr4.tree.Tree import TerminalNodeImpl  # Import TerminalNodeImpl
from turtparse.tlangVisitor import tlangVisitor
from turtparse.tlangParser import tlangParser
import os
import sys
sys.path.insert(0, os.path.join("..", "turtparse"))


class astGenPass(tlangVisitor):

    def __init__(self):
        self.repeatInstrCount = 0  # keeps count for no of 'repeat' instructions
        self.stmtList = []

    def getLval(self, ctx):

        if ctx.VAR():
            if isinstance(ctx.VAR(), list):
                return ChironAST.Var(ctx.VAR()[0].getText())
            return ChironAST.Var(ctx.VAR().getText())
        elif ctx.objectOrArrayAccess():
            return self.visitObjectOrArrayAccess(ctx.objectOrArrayAccess())

    def visitStart(self, ctx: tlangParser.StartContext):
        stmtList = self.visit(ctx.instruction_list())
        self.stmtList.extend(stmtList)
        return self.stmtList

    def visitInstruction_list(self, ctx: tlangParser.Instruction_listContext):
        instrList = []
        for instr in ctx.instruction():
            self.stmtList.extend(self.visit(instr))

        return []

    def visitStrict_ilist(self, ctx: tlangParser.Strict_ilistContext):
        # TODO: code refactoring. visitInstruction_list and visitStrict_ilist have same body
        instrList = []
        for instr in ctx.instruction():
            visvalue = self.visit(instr)
            instrList.extend(visvalue)

        return instrList
    
    def visitFunctionDeclaration(self, ctx: tlangParser.FunctionDeclarationContext):
        functionName = ctx.NAME().getText()
        functionParams = [ param.getText() for param in ctx.parameters().VAR() ] if ctx.parameters() is not None else None
        functionBody = self.visit(ctx.strict_ilist())
        numParams = 0 if functionParams is None else len(functionParams)
        return [(ChironAST.FunctionDeclarationCommand(functionName, functionParams, functionBody), len(functionBody) + 3)] + [(ChironAST.ParametersPassingCommand(functionParams), 1)] + functionBody + [(ChironAST.ReturnCommand(numParams), 1)]

    def visitFunctionCall(self, ctx: tlangParser.FunctionCallContext):
        functionName = ctx.NAME().getText()
        functionArgs = [ self.visit(arg) for arg in ctx.arguments().expression() ] if ctx.arguments() is not None else None
        return [(ChironAST.FunctionCallCommand(functionName, functionArgs), 1)]

    # computes list of recursive assign statements
    def visitAssignment(self, ctx: tlangParser.AssignmentContext):

        # print(ctx.VAR().getText(),ctx.expression().getText())
        lval = self.getLval(ctx)
        rval = self.visit(ctx.expression())
        # print(rval)
        if isinstance(rval, list):
            print(rval[-1][0])
            rvaln = rval[-1][0].lvar  # Get the last assigned variable as rval
            return rval + [(ChironAST.AssignmentCommand(lval, rvaln), 1)]

    # Otherwise, just return a normal assignment
        return [(ChironAST.AssignmentCommand(lval, rval), 1)]

    def visitObjectOrArrayAccess(self, ctx: tlangParser.ObjectOrArrayAccessContext):
        # Start with the base variable (first part of access)
        base = ctx.baseAccess().VAR().getText()

        # Traverse through the nested access ('.' for attributes, '[]' for indices)
        accesses = []
        i = 1  # Start from second child (skip baseAccess)

        while i < len(ctx.children):
            child = ctx.children[i]

            if isinstance(child, TerminalNodeImpl) and child.getText() == '.':
                # Next child must be a VAR (attribute access)
                i += 1  # Move to VAR
                accesses.append(ctx.children[i].getText())

            elif child.getText() == '[':
                # Array access: Process the expression inside `[]`
                i += 1  # Move to expression inside brackets
                # Visit and evaluate expression
                expr = self.visit(ctx.children[i])
                accesses.append([expr.val])  # Store index as a list

                i += 1  # Skip closing ']'

            i += 1  # Move to the next child

        return ChironAST.ObjectOrArrayAccess(base, accesses)

    def visitObjectInstantiation(self, ctx: tlangParser.ObjectInstantiationContext):
        # Extract the left-hand side (target variable or object access)
        lval = self.getLval(ctx)
        # Extract the class name
        # The last VAR is the class being instantiated
        class_name = ctx.VAR()[-1].getText()

        return [(ChironAST.ObjectInstantiationCommand(lval, class_name), 1)]

    def visitClassDeclaration(self, ctx: tlangParser.ClassDeclarationContext):
        className = ctx.VAR().getText()  # Extract class name

        attributes = []
        if ctx.classBody():
            for attrDecl in ctx.classBody().classAttributeDeclaration():
                assign_list = self.visitAssignment(attrDecl.assignment())
                attributes.extend(assign_list)

        print(className, attributes)

        return [(ChironAST.ClassDeclarationCommand(className, attributes), 1)]

    # def visitArrayAccess(self, ctx:tlangParser.ArrayAccessContext):
    #     var = ctx.VAR().getText()
    #     indices = [self.visit(expr).val for expr in ctx.expression()]  # Visit all expressions in []

    #     # print(var, indices, "Inside multi-dimensional array access")

    #     return ChironAST.ArrayAccess(var, indices)  # Return an object handling multiple indices

    def visitValue(self, ctx: tlangParser.ValueContext):
        if ctx.NUM():
            return ChironAST.Num(ctx.NUM().getText())
        elif ctx.VAR():
            return ChironAST.Var(ctx.VAR().getText())
        elif ctx.array():
            return ChironAST.Array(ctx.array().getText())
        elif ctx.objectOrArrayAccess():
            print("entering heaven")
            return self.visitObjectOrArrayAccess(ctx.objectOrArrayAccess())

    def visitAssignExpr(self, ctx: tlangParser.AssignExprContext):

        print("Assignment Expr")

        list = self.visitAssignment(ctx)
        self.stmtList.extend(list)

        return list[-1][0].lvar

        # return "("+ ChironAST.AssignmentCommand(lval, rval) + ")"
        # return   # Calls visitAssignment

    def visitPrintStatement(self, ctx: tlangParser.PrintStatementContext):
        expr_value = self.visit(ctx.expression())  # Evaluate the expression
        # Return value in case it's used elsewhere
        return [(ChironAST.PrintCommand(expr_value), 1)]

    def visitIfConditional(self, ctx: tlangParser.IfConditionalContext):
        condObj = ChironAST.ConditionCommand(self.visit(ctx.condition()))
        thenInstrList = self.visit(ctx.strict_ilist())
        return [(condObj, len(thenInstrList) + 1)] + thenInstrList

    def visitIfElseConditional(self, ctx: tlangParser.IfElseConditionalContext):
        condObj = ChironAST.ConditionCommand(self.visit(ctx.condition()))
        thenInstrList = self.visit(ctx.strict_ilist(0))
        elseInstrList = self.visit(ctx.strict_ilist(1))
        jumpOverElseBlock = [(ChironAST.ConditionCommand(
            ChironAST.BoolFalse()), len(elseInstrList) + 1)]
        return [(condObj, len(thenInstrList) + 2)] + thenInstrList + jumpOverElseBlock + elseInstrList

    def visitGotoCommand(self, ctx: tlangParser.GotoCommandContext):
        xcor = self.visit(ctx.expression(0))
        ycor = self.visit(ctx.expression(1))
        return [(ChironAST.GotoCommand(xcor, ycor), 1)]

    # Visit a parse tree produced by tlangParser#unaryExpr.
    def visitUnaryExpr(self, ctx: tlangParser.UnaryExprContext):
        expr1 = self.visit(ctx.expression())
        if ctx.unaryArithOp().MINUS():
            return ChironAST.UMinus(expr1)

        return self.visitChildren(ctx)

    # Visit a parse tree produced by tlangParser#addExpr.
    def visitAddExpr(self, ctx: tlangParser.AddExprContext):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if ctx.additive().PLUS():
            ext = ChironAST.Sum(left, right)
        elif ctx.additive().MINUS():
            ext = ChironAST.Diff(left, right)
        return ext

    # Visit a parse tree produced by tlangParser#mulExpr.
    def visitMulExpr(self, ctx: tlangParser.MulExprContext):
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))
        if ctx.multiplicative().MUL():
            return ChironAST.Mult(left, right)
        elif ctx.multiplicative().DIV():
            return ChironAST.Div(left, right)

    # Visit a parse tree produced by tlangParser#parenExpr.
    def visitParenExpr(self, ctx: tlangParser.ParenExprContext):
        return self.visit(ctx.expression())

    def visitCondition(self, ctx: tlangParser.ConditionContext):
        if ctx.PENCOND():
            return ChironAST.PenStatus()

        if ctx.NOT():
            expr1 = self.visit(ctx.condition(0))
            return ChironAST.NOT(expr1)

        if ctx.logicOp():
            expr1 = self.visit(ctx.condition(0))
            expr2 = self.visit(ctx.condition(1))
            logicOpCtx = ctx.logicOp()

            if logicOpCtx.AND():
                return ChironAST.AND(expr1, expr2)
            elif logicOpCtx.OR():
                return ChironAST.OR(expr1, expr2)

        if ctx.binCondOp():
            expr1 = self.visit(ctx.expression(0))
            expr2 = self.visit(ctx.expression(1))
            binOpCtx = ctx.binCondOp()

            if binOpCtx.LT():
                return ChironAST.LT(expr1, expr2)
            elif binOpCtx.GT():
                return ChironAST.GT(expr1, expr2)
            elif binOpCtx.EQ():
                return ChironAST.EQ(expr1, expr2)
            elif binOpCtx.NEQ():
                return ChironAST.NEQ(expr1, expr2)
            elif binOpCtx.LTE():
                return ChironAST.LTE(expr1, expr2)
            elif binOpCtx.GTE():
                return ChironAST.GTE(expr1, expr2)

        if ctx.condition():
            # condition is inside paranthesis
            return self.visit(ctx.condition(0))

        return self.visitChildren(ctx)

    def visitLoop(self, ctx: tlangParser.LoopContext):
        # insert counter variable in IR for tracking repeat count
        self.repeatInstrCount += 1
        repeatNum = self.visit(ctx.value())
        counterVar = ChironAST.Var(
            ":__rep_counter_" + str(self.repeatInstrCount))
        counterVarInitInstr = ChironAST.AssignmentCommand(
            counterVar, repeatNum)
        constZero = ChironAST.Num(0)
        constOne = ChironAST.Num(1)
        loopCond = ChironAST.ConditionCommand(
            ChironAST.GT(counterVar, constZero))
        counterVarDecrInstr = ChironAST.AssignmentCommand(
            counterVar, ChironAST.Diff(counterVar, constOne))

        thenInstrList = []
        for instr in ctx.strict_ilist().instruction():
            temp = self.visit(instr)
            thenInstrList.extend(temp)

        boolFalse = ChironAST.ConditionCommand(ChironAST.BoolFalse())
        return [(counterVarInitInstr, 1), (loopCond, len(thenInstrList) + 3)] + thenInstrList +\
            [(counterVarDecrInstr, 1), (boolFalse, -len(thenInstrList) - 2)]

    def visitMoveCommand(self, ctx: tlangParser.MoveCommandContext):
        mvcommand = ctx.moveOp().getText()
        mvexpr = self.visit(ctx.expression())
        return [(ChironAST.MoveCommand(mvcommand, mvexpr), 1)]

    def visitPenCommand(self, ctx: tlangParser.PenCommandContext):
        return [(ChironAST.PenCommand(ctx.getText()), 1)]
