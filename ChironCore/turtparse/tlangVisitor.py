# Generated from tlang.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .tlangParser import tlangParser
else:
    from tlangParser import tlangParser

# This class defines a complete generic visitor for a parse tree produced by tlangParser.

class tlangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by tlangParser#start.
    def visitStart(self, ctx:tlangParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#instruction_list.
    def visitInstruction_list(self, ctx:tlangParser.Instruction_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#strict_ilist.
    def visitStrict_ilist(self, ctx:tlangParser.Strict_ilistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#instruction.
    def visitInstruction(self, ctx:tlangParser.InstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#conditional.
    def visitConditional(self, ctx:tlangParser.ConditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#ifConditional.
    def visitIfConditional(self, ctx:tlangParser.IfConditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#ifElseConditional.
    def visitIfElseConditional(self, ctx:tlangParser.IfElseConditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#loop.
    def visitLoop(self, ctx:tlangParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#gotoCommand.
    def visitGotoCommand(self, ctx:tlangParser.GotoCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#assignment.
    def visitAssignment(self, ctx:tlangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#moveCommand.
    def visitMoveCommand(self, ctx:tlangParser.MoveCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#moveOp.
    def visitMoveOp(self, ctx:tlangParser.MoveOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#penCommand.
    def visitPenCommand(self, ctx:tlangParser.PenCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#pauseCommand.
    def visitPauseCommand(self, ctx:tlangParser.PauseCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#expression.
    def visitExpression(self, ctx:tlangParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#binArithOp.
    def visitBinArithOp(self, ctx:tlangParser.BinArithOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#unaryArithOp.
    def visitUnaryArithOp(self, ctx:tlangParser.UnaryArithOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#condition.
    def visitCondition(self, ctx:tlangParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#binCondOp.
    def visitBinCondOp(self, ctx:tlangParser.BinCondOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#logicOp.
    def visitLogicOp(self, ctx:tlangParser.LogicOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tlangParser#value.
    def visitValue(self, ctx:tlangParser.ValueContext):
        return self.visitChildren(ctx)



del tlangParser