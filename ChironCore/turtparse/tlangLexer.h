
// Generated from tlang.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  tlangLexer : public antlr4::Lexer {
public:
  enum {
    T__0 = 1, T__1 = 2, T__2 = 3, T__3 = 4, T__4 = 5, T__5 = 6, T__6 = 7, 
    T__7 = 8, T__8 = 9, T__9 = 10, T__10 = 11, T__11 = 12, T__12 = 13, T__13 = 14, 
    T__14 = 15, T__15 = 16, T__16 = 17, PLUS = 18, MINUS = 19, MUL = 20, 
    DIV = 21, PENCOND = 22, LT = 23, GT = 24, EQ = 25, NEQ = 26, LTE = 27, 
    GTE = 28, AND = 29, OR = 30, NOT = 31, NUM = 32, VAR = 33, NAME = 34, 
    Whitespace = 35
  };

  explicit tlangLexer(antlr4::CharStream *input);

  ~tlangLexer() override;


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.

  // Individual semantic predicate functions triggered by sempred() above.

};

