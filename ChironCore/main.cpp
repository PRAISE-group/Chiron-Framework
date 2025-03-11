#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <chironAST.hpp>

#include "antlr4-runtime.h"
#include "tlangLexer.h"
#include "tlangParser.h"
#include "tlangBaseVisitor.h"

int main(int argc, char *argv[]) {
    std::string filename = argv[1];

    std::ifstream file(filename);
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string input_str = buffer.str();

    antlr4::ANTLRInputStream input(input_str);
    tlangLexer lexer(&input);
    antlr4::CommonTokenStream tokens(&lexer);

    tlangParser parser(&tokens);
    antlr4::tree::ParseTree *tree = parser.start();

    tlangParser::StartContext *ctx = parser.start();

    tlangBaseVisitor visitor;

    std::vector<std::unique_ptr<InstrAST>> instructions = std::any_cast<std::vector<std::unique_ptr<InstrAST>>>(visitor.visitStart(ctx));

    for (auto &instr : instructions) {
        llvm::Value *val = instr->codegen();
        if (val) {
            val->print(llvm::errs());
            llvm::errs() << "\n";
        }
    }
}