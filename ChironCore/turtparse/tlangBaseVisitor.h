
// Generated from tlang.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "tlangVisitor.h"


/**
 * This class provides an empty implementation of tlangVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  tlangBaseVisitor : public tlangVisitor {
public:

  virtual std::any visitStart(tlangParser::StartContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInstruction_list(tlangParser::Instruction_listContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStrict_ilist(tlangParser::Strict_ilistContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInstruction(tlangParser::InstructionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitConditional(tlangParser::ConditionalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIfConditional(tlangParser::IfConditionalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIfElseConditional(tlangParser::IfElseConditionalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLoop(tlangParser::LoopContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGotoCommand(tlangParser::GotoCommandContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAssignment(tlangParser::AssignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMoveCommand(tlangParser::MoveCommandContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMoveOp(tlangParser::MoveOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPenCommand(tlangParser::PenCommandContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPauseCommand(tlangParser::PauseCommandContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitUnaryExpr(tlangParser::UnaryExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitValueExpr(tlangParser::ValueExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAddExpr(tlangParser::AddExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMulExpr(tlangParser::MulExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParenExpr(tlangParser::ParenExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMultiplicative(tlangParser::MultiplicativeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAdditive(tlangParser::AdditiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitUnaryArithOp(tlangParser::UnaryArithOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCondition(tlangParser::ConditionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBinCondOp(tlangParser::BinCondOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLogicOp(tlangParser::LogicOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitValue(tlangParser::ValueContext *ctx) override {
    return visitChildren(ctx);
  }


};

