#include <chironAST.hpp>

#include <map>
#include <iostream>
#include <vector>

#include <llvm/IR/Value.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Type.h>
#include <llvm/IR/IRBuilder.h>

const char MINUS = '-';
const char PLUS = '+';
const char MUL = '*';
const char DIV = '/';
const char ASSIGN = '=';
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
static std::map<std::string, llvm::AllocaInst*> SymbolTable;

static llvm::AllocaInst *CreateEntryBlockAlloca(llvm::Function *TheFunction, llvm::StringRef VarName) {
    llvm::IRBuilder<> TmpB(&TheFunction->getEntryBlock(),
    TheFunction->getEntryBlock().begin());
    return TmpB.CreateAlloca(llvm::Type::getInt32Ty(*CodeGenContext), nullptr, VarName);
}

llvm::Value* NumberExpressionAST::codegen() {
    return llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), val);
}

llvm::Value* VariableExpressionAST::codegen() {
    llvm::AllocaInst *V = SymbolTable[name];
    if (!V) {
        return nullptr;
    }
    return Builder->CreateLoad(V->getAllocatedType(), V, name.c_str());
}

llvm::Value* BinArithExpressionAST::codegen() {
    if(op == ASSIGN){
        VariableExpressionAST *LHSE = static_cast<VariableExpressionAST*>(LHS.get());
        llvm::AllocaInst *V = SymbolTable[LHSE->getName()];
        if (!V) {
            V = CreateEntryBlockAlloca(Builder->GetInsertBlock()->getParent(), LHSE->getName());
            SymbolTable[LHSE->getName()] = V;
        }
        
        llvm::Value *R = RHS->codegen();
        if (!R) {
            return nullptr;
        }

        
        return Builder->CreateStore(R, V);
    }

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

llvm::Value* IfExpressionAST::codegen() {
    llvm::Value *CondV = condition->codegen();
    if (!CondV) {
        return nullptr;
    }

    CondV = Builder->CreateICmpNE(CondV, llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 0), "ifcond");

    llvm::Function *TheFunction = Builder->GetInsertBlock()->getParent();

    llvm::BasicBlock *ThenBB = llvm::BasicBlock::Create(*CodeGenContext, "then", TheFunction);
    llvm::BasicBlock *ElseBB = llvm::BasicBlock::Create(*CodeGenContext, "else");
    llvm::BasicBlock *MergeBB = llvm::BasicBlock::Create(*CodeGenContext, "ifcont");

    Builder->CreateCondBr(CondV, ThenBB, ElseBB);
    Builder->SetInsertPoint(ThenBB);
    for(int i = 0; i < thenBlock.size(); i++){
        llvm::Value* val = thenBlock[i]->codegen();
        if(!val){
            return nullptr;
        }
    }

    Builder->CreateBr(MergeBB);
    ThenBB = Builder->GetInsertBlock();

    TheFunction->insert(TheFunction->end(), ElseBB);
    Builder->SetInsertPoint(ElseBB);
    for(int i = 0; i < elseBlock.size(); i++){
        llvm::Value* val = elseBlock[i]->codegen();
        if(!val){
            return nullptr;
        }
    }

    Builder->CreateBr(MergeBB);
    ElseBB = Builder->GetInsertBlock();

    TheFunction->insert(TheFunction->end(), MergeBB);
    Builder->SetInsertPoint(MergeBB);

    return CondV;
}

llvm::Value* LoopExpressionAST::codegen(){
    llvm::AllocaInst *RC = SymbolTable[varname];
    if(!RC){
        RC = CreateEntryBlockAlloca(Builder->GetInsertBlock()->getParent(), varname);
        SymbolTable[varname] = RC;
    }
    Builder->CreateStore(llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), repCounter), RC);

    llvm::Function *TheFunction = Builder->GetInsertBlock()->getParent();
    llvm::BasicBlock *LoopBB = llvm::BasicBlock::Create(*CodeGenContext, "loop", TheFunction);
    Builder->CreateBr(LoopBB);

    Builder->SetInsertPoint(LoopBB);

    for(int i = 0; i < body.size(); i++){
        llvm::Value* val = body[i]->codegen();
        if(!val){
            return nullptr;
        }
    }

    llvm::Value *Count = Builder->CreateLoad(RC->getAllocatedType(), RC, varname.c_str());
    llvm::Value *NextVal = Builder->CreateSub(Count, llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 1), "nextvar");
    Builder->CreateStore(NextVal, RC);

    llvm::Value *EndCond = Builder->CreateICmpNE(NextVal, llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 0), "loopcond");

    llvm::BasicBlock *AfterBB = llvm::BasicBlock::Create(*CodeGenContext, "afterloop", TheFunction);
    Builder->CreateCondBr(EndCond, LoopBB, AfterBB);

    Builder->SetInsertPoint(AfterBB);

    return llvm::Constant::getNullValue(llvm::Type::getInt32Ty(*CodeGenContext));
}

void IntializeModule() {
    CodeGenContext = std::make_unique<llvm::LLVMContext>();
    CodeGenModule = std::make_unique<llvm::Module>("Chiron Module", *CodeGenContext);
    Builder = std::make_unique<llvm::IRBuilder<>>(*CodeGenContext);
}

void TempFunction() {
    llvm::FunctionType *FT = llvm::FunctionType::get(llvm::Type::getInt32Ty(*CodeGenContext), false);
    llvm::Function *F = llvm::Function::Create(FT, llvm::Function::ExternalLinkage, "main", CodeGenModule.get());
    llvm::BasicBlock *BB = llvm::BasicBlock::Create(*CodeGenContext, "entry", F);
    Builder->SetInsertPoint(BB);
}

void tempPrint(){
    llvm::Function *TheFunction = CodeGenModule->getFunction("main");
    TheFunction->print(llvm::errs());
}