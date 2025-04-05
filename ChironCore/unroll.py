#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ChironLang Abstract Syntax Tree Builder
from turtparse.tlangParser import tlangParser
from turtparse.tlangVisitor import tlangVisitor

class UnrollLoops(tlangVisitor):
    def __init__(self, bound):
        self.bound = bound
        self.repeatVariablesCounter = 0

    def visitStart(self, ctx:tlangParser.StartContext):
        stmtList = self.visit(ctx.instruction_list())
        return stmtList

    def visitInstruction_list(self, ctx:tlangParser.Instruction_listContext):
        code = ""
        for instr in ctx.instruction():
           code += self.visit(instr) + "\n" 

        return code

    def visitStrict_ilist(self, ctx:tlangParser.Strict_ilistContext):
        code = ""
        for instr in ctx.instruction():
            code += self.visit(instr) + "\n"

        return code


    def visitAssignment(self, ctx:tlangParser.AssignmentContext):
        return ctx.getText()

    def visitIfConditional(self, ctx:tlangParser.IfConditionalContext):
        condition = self.visit(ctx.condition())
        ifBlock = self.visit(ctx.strict_ilist())
        return "if (" + condition + ") [\n" + ifBlock + "\n]"

    def visitIfElseConditional(self, ctx:tlangParser.IfElseConditionalContext):
        condition = self.visit(ctx.condition())
        ifBlock = self.visit(ctx.strict_ilist(0))
        elseBlock = self.visit(ctx.strict_ilist(1))
        return "if (" + condition + ") [\n" + ifBlock + "\n] else [\n" + elseBlock + "\n]"

    def visitGotoCommand(self, ctx:tlangParser.GotoCommandContext):
        xcor = self.visit(ctx.expression(0))
        ycor = self.visit(ctx.expression(1))
        return "goto (" + xcor + ", " + ycor + ")"

    # Visit a parse tree produced by tlangParser#unaryExpr.
    def visitUnaryExpr(self, ctx:tlangParser.UnaryExprContext):
        return ctx.getText()

    # Visit a parse tree produced by tlangParser#addExpr.
    def visitAddExpr(self, ctx:tlangParser.AddExprContext):
        return ctx.getText()

    # Visit a parse tree produced by tlangParser#mulExpr.
    def visitMulExpr(self, ctx:tlangParser.MulExprContext):
        return ctx.getText()

    # Visit a parse tree produced by tlangParser#valueExpr.
    def visitModExpr(self, ctx:tlangParser.ModExprContext):
        return ctx.getText()

    # Visit a parse tree produced by tlangParser#parenExpr.
    def visitParenExpr(self, ctx:tlangParser.ParenExprContext):
        return ctx.getText()

    def visitCondition(self, ctx:tlangParser.ConditionContext):
        return ctx.getText()

    def visitValue(self, ctx:tlangParser.ValueContext):
        return ctx.getText()

    def visitLoop(self, ctx:tlangParser.LoopContext):
        repeatCount = self.visit(ctx.value())
        loopBlock = self.visit(ctx.strict_ilist())
        code = ""
        if (repeatCount[0] != ":"):
            # constant number of iterations
            code += "assume " + str(repeatCount) + " <= " + str(self.bound) +"\n"
            for i in range(min(int(repeatCount), self.bound)):
                code += loopBlock + "\n"
        else:
            # variable number of iterations
            repeatVariable = ":_repeat" + str(self.repeatVariablesCounter)
            code += repeatVariable + " = " + repeatCount + "\n"
            code += "assume " + repeatVariable + " <= " + str(self.bound) +" \n"
            for i in range(self.bound):
                code += "if (" + repeatVariable + " > " + str(i) + ") [\n" + loopBlock + "\n]\n"
            self.repeatVariablesCounter += 1

        return code

    def visitMoveCommand(self, ctx:tlangParser.MoveCommandContext):
        return ctx.getText()

    def visitPenCommand(self, ctx:tlangParser.PenCommandContext):
        return ctx.getText()

    def visitAssertionCommand(self, ctx:tlangParser.AssertionCommandContext):
        return ctx.getText()

    def visitAssumeCommand(self, ctx:tlangParser.AssumeCommandContext):
        return ctx.getText()

