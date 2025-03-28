
// Generated from tlang.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "tlangParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by tlangParser.
 */
class  tlangVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by tlangParser.
   */
    virtual std::any visitStart(tlangParser::StartContext *context) = 0;

    virtual std::any visitInstruction_list(tlangParser::Instruction_listContext *context) = 0;

    virtual std::any visitStrict_ilist(tlangParser::Strict_ilistContext *context) = 0;

    virtual std::any visitFunction_list(tlangParser::Function_listContext *context) = 0;

    virtual std::any visitFunction_declaration(tlangParser::Function_declarationContext *context) = 0;

    virtual std::any visitVoidFunction(tlangParser::VoidFunctionContext *context) = 0;

    virtual std::any visitValueFunction(tlangParser::ValueFunctionContext *context) = 0;

    virtual std::any visitVoidReturn(tlangParser::VoidReturnContext *context) = 0;

    virtual std::any visitValueReturn(tlangParser::ValueReturnContext *context) = 0;

    virtual std::any visitParametersDeclaration(tlangParser::ParametersDeclarationContext *context) = 0;

    virtual std::any visitParameterCall(tlangParser::ParameterCallContext *context) = 0;

    virtual std::any visitVoidFuncCall(tlangParser::VoidFuncCallContext *context) = 0;

    virtual std::any visitValueFuncCall(tlangParser::ValueFuncCallContext *context) = 0;

    virtual std::any visitInstruction(tlangParser::InstructionContext *context) = 0;

    virtual std::any visitConditional(tlangParser::ConditionalContext *context) = 0;

    virtual std::any visitIfConditional(tlangParser::IfConditionalContext *context) = 0;

    virtual std::any visitIfElseConditional(tlangParser::IfElseConditionalContext *context) = 0;

    virtual std::any visitLoop(tlangParser::LoopContext *context) = 0;

    virtual std::any visitGotoCommand(tlangParser::GotoCommandContext *context) = 0;

    virtual std::any visitAssignment(tlangParser::AssignmentContext *context) = 0;

    virtual std::any visitMoveCommand(tlangParser::MoveCommandContext *context) = 0;

    virtual std::any visitMoveOp(tlangParser::MoveOpContext *context) = 0;

    virtual std::any visitPenCommand(tlangParser::PenCommandContext *context) = 0;

    virtual std::any visitPauseCommand(tlangParser::PauseCommandContext *context) = 0;

    virtual std::any visitUnaryExpr(tlangParser::UnaryExprContext *context) = 0;

    virtual std::any visitValueExpr(tlangParser::ValueExprContext *context) = 0;

    virtual std::any visitFuncExpr(tlangParser::FuncExprContext *context) = 0;

    virtual std::any visitAddExpr(tlangParser::AddExprContext *context) = 0;

    virtual std::any visitMulExpr(tlangParser::MulExprContext *context) = 0;

    virtual std::any visitParenExpr(tlangParser::ParenExprContext *context) = 0;

    virtual std::any visitMultiplicative(tlangParser::MultiplicativeContext *context) = 0;

    virtual std::any visitAdditive(tlangParser::AdditiveContext *context) = 0;

    virtual std::any visitUnaryArithOp(tlangParser::UnaryArithOpContext *context) = 0;

    virtual std::any visitCondition(tlangParser::ConditionContext *context) = 0;

    virtual std::any visitBinCondOp(tlangParser::BinCondOpContext *context) = 0;

    virtual std::any visitLogicOp(tlangParser::LogicOpContext *context) = 0;

    virtual std::any visitValue(tlangParser::ValueContext *context) = 0;


};

