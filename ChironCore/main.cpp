#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

#include "chironAST.hpp"

#include "antlr4-runtime.h"
#include "tlangLexer.h"
#include "tlangParser.h"
#include "tlangBaseVisitor.h"

extern tlangVisitor* createChironVisitor();
extern void IntializeModule();
extern void InitializeMainFunction();
extern void ConverIRtoObjectFile();

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
    
    std::any result = visitor->visitStart(ctx);

    try {
        std::vector<InstrAST*> instructions = std::any_cast<std::vector<InstrAST*>>(result);
        
        IntializeModule();
        InitializeMainFunction();

        for (auto instr : instructions) {
            llvm::Value* val = instr->codegen();
        }

        ConverIRtoObjectFile();

        for (auto instr : instructions) {
            delete instr;
        }
        delete visitor;

    } catch (const std::bad_any_cast& e) {
        std::cerr << "Error: " << e.what() << " (bad_any_cast)\n";
        return 1;
    }

    return 0;
}
