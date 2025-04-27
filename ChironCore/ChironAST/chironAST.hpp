#pragma once

#include <algorithm>
#include <memory>
#include <string>
#include <vector>

#include <llvm/IR/Value.h>
#include <llvm/IR/Function.h>
#include <llvm/Support/raw_ostream.h>

// Base class for all instructions in the AST
class InstrAST {
public:
    virtual ~InstrAST() = default;

    // Pure virtual function to generate LLVM IR for the instruction
    virtual llvm::Value* codegen() = 0;
};

// Base class for all expressions in the AST
class ExpressionAST : public InstrAST {
public:
    virtual ~ExpressionAST() = default;
};

// Represents a numeric constant in the AST
class NumberExpressionAST : public ExpressionAST {
    int val; // Value of the numeric constant

public:
    NumberExpressionAST(int val) : 
        val(val) {}

    // Generate LLVM IR for the numeric constant
    llvm::Value* codegen() override;

    // Getter for the numeric value
    int getVal() {
        return val;
    }
};

// Represents a variable in the AST
class VariableExpressionAST : public ExpressionAST {
    std::string name; // Name of the variable

public:
    VariableExpressionAST(const std::string &Name) : 
        name(Name) {}

    // Clone method to create a copy of the variable (useful for loops)
    std::unique_ptr<VariableExpressionAST> clone() {
        return std::make_unique<VariableExpressionAST>(name);
    }

    // Generate LLVM IR for the variable
    llvm::Value *codegen() override;

    // Getter for the variable name
    const std::string &getName() const {
        return name;
    }
};

// Represents a binary arithmetic operation in the AST
class BinArithExpressionAST : public ExpressionAST {
    char op; // Operator (e.g., '+', '-', '*', '/')
    std::unique_ptr<ExpressionAST> LHS, RHS; // Left-hand side and right-hand side expressions

public:
    BinArithExpressionAST(char op, std::unique_ptr<ExpressionAST> LHS, std::unique_ptr<ExpressionAST> RHS) :
        op(op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}

    // Generate LLVM IR for the binary arithmetic operation
    llvm::Value* codegen() override; 
};

// Represents a unary arithmetic operation in the AST
class UnaryArithExpressionAST : public ExpressionAST {
    char op; // Operator (e.g., '-')
    std::unique_ptr<ExpressionAST> RHS; // Right-hand side expression

public:
    UnaryArithExpressionAST(char op, std::unique_ptr<ExpressionAST> RHS) :
        op(op), RHS(std::move(RHS)) {}

    // Generate LLVM IR for the unary arithmetic operation
    llvm::Value* codegen() override; 
};

// Represents a binary conditional operation in the AST
class BinCondExpressionAST : public ExpressionAST {
    std::string op; // Operator (e.g., '==', '<', '>')
    std::unique_ptr<ExpressionAST> LHS, RHS; // Left-hand side and right-hand side expressions

public:
    BinCondExpressionAST(std::string op, std::unique_ptr<ExpressionAST> LHS, std::unique_ptr<ExpressionAST> RHS) :
        op(op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}

    // Generate LLVM IR for the binary conditional operation
    llvm::Value* codegen() override;
};

// Represents a function call in the AST
class CallExpressionAST : public ExpressionAST {
    std::string callee; // Name of the function being called
    std::vector<std::unique_ptr<ExpressionAST>> args; // Arguments to the function

public:
    CallExpressionAST(const std::string& callee, std::vector<std::unique_ptr<ExpressionAST>> args) :
        callee(callee), args(std::move(args)) {}

    // Generate LLVM IR for the function call
    llvm::Value* codegen() override;
};

// Represents a "pen" operation in the AST (e.g., pen up/down)
class PenCallExprAST : public ExpressionAST {
    bool status; // Status of the pen (true for down, false for up)

public:
    PenCallExprAST(bool status) :
        status(status) {}

    // Generate LLVM IR for the pen operation
    llvm::Value* codegen() override;
};

// Represents a "goto" operation in the AST
class GotoCallExprAST : public ExpressionAST {
    std::unique_ptr<ExpressionAST> x, y; // Coordinates for the "goto" operation

public:
    GotoCallExprAST(std::unique_ptr<ExpressionAST> x, std::unique_ptr<ExpressionAST> y) :
        x(std::move(x)), y(std::move(y)) {}

    // Generate LLVM IR for the "goto" operation
    llvm::Value* codegen() override;
};

// Represents a "move" operation in the AST
class MoveCallExprAST : public ExpressionAST {
    std::string direction; // Direction of movement (e.g., "left", "forward")
    std::unique_ptr<ExpressionAST> val; // Distance/Angle to move

public:
    MoveCallExprAST(const std::string& direction, std::unique_ptr<ExpressionAST> val) :
        direction(direction), val(std::move(val)) {}

    // Generate LLVM IR for the "move" operation
    llvm::Value* codegen() override;
};

// Represents an "if" statement in the AST
class IfExpressionAST : public ExpressionAST {
    std::unique_ptr<ExpressionAST> condition; // Condition for the "if" statement
    std::vector<std::unique_ptr<InstrAST>> thenBlock; // Instructions for the "then" block
    std::vector<std::unique_ptr<InstrAST>> elseBlock; // Instructions for the "else" block

public:
    IfExpressionAST(std::unique_ptr<ExpressionAST> condition, std::vector<std::unique_ptr<InstrAST>> thenBlock, std::vector<std::unique_ptr<InstrAST>> elseBlock) :
        condition(std::move(condition)), thenBlock(std::move(thenBlock)), elseBlock(std::move(elseBlock)) {}

    // Generate LLVM IR for the "if" statement
    llvm::Value* codegen() override;
};

// Represents a "loop" statement in the AST
class LoopExpressionAST : public ExpressionAST {
    std::unique_ptr<ExpressionAST> repCounter; // Number of repetitions
    std::string varname; // Loop counter variable name
    std::vector<std::unique_ptr<InstrAST>> body; // Instructions inside the loop

public:
    LoopExpressionAST(std::unique_ptr<ExpressionAST> repCounter, const std::string& varname, std::vector<std::unique_ptr<InstrAST>> body) :
        repCounter(std::move(repCounter)), varname(varname), body(std::move(body)) {}

    // Generate LLVM IR for the "loop" statement
    llvm::Value* codegen() override;
};

// Represents a function definition in the AST
class FunctionAST : public InstrAST {
    std::string name; // Name of the function
    std::vector<std::string> args; // Arguments of the function
    std::vector<std::unique_ptr<InstrAST>> body; // Instructions inside the function
    std::unique_ptr<ExpressionAST> returnValue; // Return value of the function
    bool isVoid; // Whether the function is void (no return value)

public:
    FunctionAST(const std::string& name, std::vector<std::string> args, std::vector<std::unique_ptr<InstrAST>> body, std::unique_ptr<ExpressionAST> returnValue, bool isVoid) :
        name(name), args(std::move(args)), body(std::move(body)), returnValue(std::move(returnValue)), isVoid(isVoid) {}

    // Generate LLVM IR for the function
    llvm::Value* codegen() override;

    // Getter for the function name
    const std::string& getName() const {
        return name;
    }
};