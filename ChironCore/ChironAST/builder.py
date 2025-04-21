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
        self.repeatInstrCount = 0           # Counter for 'repeat' instructions
        self.stmtList = []                  # Final list of all executable statements
        # Temporary list of sub-statements generated for expression breakdown
        self.subStmtList = []
        # Counter for naming virtual registers used during code synthesis
        self.virtualRegCount = 0
        # Holds the name of the current class context being compiled
        self.classRegister = None

    def visitLvalue(self, ctx: tlangParser.LvalueContext):
        if ctx.VAR():
            if isinstance(ctx.VAR(), list):
                return ChironAST.Var(ctx.VAR()[0].getText())
            return ChironAST.Var(ctx.VAR().getText())
        elif ctx.dataLocationAccess():
            return self.visitDataLocationAccess(ctx.dataLocationAccess())

    def visitStart(self, ctx: tlangParser.StartContext):
        """Entry point for visiting the parse tree. Returns the synthesized statement list."""
        self.visit(ctx.statement_list())
        return self.stmtList

    def visitStatement_list(self, ctx: tlangParser.Statement_listContext):
        self.stmtList.extend(self.visit(ctx.declaration_list()))
        self.stmtList.extend(self.visit(ctx.strict_ilist()))

    def processInstructionBlock(self, items):
        """
        Shared utility for processing declaration or instruction blocks.
        Appends the resulting instructions and sub-statements to the main statement list.
        """
        stmtList = []
        for item in items:
            currStmtList = self.visit(item)
            if not isinstance(currStmtList,list): 
                currStmtList=[]
            stmtList.extend(self.subStmtList + currStmtList)
            self.subStmtList = []
            self.virtualRegCount = 0
        return stmtList

    def visitDeclaration_list(self, ctx: tlangParser.Declaration_listContext):
        return self.processInstructionBlock(ctx.declaration())

    def visitStrict_ilist(self, ctx: tlangParser.Strict_ilistContext):
        return self.processInstructionBlock(ctx.instruction())

    def visitFunctionDeclaration(self, ctx: tlangParser.FunctionDeclarationContext):
        # address(pc) of method will be registered in the interpreter against the key of the form ":className@methodName"
        if self.classRegister is not None:
            functionName = ":" + self.classRegister + "@" + ctx.NAME().getText()
        else:
            functionName = ctx.NAME().getText()
        functionParams = [param.getText() for param in ctx.parameters(
        ).VAR()] if ctx.parameters() is not None else None
        functionBody = self.visit(ctx.strict_ilist())
        # function compilation generated two extra statements apart from the function body
        # 1. function declaration - This command is used to register the address(pc) of the function in the interpreter
        #                           against the function name
        # 2. parameters passing - This command is used to push the parameters to the function on the call stack
        return [(ChironAST.FunctionDeclarationCommand(functionName, functionParams, functionBody), len(functionBody) + 2)] + [(ChironAST.ParametersPassingCommand(functionParams), 1)] + functionBody


    def visitReturnStatement(self, ctx: tlangParser.ReturnStatementContext):
        returnValues = [self.visit(expr) for expr in ctx.expression(
        )] if ctx.expression() is not None else None
        return [(ChironAST.ReturnCommand(returnValues), 1)]

    def visitAssignment(self, ctx: tlangParser.AssignmentContext):
        lval = self.visit(ctx.lvalue())
        rval = self.visit(ctx.expression())
        return [(ChironAST.AssignmentCommand(lval, rval), 1)]

    def visitDataLocationAccess(self, ctx: tlangParser.DataLocationAccessContext):

        

        base=ctx.baseVar().VAR().getText()
       
        # Traverse through the nested access ('.' for attributes, '[]' for indices)
        access_chain = []
        i = 1  # Start from second child (skip baseVar)
        while i < len(ctx.children):
            child = ctx.children[i]
            if isinstance(child, TerminalNodeImpl) and child.getText() == '.':
                # Next child must be a VAR (attribute access)
                i += 1  # Move to VAR
                access = ctx.children[i].getText()
                # Handle private attributes
                # If the access is with ":self" and the attribute is private, mangle the name 
                if base == ":self" and i == 2 and ctx.children[i].getText().startswith(":__"):
                    access = f":_{self.classRegister}{access.replace(':', '')}"
                access_chain.append(access)
            elif child.getText() == '[':
                # Array access: Process the expression inside `[]`
                i += 1  # Move to expression inside brackets
                # Visit and evaluate expression
                expr = self.visit(ctx.children[i])
                access_chain.append([expr])  # Store index as a list
                i += 1  # Skip closing ']'
            i += 1  # Move to the next child
        return ChironAST.DataLocationAccess(base, access_chain)

    def visitMethodCaller(self, ctx: tlangParser.MethodCallerContext):

        if ctx.dataLocationAccess():
            return self.visit(ctx.dataLocationAccess())
        if ctx.VAR():
            var=ctx.VAR().getText()
            return ChironAST.DataLocationAccess(var, [])
        return None 
        # access_chain = []
        # i = 0
        # while i < len(ctx.children):
        #     child = ctx.children[i]
        #     if isinstance(child, TerminalNodeImpl):
        #         # Current child must be a VAR (attribute access)
        #         access_chain.append(ctx.children[i].getText())
        #         i += 1  # skip '.'
        #     elif child.getText() == '[':
        #         # Array access: Process the expression inside `[]`
        #         i += 1  # Move to expression inside brackets
        #         # Visit and evaluate expression
        #         expr = self.visit(ctx.children[i])
        #         access_chain.append([expr.val])  # Store index as a list
        #         i += 2  # Skip closing ']'
        #     i += 1  # Move to the next child
        # return ChironAST.MethodCaller(access_chain)


    def visitObjectInstantiation(self, ctx: tlangParser.ObjectInstantiationContext):
        # Extract the left-hand side (target variable or object access)
        lval = self.visit(ctx.lvalue())
        # Extract the class name
        # The last VAR is the class being instantiated
        class_name = ctx.VAR().getText()
        return [(ChironAST.ObjectInstantiationCommand(lval, class_name), 1)]

    def visitClassDeclaration(self, ctx: tlangParser.ClassDeclarationContext):
        className = ctx.VAR()[0].getText()
        self.classRegister = className.replace(":", "")
        baseClasses = [var.getText() for var in ctx.VAR()[1:]] if len(
            ctx.VAR()) > 1 else None  # Extract base classes
        attributes = []
        # attributes which are object instantiations
        objectAttributes = []
        methods = []
        if ctx.classBody():
            for attrDecl in ctx.classBody().classAttributeDeclaration():
                if isinstance(attrDecl.assignment(), tlangParser.AssignmentContext):
                    assign_instr = self.visitAssignment(attrDecl.assignment())
                    attributes.extend(assign_instr)
                if isinstance(attrDecl.objectInstantiation(), tlangParser.ObjectInstantiationContext):
                    objectAttributes.extend(self.visitObjectInstantiation(
                        attrDecl.objectInstantiation()))
            for methodCtx in ctx.classBody().functionDeclaration():
                methods.extend(self.visitFunctionDeclaration(
                    methodCtx))
        self.classRegister = None # Reset class register
        # compiling class declaration generates one extra statement apart from the class body
        # 1. class declaration - This command is used to register the class as a python class(along with its attributes) in the interpreter
        return [(ChironAST.ClassDeclarationCommand(className, baseClasses, attributes, objectAttributes), 1)] + methods

    def visitValue(self, ctx: tlangParser.ValueContext):
        if ctx.NUM():
            return ChironAST.Num(ctx.NUM().getText())
        if ctx.REAL():
            return ChironAST.Real(ctx.REAL().getText())
        elif ctx.VAR():
            return ChironAST.Var(ctx.VAR().getText())
        elif ctx.array():
            return ChironAST.Array(ctx.array().getText())
        elif ctx.dataLocationAccess():
            return self.visitDataLocationAccess(ctx.dataLocationAccess())
        elif ctx.functionCall():
            return self.visitFunctionCallExpr(ctx.functionCall())
    

    def visitFunctionCallExpr(self, ctx: tlangParser.FunctionCallContext):
        # TODO: Refactoring, this function has similar body as visitFunctionCall

        functionName = ctx.NAME().getText()

        # the object invoking the method, in case the function call is a method call
        methodCaller = self.visitMethodCaller(
            ctx.methodCaller()) if ctx.methodCaller().children is not None else None

        
        functionArgs = [self.visit(arg) for arg in ctx.arguments(
        ).expression()] if ctx.arguments() is not None else []
        # if the function is a method call, insert the caller object as the first argument (self)
        if methodCaller:
            functionArgs.insert(0, methodCaller)
            # call private methods with mangled names
            # eg, :self.__privateMethod() will be called as :self._className__privateMethod()
            # if len(methodCaller.access_chain) == 1 and methodCaller.access_chain[0] == ":self" and functionName.startswith("__"):
            #     functionName = f"_{self.classRegister}{functionName}"
            if  methodCaller.var == ":self" and functionName.startswith("__"):
                functionName = f"_{self.classRegister}{functionName}"
        # create a virtual register to store the return value
        returnLocation = ChironAST.Var(":__reg_" + str(self.virtualRegCount))
        self.virtualRegCount += 1
        self.subStmtList.extend([(ChironAST.FunctionCallCommand(functionName, functionArgs,
                         methodCaller), 1)] + [(ChironAST.ReadReturnCommand([returnLocation]), 1)])
  
        return returnLocation
    
    def visitFunctionCall(self, ctx:tlangParser.FunctionCallContext):
        return self.visitFunctionCallExpr(ctx)

    
    def visitAssignExpr(self, ctx: tlangParser.AssignExprContext):
        lval = self.visit(ctx.lvalue())
        rval = self.visit(ctx.expression())

        self.subStmtList.extend([(ChironAST.AssignmentCommand(lval, rval), 1)])
        return lval

    def visitPrintStatement(self, ctx: tlangParser.PrintStatementContext):
        expr_value = self.visit(ctx.expression())  # Evaluate the expression
        # Return value in case it's used elsewhere
        return [(ChironAST.PrintCommand(expr_value), 1)]

    def visitIfConditional(self, ctx: tlangParser.IfConditionalContext):
        condObj = ChironAST.ConditionCommand(self.visit(ctx.expression()))
        if self.subStmtList:
            self.stmtList.extend(self.subStmtList)
            self.subStmtList=[]
        thenInstrList = self.visit(ctx.strict_ilist())
        return [(condObj, len(thenInstrList) + 1)] + thenInstrList

    def visitIfElseConditional(self, ctx: tlangParser.IfElseConditionalContext):
        condObj = ChironAST.ConditionCommand(self.visit(ctx.expression()))
        if self.subStmtList:
            self.stmtList.extend(self.subStmtList)
            self.subStmtList=[]
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
    
    def visitNotExpr(self, ctx: tlangParser.NotExprContext):
        expr1 = self.visit(ctx.condition(0))
        return ChironAST.NOT(expr1)
    
    def visitBinExpr(self, ctx: tlangParser.BinExprContext):
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
    
    def visitLogExpr(self, ctx: tlangParser.LogExprContext):
        expr1 = self.visit(ctx.expression(0))
        expr2 = self.visit(ctx.expression(1))
        logicOpCtx = ctx.logicOp()

        if logicOpCtx.AND():
            return ChironAST.AND(expr1, expr2)
        elif logicOpCtx.OR():
            return ChironAST.OR(expr1, expr2)
    
    def visitPenExpr(self, ctx: tlangParser.PenExprContext):
        return ChironAST.PenStatus()



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

        thenInstrList = self.visit(ctx.strict_ilist())


        boolFalse = ChironAST.ConditionCommand(ChironAST.BoolFalse())
        return [(counterVarInitInstr, 1), (loopCond, len(thenInstrList) + 3)] + thenInstrList +\
            [(counterVarDecrInstr, 1), (boolFalse, -len(thenInstrList) - 2)]

    def visitMoveCommand(self, ctx: tlangParser.MoveCommandContext):
        mvcommand = ctx.moveOp().getText()
        mvexpr = self.visit(ctx.expression())
        return [(ChironAST.MoveCommand(mvcommand, mvexpr), 1)]

    def visitPenCommand(self, ctx: tlangParser.PenCommandContext):
        return [(ChironAST.PenCommand(ctx.getText()), 1)]
