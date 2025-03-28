
// Generated from tlang.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  tlangParser : public antlr4::Parser {
public:
  enum {
    T__0 = 1, T__1 = 2, T__2 = 3, T__3 = 4, T__4 = 5, T__5 = 6, T__6 = 7, 
    T__7 = 8, T__8 = 9, T__9 = 10, T__10 = 11, T__11 = 12, T__12 = 13, T__13 = 14, 
    T__14 = 15, T__15 = 16, T__16 = 17, T__17 = 18, T__18 = 19, T__19 = 20, 
    T__20 = 21, T__21 = 22, T__22 = 23, T__23 = 24, T__24 = 25, PLUS = 26, 
    MINUS = 27, MUL = 28, DIV = 29, PENCOND = 30, LT = 31, GT = 32, EQ = 33, 
    NEQ = 34, LTE = 35, GTE = 36, AND = 37, OR = 38, NOT = 39, NUM = 40, 
    VAR = 41, NAME = 42, Whitespace = 43
  };

  enum {
    RuleStart = 0, RuleInstruction_list = 1, RuleStrict_ilist = 2, RuleFunction_list = 3, 
    RuleFunction_declaration = 4, RuleVoidFunction = 5, RuleValueFunction = 6, 
    RuleVoidReturn = 7, RuleValueReturn = 8, RuleParametersDeclaration = 9, 
    RuleParameterCall = 10, RuleVoidFuncCall = 11, RuleValueFuncCall = 12, 
    RuleInstruction = 13, RuleConditional = 14, RuleIfConditional = 15, 
    RuleIfElseConditional = 16, RuleLoop = 17, RuleGotoCommand = 18, RuleAssignment = 19, 
    RuleMoveCommand = 20, RuleMoveOp = 21, RulePenCommand = 22, RulePauseCommand = 23, 
    RuleExpression = 24, RuleMultiplicative = 25, RuleAdditive = 26, RuleUnaryArithOp = 27, 
    RuleCondition = 28, RuleBinCondOp = 29, RuleLogicOp = 30, RuleValue = 31
  };

  explicit tlangParser(antlr4::TokenStream *input);

  tlangParser(antlr4::TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options);

  ~tlangParser() override;

  std::string getGrammarFileName() const override;

  const antlr4::atn::ATN& getATN() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;


  class StartContext;
  class Instruction_listContext;
  class Strict_ilistContext;
  class Function_listContext;
  class Function_declarationContext;
  class VoidFunctionContext;
  class ValueFunctionContext;
  class VoidReturnContext;
  class ValueReturnContext;
  class ParametersDeclarationContext;
  class ParameterCallContext;
  class VoidFuncCallContext;
  class ValueFuncCallContext;
  class InstructionContext;
  class ConditionalContext;
  class IfConditionalContext;
  class IfElseConditionalContext;
  class LoopContext;
  class GotoCommandContext;
  class AssignmentContext;
  class MoveCommandContext;
  class MoveOpContext;
  class PenCommandContext;
  class PauseCommandContext;
  class ExpressionContext;
  class MultiplicativeContext;
  class AdditiveContext;
  class UnaryArithOpContext;
  class ConditionContext;
  class BinCondOpContext;
  class LogicOpContext;
  class ValueContext; 

  class  StartContext : public antlr4::ParserRuleContext {
  public:
    StartContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Function_listContext *function_list();
    Instruction_listContext *instruction_list();
    antlr4::tree::TerminalNode *EOF();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StartContext* start();

  class  Instruction_listContext : public antlr4::ParserRuleContext {
  public:
    Instruction_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<InstructionContext *> instruction();
    InstructionContext* instruction(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Instruction_listContext* instruction_list();

  class  Strict_ilistContext : public antlr4::ParserRuleContext {
  public:
    Strict_ilistContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<InstructionContext *> instruction();
    InstructionContext* instruction(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Strict_ilistContext* strict_ilist();

  class  Function_listContext : public antlr4::ParserRuleContext {
  public:
    Function_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Function_declarationContext *> function_declaration();
    Function_declarationContext* function_declaration(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Function_listContext* function_list();

  class  Function_declarationContext : public antlr4::ParserRuleContext {
  public:
    Function_declarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    VoidFunctionContext *voidFunction();
    ValueFunctionContext *valueFunction();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Function_declarationContext* function_declaration();

  class  VoidFunctionContext : public antlr4::ParserRuleContext {
  public:
    VoidFunctionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NAME();
    ParametersDeclarationContext *parametersDeclaration();
    Instruction_listContext *instruction_list();
    VoidReturnContext *voidReturn();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VoidFunctionContext* voidFunction();

  class  ValueFunctionContext : public antlr4::ParserRuleContext {
  public:
    ValueFunctionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NAME();
    ParametersDeclarationContext *parametersDeclaration();
    Instruction_listContext *instruction_list();
    ValueReturnContext *valueReturn();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ValueFunctionContext* valueFunction();

  class  VoidReturnContext : public antlr4::ParserRuleContext {
  public:
    VoidReturnContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VoidReturnContext* voidReturn();

  class  ValueReturnContext : public antlr4::ParserRuleContext {
  public:
    ValueReturnContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ValueContext *value();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ValueReturnContext* valueReturn();

  class  ParametersDeclarationContext : public antlr4::ParserRuleContext {
  public:
    ParametersDeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> VAR();
    antlr4::tree::TerminalNode* VAR(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ParametersDeclarationContext* parametersDeclaration();

  class  ParameterCallContext : public antlr4::ParserRuleContext {
  public:
    ParameterCallContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ParameterCallContext* parameterCall();

  class  VoidFuncCallContext : public antlr4::ParserRuleContext {
  public:
    VoidFuncCallContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NAME();
    ParameterCallContext *parameterCall();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  VoidFuncCallContext* voidFuncCall();

  class  ValueFuncCallContext : public antlr4::ParserRuleContext {
  public:
    ValueFuncCallContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NAME();
    ParameterCallContext *parameterCall();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ValueFuncCallContext* valueFuncCall();

  class  InstructionContext : public antlr4::ParserRuleContext {
  public:
    InstructionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AssignmentContext *assignment();
    ConditionalContext *conditional();
    LoopContext *loop();
    MoveCommandContext *moveCommand();
    PenCommandContext *penCommand();
    GotoCommandContext *gotoCommand();
    PauseCommandContext *pauseCommand();
    VoidFuncCallContext *voidFuncCall();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InstructionContext* instruction();

  class  ConditionalContext : public antlr4::ParserRuleContext {
  public:
    ConditionalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IfConditionalContext *ifConditional();
    IfElseConditionalContext *ifElseConditional();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConditionalContext* conditional();

  class  IfConditionalContext : public antlr4::ParserRuleContext {
  public:
    IfConditionalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ConditionContext *condition();
    Strict_ilistContext *strict_ilist();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IfConditionalContext* ifConditional();

  class  IfElseConditionalContext : public antlr4::ParserRuleContext {
  public:
    IfElseConditionalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ConditionContext *condition();
    std::vector<Strict_ilistContext *> strict_ilist();
    Strict_ilistContext* strict_ilist(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IfElseConditionalContext* ifElseConditional();

  class  LoopContext : public antlr4::ParserRuleContext {
  public:
    LoopContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ValueContext *value();
    Strict_ilistContext *strict_ilist();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LoopContext* loop();

  class  GotoCommandContext : public antlr4::ParserRuleContext {
  public:
    GotoCommandContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GotoCommandContext* gotoCommand();

  class  AssignmentContext : public antlr4::ParserRuleContext {
  public:
    AssignmentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *VAR();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AssignmentContext* assignment();

  class  MoveCommandContext : public antlr4::ParserRuleContext {
  public:
    MoveCommandContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    MoveOpContext *moveOp();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MoveCommandContext* moveCommand();

  class  MoveOpContext : public antlr4::ParserRuleContext {
  public:
    MoveOpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MoveOpContext* moveOp();

  class  PenCommandContext : public antlr4::ParserRuleContext {
  public:
    PenCommandContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PenCommandContext* penCommand();

  class  PauseCommandContext : public antlr4::ParserRuleContext {
  public:
    PauseCommandContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PauseCommandContext* pauseCommand();

  class  ExpressionContext : public antlr4::ParserRuleContext {
  public:
    ExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    ExpressionContext() = default;
    void copyFrom(ExpressionContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnaryExprContext : public ExpressionContext {
  public:
    UnaryExprContext(ExpressionContext *ctx);

    UnaryArithOpContext *unaryArithOp();
    ExpressionContext *expression();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ValueExprContext : public ExpressionContext {
  public:
    ValueExprContext(ExpressionContext *ctx);

    ValueContext *value();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  FuncExprContext : public ExpressionContext {
  public:
    FuncExprContext(ExpressionContext *ctx);

    ValueFuncCallContext *valueFuncCall();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  AddExprContext : public ExpressionContext {
  public:
    AddExprContext(ExpressionContext *ctx);

    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    AdditiveContext *additive();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  MulExprContext : public ExpressionContext {
  public:
    MulExprContext(ExpressionContext *ctx);

    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    MultiplicativeContext *multiplicative();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ParenExprContext : public ExpressionContext {
  public:
    ParenExprContext(ExpressionContext *ctx);

    ExpressionContext *expression();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  ExpressionContext* expression();
  ExpressionContext* expression(int precedence);
  class  MultiplicativeContext : public antlr4::ParserRuleContext {
  public:
    MultiplicativeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *MUL();
    antlr4::tree::TerminalNode *DIV();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MultiplicativeContext* multiplicative();

  class  AdditiveContext : public antlr4::ParserRuleContext {
  public:
    AdditiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *PLUS();
    antlr4::tree::TerminalNode *MINUS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AdditiveContext* additive();

  class  UnaryArithOpContext : public antlr4::ParserRuleContext {
  public:
    UnaryArithOpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *MINUS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UnaryArithOpContext* unaryArithOp();

  class  ConditionContext : public antlr4::ParserRuleContext {
  public:
    ConditionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NOT();
    std::vector<ConditionContext *> condition();
    ConditionContext* condition(size_t i);
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    BinCondOpContext *binCondOp();
    antlr4::tree::TerminalNode *PENCOND();
    LogicOpContext *logicOp();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConditionContext* condition();
  ConditionContext* condition(int precedence);
  class  BinCondOpContext : public antlr4::ParserRuleContext {
  public:
    BinCondOpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EQ();
    antlr4::tree::TerminalNode *NEQ();
    antlr4::tree::TerminalNode *LT();
    antlr4::tree::TerminalNode *GT();
    antlr4::tree::TerminalNode *LTE();
    antlr4::tree::TerminalNode *GTE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BinCondOpContext* binCondOp();

  class  LogicOpContext : public antlr4::ParserRuleContext {
  public:
    LogicOpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AND();
    antlr4::tree::TerminalNode *OR();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LogicOpContext* logicOp();

  class  ValueContext : public antlr4::ParserRuleContext {
  public:
    ValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NUM();
    antlr4::tree::TerminalNode *VAR();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ValueContext* value();


  bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;

  bool expressionSempred(ExpressionContext *_localctx, size_t predicateIndex);
  bool conditionSempred(ConditionContext *_localctx, size_t predicateIndex);

  // By default the static state used to implement the parser is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:
};

