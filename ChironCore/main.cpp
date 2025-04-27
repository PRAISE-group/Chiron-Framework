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

// External declarations for functions and variables used in the program
extern tlangVisitor* createChironVisitor();
extern void IntializeModule();
extern void InitializeMainFunction();
extern bool optim;
extern void ConverIRtoObjectFile(const std::string& output_filename, bool run_output, bool dump_ir, bool print_ir);

int main(int argc, char *argv[]) {
    // Check if the required number of arguments is provided
    if (argc < 7) {
        std::cerr << "Usage: " << argv[0] << " <input file> <output file> <run output> <dump ir> <print ir> [<var name> <var value>]...\n";
        return -1;
    }
    
    // Parse command-line arguments
    std::string input_filename = argv[1];
    std::string output_filename = argv[2];
    bool run_output = argv[3][0] == '1'; // Convert '1' or '0' to boolean
    bool dump_ir = argv[4][0] == '1';
    bool print_ir = argv[5][0] == '1';
    optim = argv[6][0] == '1'; // Set optimization flag

    // Parse variable initializations from command-line arguments
    std::vector<std::pair<std::string, int>> initialized_values;
    for (int i = 7; i < argc; i += 2) {
        if (i + 1 >= argc) {
            std::cerr << "Error: Missing value for variable " << argv[i] << "\n";
            return -1;
        }
        initialized_values.push_back({argv[i], std::stoi(argv[i + 1])});
    }
    
    // Read the input file
    std::ifstream file(input_filename);
    if (!file) {
        std::cerr << "Error: Cannot open file " << input_filename << "\n";
        return 1;
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string input_str = buffer.str();
    
    // Use ANTLR to tokenize and parse the input
    antlr4::ANTLRInputStream input(input_str);
    tlangLexer lexer(&input);
    antlr4::CommonTokenStream tokens(&lexer);
    tlangParser parser(&tokens);
    
    // Parse the input using the start rule
    tlangParser::StartContext *ctx = parser.start();
    if (!ctx) {
        std::cerr << "Error: Failed to parse input.\n";
        return -1;
    }
    
    // Create a visitor to process the parsed input
    tlangVisitor* visitor = createChironVisitor();
    std::any result = visitor->visitStart(ctx);
    
    try {
        // Generate instructions for variable initializations
        std::vector<InstrAST*> instructions;
        for (const auto& pair : initialized_values) {
            std::string var_name = pair.first;
            int var_value = pair.second;
            instructions.push_back(
                new BinArithExpressionAST(
                    '=', // Assignment operation
                    std::make_unique<VariableExpressionAST>(var_name),
                    std::make_unique<NumberExpressionAST>(var_value)
                )
            );
        }
        
        // Append instructions generated from the parsed AST
        std::vector<InstrAST*> ast = std::any_cast<std::vector<InstrAST*>>(result);
        instructions.insert(instructions.end(), ast.begin(), ast.end());
        
        // Initialize LLVM module and main function
        IntializeModule();
        InitializeMainFunction();

        // Generate LLVM IR for each instruction
        for (auto instr : instructions) {
            llvm::Value* val = instr->codegen();
        }

        // Convert the generated IR to an object file
        ConverIRtoObjectFile(output_filename, run_output, dump_ir, print_ir);
        
        // Clean up dynamically allocated memory
        for (auto instr : instructions) {
            delete instr;
        }
        delete visitor;
        
    } catch (const std::exception& e) {
        // Handle standard exceptions
        std::cerr << "Error: " << e.what() << "\n";
        return -1;
    } catch (...) {
        // Handle unknown exceptions
        std::cerr << "Unknown error occurred.\n";
        return -1;
    }
    
    // Close the input file
    file.close();
    
    return 0; // Exit successfully
}
