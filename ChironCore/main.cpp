// #include <iostream>
// #include <fstream>
// #include <sstream>
// #include <string>
// #include <vector>

// #include "ChironAST/chironAST.hpp"

// #include "antlr4-runtime.h"
// #include "turtparse/tlangLexer.h"
// #include "turtparse/tlangParser.h"
// #include "turtparse/tlangBaseVisitor.h"

// extern tlangVisitor* createChironVisitor();

// extern std::unique_ptr<tlangVisitor> ChironVisitorImpl();
// extern void IntializeModule();
// extern void TempFunction();
// extern void tempPrint();

// int main(int argc, char *argv[]) {
//     if (argc < 2) {
//         std::cerr << "Usage: " << argv[0] << " <input file>\n";
//         return 1;
//     }
//     std::string filename = argv[1];

    
//     std::ifstream file(filename);
//     if (!file) {
//         std::cerr << "Error: Cannot open file " << filename << "\n";
//         return 1;
//     }
//     std::stringstream buffer;
//     buffer << file.rdbuf();
//     std::string input_str = buffer.str();
    
//     antlr4::ANTLRInputStream input(input_str);
//     tlangLexer lexer(&input);
//     antlr4::CommonTokenStream tokens(&lexer);
//     tlangParser parser(&tokens);
    
    
//     tlangParser::StartContext *ctx = parser.start();
//     if (!ctx) {
//         std::cerr << "Error: Failed to parse input.\n";
//         return 1;
//     }
    
    
//     tlangVisitor* visitor = createChironVisitor();
    
//     // extra Since our visitor returns a vector of raw pointers, update the type accordingly.
//     std::any result = visitor->visitStart(ctx);
//     std::cerr << "Result type: " << result.type().name() << std::endl;
//     // extra end 

//     std::vector<InstrAST*> instructions = std::any_cast<std::vector<InstrAST*>>(visitor->visitStart(ctx));

   
   
//     IntializeModule();
//     TempFunction();

//     for (auto instr : instructions) {
//         llvm::Value* val = instr->codegen();
//     }

//     tempPrint();

//     // Clean up the AST nodes (to avoid memory leaks).
//     for (auto instr : instructions) {
//         delete instr;
//     }
//     delete visitor;

//     auto instr_ptr = std::any_cast<std::vector<InstrAST*>*>(&result);
//     if (instr_ptr) {
//         auto& instructions = *instr_ptr;
//         // Now safely use `instructions`
//     } else {
//         std::cerr << "Bad any cast!" << std::endl;
//     }
    
//     return 0;
// }
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

extern std::unique_ptr<tlangVisitor> ChironVisitorImpl();
extern void IntializeModule();
extern void TempFunction();
extern void tempPrint();

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
    
    // added to check if if visitor is returning a vector or not.
    std::any result = visitor->visitStart(ctx);
    //std::cerr << "Result type: " << result.type().name() << std::endl;

    try {
        std::vector<InstrAST*> instructions = std::any_cast<std::vector<InstrAST*>>(result);
        
        IntializeModule();
        TempFunction();

        for (auto instr : instructions) {
            llvm::Value* val = instr->codegen();
        }

        tempPrint();

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
