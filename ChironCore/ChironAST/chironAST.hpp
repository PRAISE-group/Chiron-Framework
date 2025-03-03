#pragma once

#include "llvm/IR/Value.h"
#include <algorithm>
#include <memory>
#include <string>
#include <vector>

class InstrAST {
public:
    virtual ~InstrAST() = default;

    virtual llvm::Value* codegen() = 0;
};

class ExpressionAST : public InstrAST {
public:
    virtual ~ExpressionAST() = default;
};

class NumberExpressionAST : public ExpressionAST {
    int val;
public:
    NumberExpressionAST(int val) : 
        val(val) {}

    llvm::Value* codegen() override; 
};

class VariableExpressionAST : public ExpressionAST {
    std::string name;

public:
    VariableExpressionAST(const std::string &Name) : 
        name(Name) {}

    llvm::Value *codegen() override;
};

class BinArithExpressionAST : public ExpressionAST {
    char op;
    std::unique_ptr<ExpressionAST> LHS, RHS;

public:
    BinArithExpressionAST(char op, std::unique_ptr<ExpressionAST> LHS, std::unique_ptr<ExpressionAST> RHS) :
        op(op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}

    llvm::Value* codegen() override; 
};

class UnaryArithExpressionAST : public ExpressionAST {
    char op;
    std::unique_ptr<ExpressionAST> RHS;

public:
    UnaryArithExpressionAST(char op, std::unique_ptr<ExpressionAST> RHS) :
        op(op), RHS(std::move(RHS)) {}

    llvm::Value* codegen() override; 
};

class BinCondExpressionAST : public ExpressionAST {
    std::string op;
    std::unique_ptr<ExpressionAST> LHS, RHS;

public:
    BinCondExpressionAST(std::string op, std::unique_ptr<ExpressionAST> LHS, std::unique_ptr<ExpressionAST> RHS) :
        op(op), LHS(std::move(LHS)), RHS(std::move(RHS)) {}

    llvm::Value* codegen() override;
};

class CallExpressionAST : public ExpressionAST {
    std::string callee;
    std::vector<std::unique_ptr<ExpressionAST>> args;

public:
    CallExpressionAST(const std::string& callee, std::vector<std::unique_ptr<ExpressionAST>> args) :
        callee(callee), args(std::move(args)) {}

    llvm::Value* codegen() override;
};

class PenCallExprAST : public ExpressionAST {
    bool status;

public:
    PenCallExprAST(bool status) :
        status(status) {}

    llvm::Value* codegen() override;
};

class GotoCallExprAST : public ExpressionAST {
    int x, y;

public:
    GotoCallExprAST(int x, int y) :
        x(x), y(y) {}

    llvm::Value* codegen() override;
};

class MoveCallExprAST : public ExpressionAST {
    std::string direction;
    std::unique_ptr<ExpressionAST> expr;

public:
    MoveCallExprAST(const std::string& direction, std::unique_ptr<ExpressionAST> expr) :
        direction(direction), expr(std::move(expr)) {}

    llvm::Value* codegen() override;
};