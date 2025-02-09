
// Generated from tlang.g4 by ANTLR 4.13.2


#include "tlangLexer.h"


using namespace antlr4;



using namespace antlr4;

namespace {

struct TlangLexerStaticData final {
  TlangLexerStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  TlangLexerStaticData(const TlangLexerStaticData&) = delete;
  TlangLexerStaticData(TlangLexerStaticData&&) = delete;
  TlangLexerStaticData& operator=(const TlangLexerStaticData&) = delete;
  TlangLexerStaticData& operator=(TlangLexerStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag tlanglexerLexerOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<TlangLexerStaticData> tlanglexerLexerStaticData = nullptr;

void tlanglexerLexerInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (tlanglexerLexerStaticData != nullptr) {
    return;
  }
#else
  assert(tlanglexerLexerStaticData == nullptr);
#endif
  auto staticData = std::make_unique<TlangLexerStaticData>(
    std::vector<std::string>{
      "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
      "T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "T__16", 
      "PLUS", "MINUS", "MUL", "DIV", "PENCOND", "LT", "GT", "EQ", "NEQ", 
      "LTE", "GTE", "AND", "OR", "NOT", "NUM", "VAR", "NAME", "Whitespace"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
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
  	4,0,35,217,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,
  	7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,7,33,2,34,7,34,1,0,
  	1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,
  	4,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,10,
  	1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
  	1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,14,1,14,1,14,
  	1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,16,1,16,1,16,
  	1,16,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,1,21,1,21,1,21,
  	1,21,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,1,24,1,25,
  	1,25,1,25,1,26,1,26,1,26,1,27,1,27,1,27,1,28,1,28,1,28,1,29,1,29,1,29,
  	1,30,1,30,1,31,4,31,194,8,31,11,31,12,31,195,1,32,1,32,1,32,5,32,201,
  	8,32,10,32,12,32,204,9,32,1,33,4,33,207,8,33,11,33,12,33,208,1,34,4,34,
  	212,8,34,11,34,12,34,213,1,34,1,34,0,0,35,1,1,3,2,5,3,7,4,9,5,11,6,13,
  	7,15,8,17,9,19,10,21,11,23,12,25,13,27,14,29,15,31,16,33,17,35,18,37,
  	19,39,20,41,21,43,22,45,23,47,24,49,25,51,26,53,27,55,28,57,29,59,30,
  	61,31,63,32,65,33,67,34,69,35,1,0,5,1,0,48,57,3,0,65,90,95,95,97,122,
  	3,0,48,57,65,90,97,122,2,0,65,90,97,122,3,0,9,10,13,13,32,32,220,0,1,
  	1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,
  	0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,
  	1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,
  	0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,
  	0,45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,0,55,
  	1,0,0,0,0,57,1,0,0,0,0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,0,
  	0,0,0,67,1,0,0,0,0,69,1,0,0,0,1,71,1,0,0,0,3,74,1,0,0,0,5,76,1,0,0,0,
  	7,78,1,0,0,0,9,83,1,0,0,0,11,90,1,0,0,0,13,95,1,0,0,0,15,97,1,0,0,0,17,
  	99,1,0,0,0,19,101,1,0,0,0,21,103,1,0,0,0,23,111,1,0,0,0,25,120,1,0,0,
  	0,27,125,1,0,0,0,29,131,1,0,0,0,31,137,1,0,0,0,33,145,1,0,0,0,35,151,
  	1,0,0,0,37,153,1,0,0,0,39,155,1,0,0,0,41,157,1,0,0,0,43,159,1,0,0,0,45,
  	168,1,0,0,0,47,170,1,0,0,0,49,172,1,0,0,0,51,175,1,0,0,0,53,178,1,0,0,
  	0,55,181,1,0,0,0,57,184,1,0,0,0,59,187,1,0,0,0,61,190,1,0,0,0,63,193,
  	1,0,0,0,65,197,1,0,0,0,67,206,1,0,0,0,69,211,1,0,0,0,71,72,5,105,0,0,
  	72,73,5,102,0,0,73,2,1,0,0,0,74,75,5,91,0,0,75,4,1,0,0,0,76,77,5,93,0,
  	0,77,6,1,0,0,0,78,79,5,101,0,0,79,80,5,108,0,0,80,81,5,115,0,0,81,82,
  	5,101,0,0,82,8,1,0,0,0,83,84,5,114,0,0,84,85,5,101,0,0,85,86,5,112,0,
  	0,86,87,5,101,0,0,87,88,5,97,0,0,88,89,5,116,0,0,89,10,1,0,0,0,90,91,
  	5,103,0,0,91,92,5,111,0,0,92,93,5,116,0,0,93,94,5,111,0,0,94,12,1,0,0,
  	0,95,96,5,40,0,0,96,14,1,0,0,0,97,98,5,44,0,0,98,16,1,0,0,0,99,100,5,
  	41,0,0,100,18,1,0,0,0,101,102,5,61,0,0,102,20,1,0,0,0,103,104,5,102,0,
  	0,104,105,5,111,0,0,105,106,5,114,0,0,106,107,5,119,0,0,107,108,5,97,
  	0,0,108,109,5,114,0,0,109,110,5,100,0,0,110,22,1,0,0,0,111,112,5,98,0,
  	0,112,113,5,97,0,0,113,114,5,99,0,0,114,115,5,107,0,0,115,116,5,119,0,
  	0,116,117,5,97,0,0,117,118,5,114,0,0,118,119,5,100,0,0,119,24,1,0,0,0,
  	120,121,5,108,0,0,121,122,5,101,0,0,122,123,5,102,0,0,123,124,5,116,0,
  	0,124,26,1,0,0,0,125,126,5,114,0,0,126,127,5,105,0,0,127,128,5,103,0,
  	0,128,129,5,104,0,0,129,130,5,116,0,0,130,28,1,0,0,0,131,132,5,112,0,
  	0,132,133,5,101,0,0,133,134,5,110,0,0,134,135,5,117,0,0,135,136,5,112,
  	0,0,136,30,1,0,0,0,137,138,5,112,0,0,138,139,5,101,0,0,139,140,5,110,
  	0,0,140,141,5,100,0,0,141,142,5,111,0,0,142,143,5,119,0,0,143,144,5,110,
  	0,0,144,32,1,0,0,0,145,146,5,112,0,0,146,147,5,97,0,0,147,148,5,117,0,
  	0,148,149,5,115,0,0,149,150,5,101,0,0,150,34,1,0,0,0,151,152,5,43,0,0,
  	152,36,1,0,0,0,153,154,5,45,0,0,154,38,1,0,0,0,155,156,5,42,0,0,156,40,
  	1,0,0,0,157,158,5,47,0,0,158,42,1,0,0,0,159,160,5,112,0,0,160,161,5,101,
  	0,0,161,162,5,110,0,0,162,163,5,100,0,0,163,164,5,111,0,0,164,165,5,119,
  	0,0,165,166,5,110,0,0,166,167,5,63,0,0,167,44,1,0,0,0,168,169,5,60,0,
  	0,169,46,1,0,0,0,170,171,5,62,0,0,171,48,1,0,0,0,172,173,5,61,0,0,173,
  	174,5,61,0,0,174,50,1,0,0,0,175,176,5,33,0,0,176,177,5,61,0,0,177,52,
  	1,0,0,0,178,179,5,60,0,0,179,180,5,61,0,0,180,54,1,0,0,0,181,182,5,62,
  	0,0,182,183,5,61,0,0,183,56,1,0,0,0,184,185,5,38,0,0,185,186,5,38,0,0,
  	186,58,1,0,0,0,187,188,5,124,0,0,188,189,5,124,0,0,189,60,1,0,0,0,190,
  	191,5,33,0,0,191,62,1,0,0,0,192,194,7,0,0,0,193,192,1,0,0,0,194,195,1,
  	0,0,0,195,193,1,0,0,0,195,196,1,0,0,0,196,64,1,0,0,0,197,198,5,58,0,0,
  	198,202,7,1,0,0,199,201,7,2,0,0,200,199,1,0,0,0,201,204,1,0,0,0,202,200,
  	1,0,0,0,202,203,1,0,0,0,203,66,1,0,0,0,204,202,1,0,0,0,205,207,7,3,0,
  	0,206,205,1,0,0,0,207,208,1,0,0,0,208,206,1,0,0,0,208,209,1,0,0,0,209,
  	68,1,0,0,0,210,212,7,4,0,0,211,210,1,0,0,0,212,213,1,0,0,0,213,211,1,
  	0,0,0,213,214,1,0,0,0,214,215,1,0,0,0,215,216,6,34,0,0,216,70,1,0,0,0,
  	5,0,195,202,208,213,1,6,0,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  tlanglexerLexerStaticData = std::move(staticData);
}

}

tlangLexer::tlangLexer(CharStream *input) : Lexer(input) {
  tlangLexer::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *tlanglexerLexerStaticData->atn, tlanglexerLexerStaticData->decisionToDFA, tlanglexerLexerStaticData->sharedContextCache);
}

tlangLexer::~tlangLexer() {
  delete _interpreter;
}

std::string tlangLexer::getGrammarFileName() const {
  return "tlang.g4";
}

const std::vector<std::string>& tlangLexer::getRuleNames() const {
  return tlanglexerLexerStaticData->ruleNames;
}

const std::vector<std::string>& tlangLexer::getChannelNames() const {
  return tlanglexerLexerStaticData->channelNames;
}

const std::vector<std::string>& tlangLexer::getModeNames() const {
  return tlanglexerLexerStaticData->modeNames;
}

const dfa::Vocabulary& tlangLexer::getVocabulary() const {
  return tlanglexerLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView tlangLexer::getSerializedATN() const {
  return tlanglexerLexerStaticData->serializedATN;
}

const atn::ATN& tlangLexer::getATN() const {
  return *tlanglexerLexerStaticData->atn;
}




void tlangLexer::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  tlanglexerLexerInitialize();
#else
  ::antlr4::internal::call_once(tlanglexerLexerOnceFlag, tlanglexerLexerInitialize);
#endif
}
