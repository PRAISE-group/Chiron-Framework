
// Generated from tlang.g4 by ANTLR 4.13.2


#include "tlangVisitor.h"

#include "tlangParser.h"


using namespace antlrcpp;

using namespace antlr4;

namespace {

struct TlangParserStaticData final {
  TlangParserStaticData(std::vector<std::string> ruleNames,
                        std::vector<std::string> literalNames,
                        std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  TlangParserStaticData(const TlangParserStaticData&) = delete;
  TlangParserStaticData(TlangParserStaticData&&) = delete;
  TlangParserStaticData& operator=(const TlangParserStaticData&) = delete;
  TlangParserStaticData& operator=(TlangParserStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag tlangParserOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<TlangParserStaticData> tlangParserStaticData = nullptr;

void tlangParserInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (tlangParserStaticData != nullptr) {
    return;
  }
#else
  assert(tlangParserStaticData == nullptr);
#endif
  auto staticData = std::make_unique<TlangParserStaticData>(
    std::vector<std::string>{
      "start", "instruction_list", "strict_ilist", "instruction", "conditional", 
      "ifConditional", "ifElseConditional", "loop", "gotoCommand", "assignment", 
      "moveCommand", "moveOp", "penCommand", "pauseCommand", "expression", 
      "multiplicative", "additive", "unaryArithOp", "condition", "binCondOp", 
      "logicOp", "value"
    },
    std::vector<std::string>{
      "", "'if'", "'['", "']'", "'else'", "'repeat'", "'goto'", "'('", "','", 
      "')'", "'='", "'forward'", "'backward'", "'left'", "'right'", "'penup'", 
      "'pendown'", "'pause'", "'+'", "'-'", "'*'", "'/'", "'pendown\\u003F'", 
      "'<'", "'>'", "'=='", "'!='", "'<='", "'>='", "'&&'", "'||'", "'!'"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
      "", "PLUS", "MINUS", "MUL", "DIV", "PENCOND", "LT", "GT", "EQ", "NEQ", 
      "LTE", "GTE", "AND", "OR", "NOT", "NUM", "VAR", "NAME", "Whitespace"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,35,173,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,2,
  	7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,7,
  	14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,7,
  	21,1,0,1,0,1,0,1,1,5,1,49,8,1,10,1,12,1,52,9,1,1,2,4,2,55,8,2,11,2,12,
  	2,56,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,66,8,3,1,4,1,4,3,4,70,8,4,1,5,1,
  	5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,
  	1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,10,1,10,1,10,
  	1,11,1,11,1,12,1,12,1,13,1,13,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,
  	1,14,3,14,123,8,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,5,14,133,8,
  	14,10,14,12,14,136,9,14,1,15,1,15,1,16,1,16,1,17,1,17,1,18,1,18,1,18,
  	1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,156,8,18,1,18,1,18,
  	1,18,1,18,5,18,162,8,18,10,18,12,18,165,9,18,1,19,1,19,1,20,1,20,1,21,
  	1,21,1,21,0,2,28,36,22,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,
  	34,36,38,40,42,0,7,1,0,11,14,1,0,15,16,1,0,20,21,1,0,18,19,1,0,23,28,
  	1,0,29,30,1,0,32,33,167,0,44,1,0,0,0,2,50,1,0,0,0,4,54,1,0,0,0,6,65,1,
  	0,0,0,8,69,1,0,0,0,10,71,1,0,0,0,12,77,1,0,0,0,14,87,1,0,0,0,16,93,1,
  	0,0,0,18,100,1,0,0,0,20,104,1,0,0,0,22,107,1,0,0,0,24,109,1,0,0,0,26,
  	111,1,0,0,0,28,122,1,0,0,0,30,137,1,0,0,0,32,139,1,0,0,0,34,141,1,0,0,
  	0,36,155,1,0,0,0,38,166,1,0,0,0,40,168,1,0,0,0,42,170,1,0,0,0,44,45,3,
  	2,1,0,45,46,5,0,0,1,46,1,1,0,0,0,47,49,3,6,3,0,48,47,1,0,0,0,49,52,1,
  	0,0,0,50,48,1,0,0,0,50,51,1,0,0,0,51,3,1,0,0,0,52,50,1,0,0,0,53,55,3,
  	6,3,0,54,53,1,0,0,0,55,56,1,0,0,0,56,54,1,0,0,0,56,57,1,0,0,0,57,5,1,
  	0,0,0,58,66,3,18,9,0,59,66,3,8,4,0,60,66,3,14,7,0,61,66,3,20,10,0,62,
  	66,3,24,12,0,63,66,3,16,8,0,64,66,3,26,13,0,65,58,1,0,0,0,65,59,1,0,0,
  	0,65,60,1,0,0,0,65,61,1,0,0,0,65,62,1,0,0,0,65,63,1,0,0,0,65,64,1,0,0,
  	0,66,7,1,0,0,0,67,70,3,10,5,0,68,70,3,12,6,0,69,67,1,0,0,0,69,68,1,0,
  	0,0,70,9,1,0,0,0,71,72,5,1,0,0,72,73,3,36,18,0,73,74,5,2,0,0,74,75,3,
  	4,2,0,75,76,5,3,0,0,76,11,1,0,0,0,77,78,5,1,0,0,78,79,3,36,18,0,79,80,
  	5,2,0,0,80,81,3,4,2,0,81,82,5,3,0,0,82,83,5,4,0,0,83,84,5,2,0,0,84,85,
  	3,4,2,0,85,86,5,3,0,0,86,13,1,0,0,0,87,88,5,5,0,0,88,89,3,42,21,0,89,
  	90,5,2,0,0,90,91,3,4,2,0,91,92,5,3,0,0,92,15,1,0,0,0,93,94,5,6,0,0,94,
  	95,5,7,0,0,95,96,3,28,14,0,96,97,5,8,0,0,97,98,3,28,14,0,98,99,5,9,0,
  	0,99,17,1,0,0,0,100,101,5,33,0,0,101,102,5,10,0,0,102,103,3,28,14,0,103,
  	19,1,0,0,0,104,105,3,22,11,0,105,106,3,28,14,0,106,21,1,0,0,0,107,108,
  	7,0,0,0,108,23,1,0,0,0,109,110,7,1,0,0,110,25,1,0,0,0,111,112,5,17,0,
  	0,112,27,1,0,0,0,113,114,6,14,-1,0,114,115,3,34,17,0,115,116,3,28,14,
  	5,116,123,1,0,0,0,117,123,3,42,21,0,118,119,5,7,0,0,119,120,3,28,14,0,
  	120,121,5,9,0,0,121,123,1,0,0,0,122,113,1,0,0,0,122,117,1,0,0,0,122,118,
  	1,0,0,0,123,134,1,0,0,0,124,125,10,4,0,0,125,126,3,30,15,0,126,127,3,
  	28,14,5,127,133,1,0,0,0,128,129,10,3,0,0,129,130,3,32,16,0,130,131,3,
  	28,14,4,131,133,1,0,0,0,132,124,1,0,0,0,132,128,1,0,0,0,133,136,1,0,0,
  	0,134,132,1,0,0,0,134,135,1,0,0,0,135,29,1,0,0,0,136,134,1,0,0,0,137,
  	138,7,2,0,0,138,31,1,0,0,0,139,140,7,3,0,0,140,33,1,0,0,0,141,142,5,19,
  	0,0,142,35,1,0,0,0,143,144,6,18,-1,0,144,145,5,31,0,0,145,156,3,36,18,
  	5,146,147,3,28,14,0,147,148,3,38,19,0,148,149,3,28,14,0,149,156,1,0,0,
  	0,150,156,5,22,0,0,151,152,5,7,0,0,152,153,3,36,18,0,153,154,5,9,0,0,
  	154,156,1,0,0,0,155,143,1,0,0,0,155,146,1,0,0,0,155,150,1,0,0,0,155,151,
  	1,0,0,0,156,163,1,0,0,0,157,158,10,3,0,0,158,159,3,40,20,0,159,160,3,
  	36,18,4,160,162,1,0,0,0,161,157,1,0,0,0,162,165,1,0,0,0,163,161,1,0,0,
  	0,163,164,1,0,0,0,164,37,1,0,0,0,165,163,1,0,0,0,166,167,7,4,0,0,167,
  	39,1,0,0,0,168,169,7,5,0,0,169,41,1,0,0,0,170,171,7,6,0,0,171,43,1,0,
  	0,0,9,50,56,65,69,122,132,134,155,163
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  tlangParserStaticData = std::move(staticData);
}

}

tlangParser::tlangParser(TokenStream *input) : tlangParser(input, antlr4::atn::ParserATNSimulatorOptions()) {}

tlangParser::tlangParser(TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options) : Parser(input) {
  tlangParser::initialize();
  _interpreter = new atn::ParserATNSimulator(this, *tlangParserStaticData->atn, tlangParserStaticData->decisionToDFA, tlangParserStaticData->sharedContextCache, options);
}

tlangParser::~tlangParser() {
  delete _interpreter;
}

const atn::ATN& tlangParser::getATN() const {
  return *tlangParserStaticData->atn;
}

std::string tlangParser::getGrammarFileName() const {
  return "tlang.g4";
}

const std::vector<std::string>& tlangParser::getRuleNames() const {
  return tlangParserStaticData->ruleNames;
}

const dfa::Vocabulary& tlangParser::getVocabulary() const {
  return tlangParserStaticData->vocabulary;
}

antlr4::atn::SerializedATNView tlangParser::getSerializedATN() const {
  return tlangParserStaticData->serializedATN;
}


//----------------- StartContext ------------------------------------------------------------------

tlangParser::StartContext::StartContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::Instruction_listContext* tlangParser::StartContext::instruction_list() {
  return getRuleContext<tlangParser::Instruction_listContext>(0);
}

tree::TerminalNode* tlangParser::StartContext::EOF() {
  return getToken(tlangParser::EOF, 0);
}


size_t tlangParser::StartContext::getRuleIndex() const {
  return tlangParser::RuleStart;
}


std::any tlangParser::StartContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitStart(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::StartContext* tlangParser::start() {
  StartContext *_localctx = _tracker.createInstance<StartContext>(_ctx, getState());
  enterRule(_localctx, 0, tlangParser::RuleStart);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(44);
    instruction_list();
    setState(45);
    match(tlangParser::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Instruction_listContext ------------------------------------------------------------------

tlangParser::Instruction_listContext::Instruction_listContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tlangParser::InstructionContext *> tlangParser::Instruction_listContext::instruction() {
  return getRuleContexts<tlangParser::InstructionContext>();
}

tlangParser::InstructionContext* tlangParser::Instruction_listContext::instruction(size_t i) {
  return getRuleContext<tlangParser::InstructionContext>(i);
}


size_t tlangParser::Instruction_listContext::getRuleIndex() const {
  return tlangParser::RuleInstruction_list;
}


std::any tlangParser::Instruction_listContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitInstruction_list(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::Instruction_listContext* tlangParser::instruction_list() {
  Instruction_listContext *_localctx = _tracker.createInstance<Instruction_listContext>(_ctx, getState());
  enterRule(_localctx, 2, tlangParser::RuleInstruction_list);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(50);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 8590194786) != 0)) {
      setState(47);
      instruction();
      setState(52);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Strict_ilistContext ------------------------------------------------------------------

tlangParser::Strict_ilistContext::Strict_ilistContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tlangParser::InstructionContext *> tlangParser::Strict_ilistContext::instruction() {
  return getRuleContexts<tlangParser::InstructionContext>();
}

tlangParser::InstructionContext* tlangParser::Strict_ilistContext::instruction(size_t i) {
  return getRuleContext<tlangParser::InstructionContext>(i);
}


size_t tlangParser::Strict_ilistContext::getRuleIndex() const {
  return tlangParser::RuleStrict_ilist;
}


std::any tlangParser::Strict_ilistContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitStrict_ilist(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::Strict_ilistContext* tlangParser::strict_ilist() {
  Strict_ilistContext *_localctx = _tracker.createInstance<Strict_ilistContext>(_ctx, getState());
  enterRule(_localctx, 4, tlangParser::RuleStrict_ilist);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(54); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(53);
      instruction();
      setState(56); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 8590194786) != 0));
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- InstructionContext ------------------------------------------------------------------

tlangParser::InstructionContext::InstructionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::AssignmentContext* tlangParser::InstructionContext::assignment() {
  return getRuleContext<tlangParser::AssignmentContext>(0);
}

tlangParser::ConditionalContext* tlangParser::InstructionContext::conditional() {
  return getRuleContext<tlangParser::ConditionalContext>(0);
}

tlangParser::LoopContext* tlangParser::InstructionContext::loop() {
  return getRuleContext<tlangParser::LoopContext>(0);
}

tlangParser::MoveCommandContext* tlangParser::InstructionContext::moveCommand() {
  return getRuleContext<tlangParser::MoveCommandContext>(0);
}

tlangParser::PenCommandContext* tlangParser::InstructionContext::penCommand() {
  return getRuleContext<tlangParser::PenCommandContext>(0);
}

tlangParser::GotoCommandContext* tlangParser::InstructionContext::gotoCommand() {
  return getRuleContext<tlangParser::GotoCommandContext>(0);
}

tlangParser::PauseCommandContext* tlangParser::InstructionContext::pauseCommand() {
  return getRuleContext<tlangParser::PauseCommandContext>(0);
}


size_t tlangParser::InstructionContext::getRuleIndex() const {
  return tlangParser::RuleInstruction;
}


std::any tlangParser::InstructionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitInstruction(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::InstructionContext* tlangParser::instruction() {
  InstructionContext *_localctx = _tracker.createInstance<InstructionContext>(_ctx, getState());
  enterRule(_localctx, 6, tlangParser::RuleInstruction);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(65);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case tlangParser::VAR: {
        enterOuterAlt(_localctx, 1);
        setState(58);
        assignment();
        break;
      }

      case tlangParser::T__0: {
        enterOuterAlt(_localctx, 2);
        setState(59);
        conditional();
        break;
      }

      case tlangParser::T__4: {
        enterOuterAlt(_localctx, 3);
        setState(60);
        loop();
        break;
      }

      case tlangParser::T__10:
      case tlangParser::T__11:
      case tlangParser::T__12:
      case tlangParser::T__13: {
        enterOuterAlt(_localctx, 4);
        setState(61);
        moveCommand();
        break;
      }

      case tlangParser::T__14:
      case tlangParser::T__15: {
        enterOuterAlt(_localctx, 5);
        setState(62);
        penCommand();
        break;
      }

      case tlangParser::T__5: {
        enterOuterAlt(_localctx, 6);
        setState(63);
        gotoCommand();
        break;
      }

      case tlangParser::T__16: {
        enterOuterAlt(_localctx, 7);
        setState(64);
        pauseCommand();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConditionalContext ------------------------------------------------------------------

tlangParser::ConditionalContext::ConditionalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::IfConditionalContext* tlangParser::ConditionalContext::ifConditional() {
  return getRuleContext<tlangParser::IfConditionalContext>(0);
}

tlangParser::IfElseConditionalContext* tlangParser::ConditionalContext::ifElseConditional() {
  return getRuleContext<tlangParser::IfElseConditionalContext>(0);
}


size_t tlangParser::ConditionalContext::getRuleIndex() const {
  return tlangParser::RuleConditional;
}


std::any tlangParser::ConditionalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitConditional(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ConditionalContext* tlangParser::conditional() {
  ConditionalContext *_localctx = _tracker.createInstance<ConditionalContext>(_ctx, getState());
  enterRule(_localctx, 8, tlangParser::RuleConditional);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(69);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 3, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(67);
      ifConditional();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(68);
      ifElseConditional();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IfConditionalContext ------------------------------------------------------------------

tlangParser::IfConditionalContext::IfConditionalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::ConditionContext* tlangParser::IfConditionalContext::condition() {
  return getRuleContext<tlangParser::ConditionContext>(0);
}

tlangParser::Strict_ilistContext* tlangParser::IfConditionalContext::strict_ilist() {
  return getRuleContext<tlangParser::Strict_ilistContext>(0);
}


size_t tlangParser::IfConditionalContext::getRuleIndex() const {
  return tlangParser::RuleIfConditional;
}


std::any tlangParser::IfConditionalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitIfConditional(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::IfConditionalContext* tlangParser::ifConditional() {
  IfConditionalContext *_localctx = _tracker.createInstance<IfConditionalContext>(_ctx, getState());
  enterRule(_localctx, 10, tlangParser::RuleIfConditional);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(71);
    match(tlangParser::T__0);
    setState(72);
    condition(0);
    setState(73);
    match(tlangParser::T__1);
    setState(74);
    strict_ilist();
    setState(75);
    match(tlangParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IfElseConditionalContext ------------------------------------------------------------------

tlangParser::IfElseConditionalContext::IfElseConditionalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::ConditionContext* tlangParser::IfElseConditionalContext::condition() {
  return getRuleContext<tlangParser::ConditionContext>(0);
}

std::vector<tlangParser::Strict_ilistContext *> tlangParser::IfElseConditionalContext::strict_ilist() {
  return getRuleContexts<tlangParser::Strict_ilistContext>();
}

tlangParser::Strict_ilistContext* tlangParser::IfElseConditionalContext::strict_ilist(size_t i) {
  return getRuleContext<tlangParser::Strict_ilistContext>(i);
}


size_t tlangParser::IfElseConditionalContext::getRuleIndex() const {
  return tlangParser::RuleIfElseConditional;
}


std::any tlangParser::IfElseConditionalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitIfElseConditional(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::IfElseConditionalContext* tlangParser::ifElseConditional() {
  IfElseConditionalContext *_localctx = _tracker.createInstance<IfElseConditionalContext>(_ctx, getState());
  enterRule(_localctx, 12, tlangParser::RuleIfElseConditional);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(77);
    match(tlangParser::T__0);
    setState(78);
    condition(0);
    setState(79);
    match(tlangParser::T__1);
    setState(80);
    strict_ilist();
    setState(81);
    match(tlangParser::T__2);
    setState(82);
    match(tlangParser::T__3);
    setState(83);
    match(tlangParser::T__1);
    setState(84);
    strict_ilist();
    setState(85);
    match(tlangParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LoopContext ------------------------------------------------------------------

tlangParser::LoopContext::LoopContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::ValueContext* tlangParser::LoopContext::value() {
  return getRuleContext<tlangParser::ValueContext>(0);
}

tlangParser::Strict_ilistContext* tlangParser::LoopContext::strict_ilist() {
  return getRuleContext<tlangParser::Strict_ilistContext>(0);
}


size_t tlangParser::LoopContext::getRuleIndex() const {
  return tlangParser::RuleLoop;
}


std::any tlangParser::LoopContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitLoop(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::LoopContext* tlangParser::loop() {
  LoopContext *_localctx = _tracker.createInstance<LoopContext>(_ctx, getState());
  enterRule(_localctx, 14, tlangParser::RuleLoop);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(87);
    match(tlangParser::T__4);
    setState(88);
    value();
    setState(89);
    match(tlangParser::T__1);
    setState(90);
    strict_ilist();
    setState(91);
    match(tlangParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- GotoCommandContext ------------------------------------------------------------------

tlangParser::GotoCommandContext::GotoCommandContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tlangParser::ExpressionContext *> tlangParser::GotoCommandContext::expression() {
  return getRuleContexts<tlangParser::ExpressionContext>();
}

tlangParser::ExpressionContext* tlangParser::GotoCommandContext::expression(size_t i) {
  return getRuleContext<tlangParser::ExpressionContext>(i);
}


size_t tlangParser::GotoCommandContext::getRuleIndex() const {
  return tlangParser::RuleGotoCommand;
}


std::any tlangParser::GotoCommandContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitGotoCommand(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::GotoCommandContext* tlangParser::gotoCommand() {
  GotoCommandContext *_localctx = _tracker.createInstance<GotoCommandContext>(_ctx, getState());
  enterRule(_localctx, 16, tlangParser::RuleGotoCommand);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(93);
    match(tlangParser::T__5);
    setState(94);
    match(tlangParser::T__6);
    setState(95);
    expression(0);
    setState(96);
    match(tlangParser::T__7);
    setState(97);
    expression(0);
    setState(98);
    match(tlangParser::T__8);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AssignmentContext ------------------------------------------------------------------

tlangParser::AssignmentContext::AssignmentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::AssignmentContext::VAR() {
  return getToken(tlangParser::VAR, 0);
}

tlangParser::ExpressionContext* tlangParser::AssignmentContext::expression() {
  return getRuleContext<tlangParser::ExpressionContext>(0);
}


size_t tlangParser::AssignmentContext::getRuleIndex() const {
  return tlangParser::RuleAssignment;
}


std::any tlangParser::AssignmentContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitAssignment(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::AssignmentContext* tlangParser::assignment() {
  AssignmentContext *_localctx = _tracker.createInstance<AssignmentContext>(_ctx, getState());
  enterRule(_localctx, 18, tlangParser::RuleAssignment);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(100);
    match(tlangParser::VAR);
    setState(101);
    match(tlangParser::T__9);
    setState(102);
    expression(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MoveCommandContext ------------------------------------------------------------------

tlangParser::MoveCommandContext::MoveCommandContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::MoveOpContext* tlangParser::MoveCommandContext::moveOp() {
  return getRuleContext<tlangParser::MoveOpContext>(0);
}

tlangParser::ExpressionContext* tlangParser::MoveCommandContext::expression() {
  return getRuleContext<tlangParser::ExpressionContext>(0);
}


size_t tlangParser::MoveCommandContext::getRuleIndex() const {
  return tlangParser::RuleMoveCommand;
}


std::any tlangParser::MoveCommandContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitMoveCommand(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::MoveCommandContext* tlangParser::moveCommand() {
  MoveCommandContext *_localctx = _tracker.createInstance<MoveCommandContext>(_ctx, getState());
  enterRule(_localctx, 20, tlangParser::RuleMoveCommand);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(104);
    moveOp();
    setState(105);
    expression(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MoveOpContext ------------------------------------------------------------------

tlangParser::MoveOpContext::MoveOpContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t tlangParser::MoveOpContext::getRuleIndex() const {
  return tlangParser::RuleMoveOp;
}


std::any tlangParser::MoveOpContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitMoveOp(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::MoveOpContext* tlangParser::moveOp() {
  MoveOpContext *_localctx = _tracker.createInstance<MoveOpContext>(_ctx, getState());
  enterRule(_localctx, 22, tlangParser::RuleMoveOp);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(107);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 30720) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PenCommandContext ------------------------------------------------------------------

tlangParser::PenCommandContext::PenCommandContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t tlangParser::PenCommandContext::getRuleIndex() const {
  return tlangParser::RulePenCommand;
}


std::any tlangParser::PenCommandContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitPenCommand(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::PenCommandContext* tlangParser::penCommand() {
  PenCommandContext *_localctx = _tracker.createInstance<PenCommandContext>(_ctx, getState());
  enterRule(_localctx, 24, tlangParser::RulePenCommand);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(109);
    _la = _input->LA(1);
    if (!(_la == tlangParser::T__14

    || _la == tlangParser::T__15)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PauseCommandContext ------------------------------------------------------------------

tlangParser::PauseCommandContext::PauseCommandContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t tlangParser::PauseCommandContext::getRuleIndex() const {
  return tlangParser::RulePauseCommand;
}


std::any tlangParser::PauseCommandContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitPauseCommand(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::PauseCommandContext* tlangParser::pauseCommand() {
  PauseCommandContext *_localctx = _tracker.createInstance<PauseCommandContext>(_ctx, getState());
  enterRule(_localctx, 26, tlangParser::RulePauseCommand);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(111);
    match(tlangParser::T__16);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExpressionContext ------------------------------------------------------------------

tlangParser::ExpressionContext::ExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t tlangParser::ExpressionContext::getRuleIndex() const {
  return tlangParser::RuleExpression;
}

void tlangParser::ExpressionContext::copyFrom(ExpressionContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- UnaryExprContext ------------------------------------------------------------------

tlangParser::UnaryArithOpContext* tlangParser::UnaryExprContext::unaryArithOp() {
  return getRuleContext<tlangParser::UnaryArithOpContext>(0);
}

tlangParser::ExpressionContext* tlangParser::UnaryExprContext::expression() {
  return getRuleContext<tlangParser::ExpressionContext>(0);
}

tlangParser::UnaryExprContext::UnaryExprContext(ExpressionContext *ctx) { copyFrom(ctx); }


std::any tlangParser::UnaryExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitUnaryExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ValueExprContext ------------------------------------------------------------------

tlangParser::ValueContext* tlangParser::ValueExprContext::value() {
  return getRuleContext<tlangParser::ValueContext>(0);
}

tlangParser::ValueExprContext::ValueExprContext(ExpressionContext *ctx) { copyFrom(ctx); }


std::any tlangParser::ValueExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitValueExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- AddExprContext ------------------------------------------------------------------

std::vector<tlangParser::ExpressionContext *> tlangParser::AddExprContext::expression() {
  return getRuleContexts<tlangParser::ExpressionContext>();
}

tlangParser::ExpressionContext* tlangParser::AddExprContext::expression(size_t i) {
  return getRuleContext<tlangParser::ExpressionContext>(i);
}

tlangParser::AdditiveContext* tlangParser::AddExprContext::additive() {
  return getRuleContext<tlangParser::AdditiveContext>(0);
}

tlangParser::AddExprContext::AddExprContext(ExpressionContext *ctx) { copyFrom(ctx); }


std::any tlangParser::AddExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitAddExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- MulExprContext ------------------------------------------------------------------

std::vector<tlangParser::ExpressionContext *> tlangParser::MulExprContext::expression() {
  return getRuleContexts<tlangParser::ExpressionContext>();
}

tlangParser::ExpressionContext* tlangParser::MulExprContext::expression(size_t i) {
  return getRuleContext<tlangParser::ExpressionContext>(i);
}

tlangParser::MultiplicativeContext* tlangParser::MulExprContext::multiplicative() {
  return getRuleContext<tlangParser::MultiplicativeContext>(0);
}

tlangParser::MulExprContext::MulExprContext(ExpressionContext *ctx) { copyFrom(ctx); }


std::any tlangParser::MulExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitMulExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ParenExprContext ------------------------------------------------------------------

tlangParser::ExpressionContext* tlangParser::ParenExprContext::expression() {
  return getRuleContext<tlangParser::ExpressionContext>(0);
}

tlangParser::ParenExprContext::ParenExprContext(ExpressionContext *ctx) { copyFrom(ctx); }


std::any tlangParser::ParenExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitParenExpr(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ExpressionContext* tlangParser::expression() {
   return expression(0);
}

tlangParser::ExpressionContext* tlangParser::expression(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  tlangParser::ExpressionContext *_localctx = _tracker.createInstance<ExpressionContext>(_ctx, parentState);
  tlangParser::ExpressionContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 28;
  enterRecursionRule(_localctx, 28, tlangParser::RuleExpression, precedence);

    

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(122);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case tlangParser::MINUS: {
        _localctx = _tracker.createInstance<UnaryExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;

        setState(114);
        unaryArithOp();
        setState(115);
        expression(5);
        break;
      }

      case tlangParser::NUM:
      case tlangParser::VAR: {
        _localctx = _tracker.createInstance<ValueExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;
        setState(117);
        value();
        break;
      }

      case tlangParser::T__6: {
        _localctx = _tracker.createInstance<ParenExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;
        setState(118);
        match(tlangParser::T__6);
        setState(119);
        expression(0);
        setState(120);
        match(tlangParser::T__8);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
    _ctx->stop = _input->LT(-1);
    setState(134);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 6, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        setState(132);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 5, _ctx)) {
        case 1: {
          auto newContext = _tracker.createInstance<MulExprContext>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(124);

          if (!(precpred(_ctx, 4))) throw FailedPredicateException(this, "precpred(_ctx, 4)");
          setState(125);
          multiplicative();
          setState(126);
          expression(5);
          break;
        }

        case 2: {
          auto newContext = _tracker.createInstance<AddExprContext>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(128);

          if (!(precpred(_ctx, 3))) throw FailedPredicateException(this, "precpred(_ctx, 3)");
          setState(129);
          additive();
          setState(130);
          expression(4);
          break;
        }

        default:
          break;
        } 
      }
      setState(136);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 6, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

//----------------- MultiplicativeContext ------------------------------------------------------------------

tlangParser::MultiplicativeContext::MultiplicativeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::MultiplicativeContext::MUL() {
  return getToken(tlangParser::MUL, 0);
}

tree::TerminalNode* tlangParser::MultiplicativeContext::DIV() {
  return getToken(tlangParser::DIV, 0);
}


size_t tlangParser::MultiplicativeContext::getRuleIndex() const {
  return tlangParser::RuleMultiplicative;
}


std::any tlangParser::MultiplicativeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitMultiplicative(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::MultiplicativeContext* tlangParser::multiplicative() {
  MultiplicativeContext *_localctx = _tracker.createInstance<MultiplicativeContext>(_ctx, getState());
  enterRule(_localctx, 30, tlangParser::RuleMultiplicative);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(137);
    _la = _input->LA(1);
    if (!(_la == tlangParser::MUL

    || _la == tlangParser::DIV)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AdditiveContext ------------------------------------------------------------------

tlangParser::AdditiveContext::AdditiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::AdditiveContext::PLUS() {
  return getToken(tlangParser::PLUS, 0);
}

tree::TerminalNode* tlangParser::AdditiveContext::MINUS() {
  return getToken(tlangParser::MINUS, 0);
}


size_t tlangParser::AdditiveContext::getRuleIndex() const {
  return tlangParser::RuleAdditive;
}


std::any tlangParser::AdditiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitAdditive(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::AdditiveContext* tlangParser::additive() {
  AdditiveContext *_localctx = _tracker.createInstance<AdditiveContext>(_ctx, getState());
  enterRule(_localctx, 32, tlangParser::RuleAdditive);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(139);
    _la = _input->LA(1);
    if (!(_la == tlangParser::PLUS

    || _la == tlangParser::MINUS)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- UnaryArithOpContext ------------------------------------------------------------------

tlangParser::UnaryArithOpContext::UnaryArithOpContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::UnaryArithOpContext::MINUS() {
  return getToken(tlangParser::MINUS, 0);
}


size_t tlangParser::UnaryArithOpContext::getRuleIndex() const {
  return tlangParser::RuleUnaryArithOp;
}


std::any tlangParser::UnaryArithOpContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitUnaryArithOp(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::UnaryArithOpContext* tlangParser::unaryArithOp() {
  UnaryArithOpContext *_localctx = _tracker.createInstance<UnaryArithOpContext>(_ctx, getState());
  enterRule(_localctx, 34, tlangParser::RuleUnaryArithOp);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(141);
    match(tlangParser::MINUS);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConditionContext ------------------------------------------------------------------

tlangParser::ConditionContext::ConditionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::ConditionContext::NOT() {
  return getToken(tlangParser::NOT, 0);
}

std::vector<tlangParser::ConditionContext *> tlangParser::ConditionContext::condition() {
  return getRuleContexts<tlangParser::ConditionContext>();
}

tlangParser::ConditionContext* tlangParser::ConditionContext::condition(size_t i) {
  return getRuleContext<tlangParser::ConditionContext>(i);
}

std::vector<tlangParser::ExpressionContext *> tlangParser::ConditionContext::expression() {
  return getRuleContexts<tlangParser::ExpressionContext>();
}

tlangParser::ExpressionContext* tlangParser::ConditionContext::expression(size_t i) {
  return getRuleContext<tlangParser::ExpressionContext>(i);
}

tlangParser::BinCondOpContext* tlangParser::ConditionContext::binCondOp() {
  return getRuleContext<tlangParser::BinCondOpContext>(0);
}

tree::TerminalNode* tlangParser::ConditionContext::PENCOND() {
  return getToken(tlangParser::PENCOND, 0);
}

tlangParser::LogicOpContext* tlangParser::ConditionContext::logicOp() {
  return getRuleContext<tlangParser::LogicOpContext>(0);
}


size_t tlangParser::ConditionContext::getRuleIndex() const {
  return tlangParser::RuleCondition;
}


std::any tlangParser::ConditionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitCondition(this);
  else
    return visitor->visitChildren(this);
}


tlangParser::ConditionContext* tlangParser::condition() {
   return condition(0);
}

tlangParser::ConditionContext* tlangParser::condition(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  tlangParser::ConditionContext *_localctx = _tracker.createInstance<ConditionContext>(_ctx, parentState);
  tlangParser::ConditionContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 36;
  enterRecursionRule(_localctx, 36, tlangParser::RuleCondition, precedence);

    

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(155);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 7, _ctx)) {
    case 1: {
      setState(144);
      match(tlangParser::NOT);
      setState(145);
      condition(5);
      break;
    }

    case 2: {
      setState(146);
      expression(0);
      setState(147);
      binCondOp();
      setState(148);
      expression(0);
      break;
    }

    case 3: {
      setState(150);
      match(tlangParser::PENCOND);
      break;
    }

    case 4: {
      setState(151);
      match(tlangParser::T__6);
      setState(152);
      condition(0);
      setState(153);
      match(tlangParser::T__8);
      break;
    }

    default:
      break;
    }
    _ctx->stop = _input->LT(-1);
    setState(163);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 8, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        _localctx = _tracker.createInstance<ConditionContext>(parentContext, parentState);
        pushNewRecursionContext(_localctx, startState, RuleCondition);
        setState(157);

        if (!(precpred(_ctx, 3))) throw FailedPredicateException(this, "precpred(_ctx, 3)");
        setState(158);
        logicOp();
        setState(159);
        condition(4); 
      }
      setState(165);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 8, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

//----------------- BinCondOpContext ------------------------------------------------------------------

tlangParser::BinCondOpContext::BinCondOpContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::BinCondOpContext::EQ() {
  return getToken(tlangParser::EQ, 0);
}

tree::TerminalNode* tlangParser::BinCondOpContext::NEQ() {
  return getToken(tlangParser::NEQ, 0);
}

tree::TerminalNode* tlangParser::BinCondOpContext::LT() {
  return getToken(tlangParser::LT, 0);
}

tree::TerminalNode* tlangParser::BinCondOpContext::GT() {
  return getToken(tlangParser::GT, 0);
}

tree::TerminalNode* tlangParser::BinCondOpContext::LTE() {
  return getToken(tlangParser::LTE, 0);
}

tree::TerminalNode* tlangParser::BinCondOpContext::GTE() {
  return getToken(tlangParser::GTE, 0);
}


size_t tlangParser::BinCondOpContext::getRuleIndex() const {
  return tlangParser::RuleBinCondOp;
}


std::any tlangParser::BinCondOpContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitBinCondOp(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::BinCondOpContext* tlangParser::binCondOp() {
  BinCondOpContext *_localctx = _tracker.createInstance<BinCondOpContext>(_ctx, getState());
  enterRule(_localctx, 38, tlangParser::RuleBinCondOp);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(166);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 528482304) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LogicOpContext ------------------------------------------------------------------

tlangParser::LogicOpContext::LogicOpContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::LogicOpContext::AND() {
  return getToken(tlangParser::AND, 0);
}

tree::TerminalNode* tlangParser::LogicOpContext::OR() {
  return getToken(tlangParser::OR, 0);
}


size_t tlangParser::LogicOpContext::getRuleIndex() const {
  return tlangParser::RuleLogicOp;
}


std::any tlangParser::LogicOpContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitLogicOp(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::LogicOpContext* tlangParser::logicOp() {
  LogicOpContext *_localctx = _tracker.createInstance<LogicOpContext>(_ctx, getState());
  enterRule(_localctx, 40, tlangParser::RuleLogicOp);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(168);
    _la = _input->LA(1);
    if (!(_la == tlangParser::AND

    || _la == tlangParser::OR)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ValueContext ------------------------------------------------------------------

tlangParser::ValueContext::ValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::ValueContext::NUM() {
  return getToken(tlangParser::NUM, 0);
}

tree::TerminalNode* tlangParser::ValueContext::VAR() {
  return getToken(tlangParser::VAR, 0);
}


size_t tlangParser::ValueContext::getRuleIndex() const {
  return tlangParser::RuleValue;
}


std::any tlangParser::ValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitValue(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ValueContext* tlangParser::value() {
  ValueContext *_localctx = _tracker.createInstance<ValueContext>(_ctx, getState());
  enterRule(_localctx, 42, tlangParser::RuleValue);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(170);
    _la = _input->LA(1);
    if (!(_la == tlangParser::NUM

    || _la == tlangParser::VAR)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

bool tlangParser::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 14: return expressionSempred(antlrcpp::downCast<ExpressionContext *>(context), predicateIndex);
    case 18: return conditionSempred(antlrcpp::downCast<ConditionContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool tlangParser::expressionSempred(ExpressionContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return precpred(_ctx, 4);
    case 1: return precpred(_ctx, 3);

  default:
    break;
  }
  return true;
}

bool tlangParser::conditionSempred(ConditionContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 2: return precpred(_ctx, 3);

  default:
    break;
  }
  return true;
}

void tlangParser::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  tlangParserInitialize();
#else
  ::antlr4::internal::call_once(tlangParserOnceFlag, tlangParserInitialize);
#endif
}
