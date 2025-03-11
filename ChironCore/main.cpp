#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include "ChironAST/chironAST.hpp"

#include "antlr4-runtime.h"
#include "turtparse/tlangLexer.h"
#include "turtparse/tlangParser.h"
#include "turtparse/tlangBaseVisitor.h"

extern tlangVisitor* createChironVisitor();

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input file>\n";
        return 1;
    }
    std::string filename = argv[1];

    std::ifstream file(filename);
    if (!file) {
        std::cerr << "Error: Cannot open file " << filename << "\n";
        return 1;
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string input_str = buffer.str();

    antlr4::ANTLRInputStream input(input_str);
    tlangLexer lexer(&input);
    antlr4::CommonTokenStream tokens(&lexer);
    tlangParser parser(&tokens);
    
   
    tlangParser::StartContext *ctx = parser.start();
    if (!ctx) {
        std::cerr << "Error: Failed to parse input.\n";
        return 1;
    }

    
    tlangVisitor* visitor = createChironVisitor();

    // Since our visitor returns a vector of raw pointers, update the type accordingly.
    std::vector<InstrAST*> instructions = std::any_cast<std::vector<InstrAST*>>(visitor->visitStart(ctx));

   
    for (auto instr : instructions) {
        llvm::Value* val = instr->codegen();
        if (val) {
            val->print(llvm::errs());
            llvm::errs() << "\n";
        }
    }

    // Clean up the AST nodes (to avoid memory leaks).
    for (auto instr : instructions) {
        delete instr;
    }
    delete visitor;
    
    return 0;
}
