#pragma once

#include <algorithm>
#include <memory>
#include <string>
#include <vector>

#include "llvm/IR/Value.h"
#include "llvm/Support/raw_ostream.h"

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

    int getVal() {
        return val;
    }
};

class VariableExpressionAST : public ExpressionAST {
    std::string name;

public:
    VariableExpressionAST(const std::string &Name) : 
        name(Name) {}
    // Adding to handle loop counter variable - clone method
    std::unique_ptr<VariableExpressionAST> clone() {
        return std::make_unique<VariableExpressionAST>(name);
    }

    llvm::Value *codegen() override;

    const std::string &getName() const {
        return name;
    }
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
    std::unique_ptr<ExpressionAST> x, y;

public:
    GotoCallExprAST(std::unique_ptr<ExpressionAST> x, std::unique_ptr<ExpressionAST> y) :
        x(std::move(x)), y(std::move(y)) {}

    llvm::Value* codegen() override;
};

class MoveCallExprAST : public ExpressionAST {
    std::string direction;
    std::unique_ptr<ExpressionAST> val;

public:
    MoveCallExprAST(const std::string& direction, std::unique_ptr<ExpressionAST> val) :
        direction(direction), val(std::move(val)) {}

    llvm::Value* codegen() override;
};

class IfExpressionAST : public ExpressionAST {
    std::unique_ptr<ExpressionAST> condition;
    std::vector<std::unique_ptr<InstrAST>> thenBlock;
    std::vector<std::unique_ptr<InstrAST>> elseBlock;

public:
    IfExpressionAST(std::unique_ptr<ExpressionAST> condition, std::vector<std::unique_ptr<InstrAST>> thenBlock, std::vector<std::unique_ptr<InstrAST>> elseBlock) :
        condition(std::move(condition)), thenBlock(std::move(thenBlock)), elseBlock(std::move(elseBlock)) {}

    llvm::Value* codegen() override;
};

class LoopExpressionAST : public ExpressionAST {
    int repCounter;
    std::string varname;
    std::vector<std::unique_ptr<InstrAST>> body;

public:
    LoopExpressionAST(int repCounter, std::string varname, std::vector<std::unique_ptr<InstrAST>> body) :
        repCounter(repCounter), varname(varname), body(std::move(body)) {}

    llvm::Value* codegen() override;
};