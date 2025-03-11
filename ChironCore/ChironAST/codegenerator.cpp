#include <chironAST.hpp>

#include <map>

#include <llvm/IR/Value.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Type.h>
#include <llvm/IR/IRBuilder.h>

const char MINUS = '-';
const char PLUS = '+';
const char MUL = '*';
const char DIV = '/';
const char NOT = '!';

const std::string LT = "<";
const std::string GT = ">";
const std::string EQ = "==";
const std::string NEQ = "!=";
const std::string LTE = "<=";
const std::string GTE = ">=";

const std::string AND = "&&";
const std::string OR = "||";

static std::unique_ptr<llvm::LLVMContext> CodeGenContext;
static std::unique_ptr<llvm::Module> CodeGenModule;
static std::unique_ptr<llvm::IRBuilder<>> Builder;
static std::map<std::string, llvm::Value*> SymbolTable;

llvm::Value* NumberExpressionAST::codegen() {
    return llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), val);
}

llvm::Value* VariableExpressionAST::codegen() {
    llvm::Value *V = SymbolTable[name];
    if (!V) {
        return nullptr;
    }
    return V;
}

llvm::Value* BinArithExpressionAST::codegen() {
    llvm::Value *L = LHS->codegen();
    llvm::Value *R = RHS->codegen();
    if (!L || !R) {
        return nullptr;
    }
    switch (op) {
        case PLUS:
            return Builder->CreateAdd(L, R, "addtmp");
        case MINUS:
            return Builder->CreateSub(L, R, "subtmp");
        case MUL:
            return Builder->CreateMul(L, R, "multmp");
        case DIV:
            return Builder->CreateSDiv(L, R, "divtmp");
        default:
            return nullptr;
    }
}

llvm::Value* UnaryArithExpressionAST::codegen() {
    llvm::Value *R = RHS->codegen();
    if (!R) {
        return nullptr;
    }
    if (op == MINUS) {
        return Builder->CreateNeg(R, "negtmp");
    } else if (op == NOT) {
        return Builder->CreateNot(R, "nottmp");
    }

    return nullptr;
}

llvm::Value* BinCondExpressionAST::codegen() {
    llvm::Value *L = LHS->codegen();
    llvm::Value *R = RHS->codegen();
    if (!L || !R) {
        return nullptr;
    }
    
    if(op == LT) {
        return Builder->CreateICmpSLT(L, R, "lttmp");
    } else if (op == GT) {
        return Builder->CreateICmpSGT(L, R, "gttmp");
    } else if (op == EQ) {
        return Builder->CreateICmpEQ(L, R, "eqtmp");
    } else if (op == NEQ) {
        return Builder->CreateICmpNE(L, R, "neqtmp");
    } else if (op == LTE) {
        return Builder->CreateICmpSLE(L, R, "ltetmp");
    } else if (op == GTE) {
        return Builder->CreateICmpSGE(L, R, "gtetmp");
    } else if (op == AND) {
        return Builder->CreateAnd(L, R, "andtmp");
    } else if (op == OR) {
        return Builder->CreateOr(L, R, "ortmp");
    }
}

llvm::Value* CallExpressionAST::codegen() {
    llvm::Function *CalleeFunc = CodeGenModule->getFunction(callee);
    if (!CalleeFunc) {
        return nullptr;
    }

    if (CalleeFunc->arg_size() != args.size()) {
        return nullptr;
    }

    std::vector<llvm::Value*> ArgsValue;

    for (int i = 0, e = args.size(); i != e; ++i) {
        ArgsValue.push_back(args[i]->codegen());
        if (!ArgsValue.back()) {
            return nullptr;
        }
    }

    return Builder->CreateCall(CalleeFunc, ArgsValue, "calltmp");
}
llvm::Value* PenCallExprAST::codegen() {
    return nullptr;
}

llvm::Value* GotoCallExprAST::codegen() {
    return nullptr;
}

llvm::Value* MoveCallExprAST::codegen() {
    return nullptr;
}
void IntializeModule() {
    CodeGenContext = std::make_unique<llvm::LLVMContext>();
    CodeGenModule = std::make_unique<llvm::Module>("Chiron Module", *CodeGenContext);
    Builder = std::make_unique<llvm::IRBuilder<>>(*CodeGenContext);
}