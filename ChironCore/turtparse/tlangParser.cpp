
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
      "start", "instruction_list", "strict_ilist", "function_list", "function_declaration", 
      "voidFunction", "valueFunction", "voidReturn", "valueReturn", "parametersDeclaration", 
      "parameterCall", "voidFuncCall", "valueFuncCall", "instruction", "conditional", 
      "ifConditional", "ifElseConditional", "loop", "gotoCommand", "assignment", 
      "moveCommand", "moveOp", "penCommand", "pauseCommand", "expression", 
      "multiplicative", "additive", "unaryArithOp", "condition", "binCondOp", 
      "logicOp", "value"
    },
    std::vector<std::string>{
      "", "'voidfunc'", "'{'", "'}'", "'valuefunc'", "'voidreturn'", "'valuereturn'", 
      "'('", "')'", "','", "'procedure'", "'get'", "'if'", "'['", "']'", 
      "'else'", "'repeat'", "'goto'", "'='", "'forward'", "'backward'", 
      "'left'", "'right'", "'penup'", "'pendown'", "'pause'", "'+'", "'-'", 
      "'*'", "'/'", "'pendown\\u003F'", "'<'", "'>'", "'=='", "'!='", "'<='", 
      "'>='", "'&&'", "'||'", "'!'"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
      "", "", "", "", "", "", "", "", "", "PLUS", "MINUS", "MUL", "DIV", 
      "PENCOND", "LT", "GT", "EQ", "NEQ", "LTE", "GTE", "AND", "OR", "NOT", 
      "NUM", "VAR", "NAME", "Whitespace"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,43,264,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,2,
  	7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,7,
  	14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,7,
  	21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,7,
  	28,2,29,7,29,2,30,7,30,2,31,7,31,1,0,1,0,1,0,1,0,1,1,5,1,70,8,1,10,1,
  	12,1,73,9,1,1,2,4,2,76,8,2,11,2,12,2,77,1,3,5,3,81,8,3,10,3,12,3,84,9,
  	3,1,4,1,4,3,4,88,8,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,
  	1,6,1,6,1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,5,9,117,8,
  	9,10,9,12,9,120,9,9,1,9,3,9,123,8,9,1,10,1,10,1,10,1,10,1,10,1,10,5,10,
  	131,8,10,10,10,12,10,134,9,10,1,10,1,10,3,10,138,8,10,1,11,1,11,1,11,
  	1,11,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,
  	156,8,13,1,14,1,14,3,14,160,8,14,1,15,1,15,1,15,1,15,1,15,1,15,1,16,1,
  	16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,
  	17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,20,1,20,1,
  	20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,
  	24,1,24,1,24,3,24,214,8,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,5,
  	24,224,8,24,10,24,12,24,227,9,24,1,25,1,25,1,26,1,26,1,27,1,27,1,28,1,
  	28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,3,28,247,8,28,1,
  	28,1,28,1,28,1,28,5,28,253,8,28,10,28,12,28,256,9,28,1,29,1,29,1,30,1,
  	30,1,31,1,31,1,31,0,2,48,56,32,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,
  	30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,0,7,1,0,19,22,1,0,
  	23,24,1,0,28,29,1,0,26,27,1,0,31,36,1,0,37,38,1,0,40,41,256,0,64,1,0,
  	0,0,2,71,1,0,0,0,4,75,1,0,0,0,6,82,1,0,0,0,8,87,1,0,0,0,10,89,1,0,0,0,
  	12,97,1,0,0,0,14,105,1,0,0,0,16,107,1,0,0,0,18,122,1,0,0,0,20,137,1,0,
  	0,0,22,139,1,0,0,0,24,143,1,0,0,0,26,155,1,0,0,0,28,159,1,0,0,0,30,161,
  	1,0,0,0,32,167,1,0,0,0,34,177,1,0,0,0,36,183,1,0,0,0,38,190,1,0,0,0,40,
  	194,1,0,0,0,42,197,1,0,0,0,44,199,1,0,0,0,46,201,1,0,0,0,48,213,1,0,0,
  	0,50,228,1,0,0,0,52,230,1,0,0,0,54,232,1,0,0,0,56,246,1,0,0,0,58,257,
  	1,0,0,0,60,259,1,0,0,0,62,261,1,0,0,0,64,65,3,6,3,0,65,66,3,2,1,0,66,
  	67,5,0,0,1,67,1,1,0,0,0,68,70,3,26,13,0,69,68,1,0,0,0,70,73,1,0,0,0,71,
  	69,1,0,0,0,71,72,1,0,0,0,72,3,1,0,0,0,73,71,1,0,0,0,74,76,3,26,13,0,75,
  	74,1,0,0,0,76,77,1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,0,78,5,1,0,0,0,79,
  	81,3,8,4,0,80,79,1,0,0,0,81,84,1,0,0,0,82,80,1,0,0,0,82,83,1,0,0,0,83,
  	7,1,0,0,0,84,82,1,0,0,0,85,88,3,10,5,0,86,88,3,12,6,0,87,85,1,0,0,0,87,
  	86,1,0,0,0,88,9,1,0,0,0,89,90,5,1,0,0,90,91,5,42,0,0,91,92,3,18,9,0,92,
  	93,5,2,0,0,93,94,3,2,1,0,94,95,3,14,7,0,95,96,5,3,0,0,96,11,1,0,0,0,97,
  	98,5,4,0,0,98,99,5,42,0,0,99,100,3,18,9,0,100,101,5,2,0,0,101,102,3,2,
  	1,0,102,103,3,16,8,0,103,104,5,3,0,0,104,13,1,0,0,0,105,106,5,5,0,0,106,
  	15,1,0,0,0,107,108,5,6,0,0,108,109,3,48,24,0,109,17,1,0,0,0,110,111,5,
  	7,0,0,111,123,5,8,0,0,112,113,5,7,0,0,113,118,5,41,0,0,114,115,5,9,0,
  	0,115,117,5,41,0,0,116,114,1,0,0,0,117,120,1,0,0,0,118,116,1,0,0,0,118,
  	119,1,0,0,0,119,121,1,0,0,0,120,118,1,0,0,0,121,123,5,8,0,0,122,110,1,
  	0,0,0,122,112,1,0,0,0,123,19,1,0,0,0,124,125,5,7,0,0,125,138,5,8,0,0,
  	126,127,5,7,0,0,127,132,3,48,24,0,128,129,5,9,0,0,129,131,3,48,24,0,130,
  	128,1,0,0,0,131,134,1,0,0,0,132,130,1,0,0,0,132,133,1,0,0,0,133,135,1,
  	0,0,0,134,132,1,0,0,0,135,136,5,8,0,0,136,138,1,0,0,0,137,124,1,0,0,0,
  	137,126,1,0,0,0,138,21,1,0,0,0,139,140,5,10,0,0,140,141,5,42,0,0,141,
  	142,3,20,10,0,142,23,1,0,0,0,143,144,5,11,0,0,144,145,5,42,0,0,145,146,
  	3,20,10,0,146,25,1,0,0,0,147,156,3,38,19,0,148,156,3,28,14,0,149,156,
  	3,34,17,0,150,156,3,40,20,0,151,156,3,44,22,0,152,156,3,36,18,0,153,156,
  	3,46,23,0,154,156,3,22,11,0,155,147,1,0,0,0,155,148,1,0,0,0,155,149,1,
  	0,0,0,155,150,1,0,0,0,155,151,1,0,0,0,155,152,1,0,0,0,155,153,1,0,0,0,
  	155,154,1,0,0,0,156,27,1,0,0,0,157,160,3,30,15,0,158,160,3,32,16,0,159,
  	157,1,0,0,0,159,158,1,0,0,0,160,29,1,0,0,0,161,162,5,12,0,0,162,163,3,
  	56,28,0,163,164,5,13,0,0,164,165,3,4,2,0,165,166,5,14,0,0,166,31,1,0,
  	0,0,167,168,5,12,0,0,168,169,3,56,28,0,169,170,5,13,0,0,170,171,3,4,2,
  	0,171,172,5,14,0,0,172,173,5,15,0,0,173,174,5,13,0,0,174,175,3,4,2,0,
  	175,176,5,14,0,0,176,33,1,0,0,0,177,178,5,16,0,0,178,179,3,62,31,0,179,
  	180,5,13,0,0,180,181,3,4,2,0,181,182,5,14,0,0,182,35,1,0,0,0,183,184,
  	5,17,0,0,184,185,5,7,0,0,185,186,3,48,24,0,186,187,5,9,0,0,187,188,3,
  	48,24,0,188,189,5,8,0,0,189,37,1,0,0,0,190,191,5,41,0,0,191,192,5,18,
  	0,0,192,193,3,48,24,0,193,39,1,0,0,0,194,195,3,42,21,0,195,196,3,48,24,
  	0,196,41,1,0,0,0,197,198,7,0,0,0,198,43,1,0,0,0,199,200,7,1,0,0,200,45,
  	1,0,0,0,201,202,5,25,0,0,202,47,1,0,0,0,203,204,6,24,-1,0,204,205,3,54,
  	27,0,205,206,3,48,24,6,206,214,1,0,0,0,207,214,3,62,31,0,208,209,5,7,
  	0,0,209,210,3,48,24,0,210,211,5,8,0,0,211,214,1,0,0,0,212,214,3,24,12,
  	0,213,203,1,0,0,0,213,207,1,0,0,0,213,208,1,0,0,0,213,212,1,0,0,0,214,
  	225,1,0,0,0,215,216,10,5,0,0,216,217,3,50,25,0,217,218,3,48,24,6,218,
  	224,1,0,0,0,219,220,10,4,0,0,220,221,3,52,26,0,221,222,3,48,24,5,222,
  	224,1,0,0,0,223,215,1,0,0,0,223,219,1,0,0,0,224,227,1,0,0,0,225,223,1,
  	0,0,0,225,226,1,0,0,0,226,49,1,0,0,0,227,225,1,0,0,0,228,229,7,2,0,0,
  	229,51,1,0,0,0,230,231,7,3,0,0,231,53,1,0,0,0,232,233,5,27,0,0,233,55,
  	1,0,0,0,234,235,6,28,-1,0,235,236,5,39,0,0,236,247,3,56,28,5,237,238,
  	3,48,24,0,238,239,3,58,29,0,239,240,3,48,24,0,240,247,1,0,0,0,241,247,
  	5,30,0,0,242,243,5,7,0,0,243,244,3,56,28,0,244,245,5,8,0,0,245,247,1,
  	0,0,0,246,234,1,0,0,0,246,237,1,0,0,0,246,241,1,0,0,0,246,242,1,0,0,0,
  	247,254,1,0,0,0,248,249,10,3,0,0,249,250,3,60,30,0,250,251,3,56,28,4,
  	251,253,1,0,0,0,252,248,1,0,0,0,253,256,1,0,0,0,254,252,1,0,0,0,254,255,
  	1,0,0,0,255,57,1,0,0,0,256,254,1,0,0,0,257,258,7,4,0,0,258,59,1,0,0,0,
  	259,260,7,5,0,0,260,61,1,0,0,0,261,262,7,6,0,0,262,63,1,0,0,0,15,71,77,
  	82,87,118,122,132,137,155,159,213,223,225,246,254
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

tlangParser::Function_listContext* tlangParser::StartContext::function_list() {
  return getRuleContext<tlangParser::Function_listContext>(0);
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
    setState(64);
    function_list();
    setState(65);
    instruction_list();
    setState(66);
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
    setState(71);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 2199090041856) != 0)) {
      setState(68);
      instruction();
      setState(73);
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
    setState(75); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(74);
      instruction();
      setState(77); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 2199090041856) != 0));
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Function_listContext ------------------------------------------------------------------

tlangParser::Function_listContext::Function_listContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tlangParser::Function_declarationContext *> tlangParser::Function_listContext::function_declaration() {
  return getRuleContexts<tlangParser::Function_declarationContext>();
}

tlangParser::Function_declarationContext* tlangParser::Function_listContext::function_declaration(size_t i) {
  return getRuleContext<tlangParser::Function_declarationContext>(i);
}


size_t tlangParser::Function_listContext::getRuleIndex() const {
  return tlangParser::RuleFunction_list;
}


std::any tlangParser::Function_listContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitFunction_list(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::Function_listContext* tlangParser::function_list() {
  Function_listContext *_localctx = _tracker.createInstance<Function_listContext>(_ctx, getState());
  enterRule(_localctx, 6, tlangParser::RuleFunction_list);
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
    setState(82);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == tlangParser::T__0

    || _la == tlangParser::T__3) {
      setState(79);
      function_declaration();
      setState(84);
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

//----------------- Function_declarationContext ------------------------------------------------------------------

tlangParser::Function_declarationContext::Function_declarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::VoidFunctionContext* tlangParser::Function_declarationContext::voidFunction() {
  return getRuleContext<tlangParser::VoidFunctionContext>(0);
}

tlangParser::ValueFunctionContext* tlangParser::Function_declarationContext::valueFunction() {
  return getRuleContext<tlangParser::ValueFunctionContext>(0);
}


size_t tlangParser::Function_declarationContext::getRuleIndex() const {
  return tlangParser::RuleFunction_declaration;
}


std::any tlangParser::Function_declarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitFunction_declaration(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::Function_declarationContext* tlangParser::function_declaration() {
  Function_declarationContext *_localctx = _tracker.createInstance<Function_declarationContext>(_ctx, getState());
  enterRule(_localctx, 8, tlangParser::RuleFunction_declaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(87);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case tlangParser::T__0: {
        enterOuterAlt(_localctx, 1);
        setState(85);
        voidFunction();
        break;
      }

      case tlangParser::T__3: {
        enterOuterAlt(_localctx, 2);
        setState(86);
        valueFunction();
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

//----------------- VoidFunctionContext ------------------------------------------------------------------

tlangParser::VoidFunctionContext::VoidFunctionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::VoidFunctionContext::NAME() {
  return getToken(tlangParser::NAME, 0);
}

tlangParser::ParametersDeclarationContext* tlangParser::VoidFunctionContext::parametersDeclaration() {
  return getRuleContext<tlangParser::ParametersDeclarationContext>(0);
}

tlangParser::Instruction_listContext* tlangParser::VoidFunctionContext::instruction_list() {
  return getRuleContext<tlangParser::Instruction_listContext>(0);
}

tlangParser::VoidReturnContext* tlangParser::VoidFunctionContext::voidReturn() {
  return getRuleContext<tlangParser::VoidReturnContext>(0);
}


size_t tlangParser::VoidFunctionContext::getRuleIndex() const {
  return tlangParser::RuleVoidFunction;
}


std::any tlangParser::VoidFunctionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitVoidFunction(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::VoidFunctionContext* tlangParser::voidFunction() {
  VoidFunctionContext *_localctx = _tracker.createInstance<VoidFunctionContext>(_ctx, getState());
  enterRule(_localctx, 10, tlangParser::RuleVoidFunction);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(89);
    match(tlangParser::T__0);
    setState(90);
    match(tlangParser::NAME);
    setState(91);
    parametersDeclaration();
    setState(92);
    match(tlangParser::T__1);
    setState(93);
    instruction_list();
    setState(94);
    voidReturn();
    setState(95);
    match(tlangParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ValueFunctionContext ------------------------------------------------------------------

tlangParser::ValueFunctionContext::ValueFunctionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::ValueFunctionContext::NAME() {
  return getToken(tlangParser::NAME, 0);
}

tlangParser::ParametersDeclarationContext* tlangParser::ValueFunctionContext::parametersDeclaration() {
  return getRuleContext<tlangParser::ParametersDeclarationContext>(0);
}

tlangParser::Instruction_listContext* tlangParser::ValueFunctionContext::instruction_list() {
  return getRuleContext<tlangParser::Instruction_listContext>(0);
}

tlangParser::ValueReturnContext* tlangParser::ValueFunctionContext::valueReturn() {
  return getRuleContext<tlangParser::ValueReturnContext>(0);
}


size_t tlangParser::ValueFunctionContext::getRuleIndex() const {
  return tlangParser::RuleValueFunction;
}


std::any tlangParser::ValueFunctionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitValueFunction(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ValueFunctionContext* tlangParser::valueFunction() {
  ValueFunctionContext *_localctx = _tracker.createInstance<ValueFunctionContext>(_ctx, getState());
  enterRule(_localctx, 12, tlangParser::RuleValueFunction);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(97);
    match(tlangParser::T__3);
    setState(98);
    match(tlangParser::NAME);
    setState(99);
    parametersDeclaration();
    setState(100);
    match(tlangParser::T__1);
    setState(101);
    instruction_list();
    setState(102);
    valueReturn();
    setState(103);
    match(tlangParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VoidReturnContext ------------------------------------------------------------------

tlangParser::VoidReturnContext::VoidReturnContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t tlangParser::VoidReturnContext::getRuleIndex() const {
  return tlangParser::RuleVoidReturn;
}


std::any tlangParser::VoidReturnContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitVoidReturn(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::VoidReturnContext* tlangParser::voidReturn() {
  VoidReturnContext *_localctx = _tracker.createInstance<VoidReturnContext>(_ctx, getState());
  enterRule(_localctx, 14, tlangParser::RuleVoidReturn);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(105);
    match(tlangParser::T__4);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ValueReturnContext ------------------------------------------------------------------

tlangParser::ValueReturnContext::ValueReturnContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tlangParser::ExpressionContext* tlangParser::ValueReturnContext::expression() {
  return getRuleContext<tlangParser::ExpressionContext>(0);
}


size_t tlangParser::ValueReturnContext::getRuleIndex() const {
  return tlangParser::RuleValueReturn;
}


std::any tlangParser::ValueReturnContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitValueReturn(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ValueReturnContext* tlangParser::valueReturn() {
  ValueReturnContext *_localctx = _tracker.createInstance<ValueReturnContext>(_ctx, getState());
  enterRule(_localctx, 16, tlangParser::RuleValueReturn);

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
    match(tlangParser::T__5);
    setState(108);
    expression(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ParametersDeclarationContext ------------------------------------------------------------------

tlangParser::ParametersDeclarationContext::ParametersDeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> tlangParser::ParametersDeclarationContext::VAR() {
  return getTokens(tlangParser::VAR);
}

tree::TerminalNode* tlangParser::ParametersDeclarationContext::VAR(size_t i) {
  return getToken(tlangParser::VAR, i);
}


size_t tlangParser::ParametersDeclarationContext::getRuleIndex() const {
  return tlangParser::RuleParametersDeclaration;
}


std::any tlangParser::ParametersDeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitParametersDeclaration(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ParametersDeclarationContext* tlangParser::parametersDeclaration() {
  ParametersDeclarationContext *_localctx = _tracker.createInstance<ParametersDeclarationContext>(_ctx, getState());
  enterRule(_localctx, 18, tlangParser::RuleParametersDeclaration);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(122);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 5, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(110);
      match(tlangParser::T__6);
      setState(111);
      match(tlangParser::T__7);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(112);
      match(tlangParser::T__6);
      setState(113);
      match(tlangParser::VAR);
      setState(118);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == tlangParser::T__8) {
        setState(114);
        match(tlangParser::T__8);
        setState(115);
        match(tlangParser::VAR);
        setState(120);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(121);
      match(tlangParser::T__7);
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

//----------------- ParameterCallContext ------------------------------------------------------------------

tlangParser::ParameterCallContext::ParameterCallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tlangParser::ExpressionContext *> tlangParser::ParameterCallContext::expression() {
  return getRuleContexts<tlangParser::ExpressionContext>();
}

tlangParser::ExpressionContext* tlangParser::ParameterCallContext::expression(size_t i) {
  return getRuleContext<tlangParser::ExpressionContext>(i);
}


size_t tlangParser::ParameterCallContext::getRuleIndex() const {
  return tlangParser::RuleParameterCall;
}


std::any tlangParser::ParameterCallContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitParameterCall(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ParameterCallContext* tlangParser::parameterCall() {
  ParameterCallContext *_localctx = _tracker.createInstance<ParameterCallContext>(_ctx, getState());
  enterRule(_localctx, 20, tlangParser::RuleParameterCall);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(137);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 7, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(124);
      match(tlangParser::T__6);
      setState(125);
      match(tlangParser::T__7);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(126);
      match(tlangParser::T__6);
      setState(127);
      expression(0);
      setState(132);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == tlangParser::T__8) {
        setState(128);
        match(tlangParser::T__8);
        setState(129);
        expression(0);
        setState(134);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(135);
      match(tlangParser::T__7);
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

//----------------- VoidFuncCallContext ------------------------------------------------------------------

tlangParser::VoidFuncCallContext::VoidFuncCallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::VoidFuncCallContext::NAME() {
  return getToken(tlangParser::NAME, 0);
}

tlangParser::ParameterCallContext* tlangParser::VoidFuncCallContext::parameterCall() {
  return getRuleContext<tlangParser::ParameterCallContext>(0);
}


size_t tlangParser::VoidFuncCallContext::getRuleIndex() const {
  return tlangParser::RuleVoidFuncCall;
}


std::any tlangParser::VoidFuncCallContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitVoidFuncCall(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::VoidFuncCallContext* tlangParser::voidFuncCall() {
  VoidFuncCallContext *_localctx = _tracker.createInstance<VoidFuncCallContext>(_ctx, getState());
  enterRule(_localctx, 22, tlangParser::RuleVoidFuncCall);

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
    match(tlangParser::T__9);
    setState(140);
    match(tlangParser::NAME);
    setState(141);
    parameterCall();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ValueFuncCallContext ------------------------------------------------------------------

tlangParser::ValueFuncCallContext::ValueFuncCallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* tlangParser::ValueFuncCallContext::NAME() {
  return getToken(tlangParser::NAME, 0);
}

tlangParser::ParameterCallContext* tlangParser::ValueFuncCallContext::parameterCall() {
  return getRuleContext<tlangParser::ParameterCallContext>(0);
}


size_t tlangParser::ValueFuncCallContext::getRuleIndex() const {
  return tlangParser::RuleValueFuncCall;
}


std::any tlangParser::ValueFuncCallContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitValueFuncCall(this);
  else
    return visitor->visitChildren(this);
}

tlangParser::ValueFuncCallContext* tlangParser::valueFuncCall() {
  ValueFuncCallContext *_localctx = _tracker.createInstance<ValueFuncCallContext>(_ctx, getState());
  enterRule(_localctx, 24, tlangParser::RuleValueFuncCall);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(143);
    match(tlangParser::T__10);
    setState(144);
    match(tlangParser::NAME);
    setState(145);
    parameterCall();
   
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

tlangParser::VoidFuncCallContext* tlangParser::InstructionContext::voidFuncCall() {
  return getRuleContext<tlangParser::VoidFuncCallContext>(0);
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
  enterRule(_localctx, 26, tlangParser::RuleInstruction);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(155);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case tlangParser::VAR: {
        enterOuterAlt(_localctx, 1);
        setState(147);
        assignment();
        break;
      }

      case tlangParser::T__11: {
        enterOuterAlt(_localctx, 2);
        setState(148);
        conditional();
        break;
      }

      case tlangParser::T__15: {
        enterOuterAlt(_localctx, 3);
        setState(149);
        loop();
        break;
      }

      case tlangParser::T__18:
      case tlangParser::T__19:
      case tlangParser::T__20:
      case tlangParser::T__21: {
        enterOuterAlt(_localctx, 4);
        setState(150);
        moveCommand();
        break;
      }

      case tlangParser::T__22:
      case tlangParser::T__23: {
        enterOuterAlt(_localctx, 5);
        setState(151);
        penCommand();
        break;
      }

      case tlangParser::T__16: {
        enterOuterAlt(_localctx, 6);
        setState(152);
        gotoCommand();
        break;
      }

      case tlangParser::T__24: {
        enterOuterAlt(_localctx, 7);
        setState(153);
        pauseCommand();
        break;
      }

      case tlangParser::T__9: {
        enterOuterAlt(_localctx, 8);
        setState(154);
        voidFuncCall();
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
  enterRule(_localctx, 28, tlangParser::RuleConditional);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(159);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 9, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(157);
      ifConditional();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(158);
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
  enterRule(_localctx, 30, tlangParser::RuleIfConditional);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(161);
    match(tlangParser::T__11);
    setState(162);
    condition(0);
    setState(163);
    match(tlangParser::T__12);
    setState(164);
    strict_ilist();
    setState(165);
    match(tlangParser::T__13);
   
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
  enterRule(_localctx, 32, tlangParser::RuleIfElseConditional);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(167);
    match(tlangParser::T__11);
    setState(168);
    condition(0);
    setState(169);
    match(tlangParser::T__12);
    setState(170);
    strict_ilist();
    setState(171);
    match(tlangParser::T__13);
    setState(172);
    match(tlangParser::T__14);
    setState(173);
    match(tlangParser::T__12);
    setState(174);
    strict_ilist();
    setState(175);
    match(tlangParser::T__13);
   
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
  enterRule(_localctx, 34, tlangParser::RuleLoop);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(177);
    match(tlangParser::T__15);
    setState(178);
    value();
    setState(179);
    match(tlangParser::T__12);
    setState(180);
    strict_ilist();
    setState(181);
    match(tlangParser::T__13);
   
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
  enterRule(_localctx, 36, tlangParser::RuleGotoCommand);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(183);
    match(tlangParser::T__16);
    setState(184);
    match(tlangParser::T__6);
    setState(185);
    expression(0);
    setState(186);
    match(tlangParser::T__8);
    setState(187);
    expression(0);
    setState(188);
    match(tlangParser::T__7);
   
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
  enterRule(_localctx, 38, tlangParser::RuleAssignment);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(190);
    match(tlangParser::VAR);
    setState(191);
    match(tlangParser::T__17);
    setState(192);
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
  enterRule(_localctx, 40, tlangParser::RuleMoveCommand);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(194);
    moveOp();
    setState(195);
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
  enterRule(_localctx, 42, tlangParser::RuleMoveOp);
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
    setState(197);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 7864320) != 0))) {
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
  enterRule(_localctx, 44, tlangParser::RulePenCommand);
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
    setState(199);
    _la = _input->LA(1);
    if (!(_la == tlangParser::T__22

    || _la == tlangParser::T__23)) {
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
  enterRule(_localctx, 46, tlangParser::RulePauseCommand);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(201);
    match(tlangParser::T__24);
   
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
//----------------- FuncExprContext ------------------------------------------------------------------

tlangParser::ValueFuncCallContext* tlangParser::FuncExprContext::valueFuncCall() {
  return getRuleContext<tlangParser::ValueFuncCallContext>(0);
}

tlangParser::FuncExprContext::FuncExprContext(ExpressionContext *ctx) { copyFrom(ctx); }


std::any tlangParser::FuncExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<tlangVisitor*>(visitor))
    return parserVisitor->visitFuncExpr(this);
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
  size_t startState = 48;
  enterRecursionRule(_localctx, 48, tlangParser::RuleExpression, precedence);

    

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
    setState(213);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case tlangParser::MINUS: {
        _localctx = _tracker.createInstance<UnaryExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;

        setState(204);
        unaryArithOp();
        setState(205);
        expression(6);
        break;
      }

      case tlangParser::NUM:
      case tlangParser::VAR: {
        _localctx = _tracker.createInstance<ValueExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;
        setState(207);
        value();
        break;
      }

      case tlangParser::T__6: {
        _localctx = _tracker.createInstance<ParenExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;
        setState(208);
        match(tlangParser::T__6);
        setState(209);
        expression(0);
        setState(210);
        match(tlangParser::T__7);
        break;
      }

      case tlangParser::T__10: {
        _localctx = _tracker.createInstance<FuncExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;
        setState(212);
        valueFuncCall();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
    _ctx->stop = _input->LT(-1);
    setState(225);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 12, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        setState(223);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 11, _ctx)) {
        case 1: {
          auto newContext = _tracker.createInstance<MulExprContext>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(215);

          if (!(precpred(_ctx, 5))) throw FailedPredicateException(this, "precpred(_ctx, 5)");
          setState(216);
          multiplicative();
          setState(217);
          expression(6);
          break;
        }

        case 2: {
          auto newContext = _tracker.createInstance<AddExprContext>(_tracker.createInstance<ExpressionContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpression);
          setState(219);

          if (!(precpred(_ctx, 4))) throw FailedPredicateException(this, "precpred(_ctx, 4)");
          setState(220);
          additive();
          setState(221);
          expression(5);
          break;
        }

        default:
          break;
        } 
      }
      setState(227);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 12, _ctx);
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
  enterRule(_localctx, 50, tlangParser::RuleMultiplicative);
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
    setState(228);
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
  enterRule(_localctx, 52, tlangParser::RuleAdditive);
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
    setState(230);
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
  enterRule(_localctx, 54, tlangParser::RuleUnaryArithOp);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(232);
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
  size_t startState = 56;
  enterRecursionRule(_localctx, 56, tlangParser::RuleCondition, precedence);

    

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
    setState(246);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 13, _ctx)) {
    case 1: {
      setState(235);
      match(tlangParser::NOT);
      setState(236);
      condition(5);
      break;
    }

    case 2: {
      setState(237);
      expression(0);
      setState(238);
      binCondOp();
      setState(239);
      expression(0);
      break;
    }

    case 3: {
      setState(241);
      match(tlangParser::PENCOND);
      break;
    }

    case 4: {
      setState(242);
      match(tlangParser::T__6);
      setState(243);
      condition(0);
      setState(244);
      match(tlangParser::T__7);
      break;
    }

    default:
      break;
    }
    _ctx->stop = _input->LT(-1);
    setState(254);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 14, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        _localctx = _tracker.createInstance<ConditionContext>(parentContext, parentState);
        pushNewRecursionContext(_localctx, startState, RuleCondition);
        setState(248);

        if (!(precpred(_ctx, 3))) throw FailedPredicateException(this, "precpred(_ctx, 3)");
        setState(249);
        logicOp();
        setState(250);
        condition(4); 
      }
      setState(256);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 14, _ctx);
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
  enterRule(_localctx, 58, tlangParser::RuleBinCondOp);
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
    setState(257);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 135291469824) != 0))) {
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
  enterRule(_localctx, 60, tlangParser::RuleLogicOp);
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
    setState(259);
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
  enterRule(_localctx, 62, tlangParser::RuleValue);
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
    setState(261);
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
    case 24: return expressionSempred(antlrcpp::downCast<ExpressionContext *>(context), predicateIndex);
    case 28: return conditionSempred(antlrcpp::downCast<ConditionContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool tlangParser::expressionSempred(ExpressionContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return precpred(_ctx, 5);
    case 1: return precpred(_ctx, 4);

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
