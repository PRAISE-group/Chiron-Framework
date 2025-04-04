#include <map>
#include <iostream>
#include <vector>

#include "chironAST.hpp"

#include <llvm/IR/Value.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Type.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/Verifier.h>

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

static llvm::Function* printfFunc;

static llvm::Function* InitFunc;
static llvm::Function* HandleGoToFunc;
static llvm::Function* HandleForwardFunc;
static llvm::Function* HandleBackwardFunc;
static llvm::Function* HandleRightFunc;
static llvm::Function* HandleLeftFunc;
static llvm::Function* HandlePenUpFunc;
static llvm::Function* HandlePenDownFunc;
static llvm::Function* FinishFunc;

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
        throw std::runtime_error("Variable not declared: " + name);
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
            throw std::runtime_error("Invalid right-hand side expression");
        }

        llvm::Value* formatStr = Builder->CreateGlobalStringPtr("%d\n", "fmt");
        Builder->CreateCall(printfFunc, {formatStr, R}, "prnt");
        
        return Builder->CreateStore(R, V);
    }

    llvm::Value *L = LHS->codegen();
    llvm::Value *R = RHS->codegen();
    if(!L){
        throw std::runtime_error("Invalid left-hand side expression");
    }
    if(!R){
        throw std::runtime_error("Invalid right-hand side expression");
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
            throw std::runtime_error("Invalid binary operator");
    }
}

llvm::Value* UnaryArithExpressionAST::codegen() {
    llvm::Value *R = RHS->codegen();
    if (!R) {
        throw std::runtime_error("Invalid right-hand side expression");
    }

    if (op == MINUS) {
        return Builder->CreateNeg(R, "negtmp");
    } else if (op == NOT) {
        return Builder->CreateNot(R, "nottmp");
    }

    throw std::runtime_error("Invalid unary operator");
}

llvm::Value* BinCondExpressionAST::codegen() {
    llvm::Value *L = LHS->codegen();
    llvm::Value *R = RHS->codegen();
    if (!L) {
        throw std::runtime_error("Invalid left-hand side expression");
    }
    if (!R) {
        throw std::runtime_error("Invalid right-hand side expression");
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

    throw std::runtime_error("Invalid binary conditional operator");
}

llvm::Value* CallExpressionAST::codegen() {
    llvm::Function *CalleeFunc = CodeGenModule->getFunction(callee);
    if (!CalleeFunc) {
        throw std::runtime_error("Function not found: " + callee);
    }

    if (CalleeFunc->arg_size() != args.size()) {
        throw std::runtime_error("Incorrect number of arguments passed to function");
    }

    std::vector<llvm::Value*> ArgsValue;

    for (int i = 0, e = args.size(); i != e; ++i) {
        ArgsValue.push_back(args[i]->codegen());
        if (!ArgsValue.back()) {
            throw std::runtime_error("Invalid argument passed to function");
        }
    }

    if(CalleeFunc->getReturnType()->isVoidTy()) {
        return Builder->CreateCall(CalleeFunc, ArgsValue);
    }

    return Builder->CreateCall(CalleeFunc, ArgsValue, "calltmp");
}

llvm::Value* PenCallExprAST::codegen() {
    if (status) {
        return Builder->CreateCall(HandlePenUpFunc);
    } else {
        return Builder->CreateCall(HandlePenDownFunc);
    }
}

llvm::Value* GotoCallExprAST::codegen() {
    llvm::Value *X = x->codegen();
    llvm::Value *Y = y->codegen();
    if (!X) {
        throw std::runtime_error("Invalid x-coordinate expression");
    }
    if (!Y) {
        throw std::runtime_error("Invalid y-coordinate expression");
    }
    if (!X->getType()->isIntegerTy(32) || !Y->getType()->isIntegerTy(32)) {
        throw std::runtime_error("Goto coordinates must be integers");
    }

    return Builder->CreateCall(HandleGoToFunc, {X, Y});
}

llvm::Value* MoveCallExprAST::codegen() {
    llvm::Value *V = val->codegen();
    if (!V) {
        throw std::runtime_error("Invalid value expression");
    }

    if(direction == "forward"){
        return Builder->CreateCall(HandleForwardFunc, V);
    } else if(direction == "backward"){
        return Builder->CreateCall(HandleBackwardFunc, V);
    } else if(direction == "right"){
        return Builder->CreateCall(HandleRightFunc, V);
    } else if(direction == "left"){
        return Builder->CreateCall(HandleLeftFunc, V);
    }

    throw std::runtime_error("Invalid move direction");
}

llvm::Value* IfExpressionAST::codegen() {
    llvm::Value *CondV = condition->codegen();
    if (!CondV){
        throw std::runtime_error("Invalid condition expression");
    }

    // Only convert CondV to an i1 boolean if it is not already i1.
    if (!CondV->getType()->isIntegerTy(1)) {
        CondV = Builder->CreateICmpNE(
                    CondV, 
                    llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 0),
                    "ifcond");
    }

    llvm::Function *TheFunction = Builder->GetInsertBlock()->getParent();

    llvm::BasicBlock *ThenBB = llvm::BasicBlock::Create(*CodeGenContext, "then", TheFunction);
    llvm::BasicBlock *ElseBB = llvm::BasicBlock::Create(*CodeGenContext, "else");
    llvm::BasicBlock *MergeBB = llvm::BasicBlock::Create(*CodeGenContext, "ifcont");

    Builder->CreateCondBr(CondV, ThenBB, ElseBB);

    Builder->SetInsertPoint(ThenBB);
    for (size_t i = 0; i < thenBlock.size(); ++i) {
        llvm::Value* val = thenBlock[i]->codegen();
        if (!val){
            throw std::runtime_error("Invalid then block expression");
        }
    }
    Builder->CreateBr(MergeBB);
    ThenBB = Builder->GetInsertBlock();

    TheFunction->insert(TheFunction->end(), ElseBB);
    Builder->SetInsertPoint(ElseBB);
    for (size_t i = 0; i < elseBlock.size(); ++i) {
        llvm::Value* val = elseBlock[i]->codegen();
        if (!val){
            throw std::runtime_error("Invalid else block expression");
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
            throw std::runtime_error("Invalid loop body expression");
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

llvm::Value *FunctionAST::codegen() {
    std::vector<llvm::Type*> argTypes(args.size(), llvm::Type::getInt32Ty(*CodeGenContext));
    llvm::FunctionType *FT = llvm::FunctionType::get(
        isVoid ? llvm::Type::getVoidTy(*CodeGenContext) : llvm::Type::getInt32Ty(*CodeGenContext),
        argTypes,
        false
    );

    llvm::Function *TheFunction = llvm::Function::Create(
        FT,
        llvm::Function::ExternalLinkage,
        name,
        CodeGenModule.get()
    );

    llvm::BasicBlock *BB = llvm::BasicBlock::Create(*CodeGenContext, "entry", TheFunction);
    Builder->SetInsertPoint(BB);

    std::map<std::string, llvm::AllocaInst*> StoredTable = SymbolTable;
    SymbolTable.clear();

    int i = 0;
    for(auto &arg : TheFunction->args()){
        arg.setName(args[i++]);
        llvm::AllocaInst *Alloca = CreateEntryBlockAlloca(TheFunction, arg.getName());
        Builder->CreateStore(&arg, Alloca);
        SymbolTable[std::string(arg.getName())] = Alloca;
    }

    for (size_t i = 0; i < body.size(); ++i) {
        llvm::Value* val = body[i]->codegen();
        if (!val) {
            TheFunction->eraseFromParent();
            SymbolTable = StoredTable;
            throw std::runtime_error("Invalid function body expression");
        }
    }

    llvm::Value *RV;

    if (isVoid) {
        RV = Builder->CreateRetVoid();
    } else {
        if (returnValue) {
            RV = returnValue->codegen();
            if (!RV) {
                TheFunction->eraseFromParent();
                SymbolTable = StoredTable;
                throw std::runtime_error("Invalid return value expression");
            }
            RV = Builder->CreateRet(RV);
        } else {
            TheFunction->eraseFromParent();
            SymbolTable = StoredTable;
            throw std::runtime_error("Function should return a value");
        }
    }

    llvm::verifyFunction(*TheFunction, &llvm::errs());
    SymbolTable = StoredTable;

    Builder->SetInsertPoint(&CodeGenModule->getFunction("main")->getEntryBlock());

    return RV;
}

void IntializeModule() {
    CodeGenContext = std::make_unique<llvm::LLVMContext>();
    CodeGenModule = std::make_unique<llvm::Module>("Chiron Module", *CodeGenContext);
    Builder = std::make_unique<llvm::IRBuilder<>>(*CodeGenContext);
    
    printfFunc = llvm::Function::Create(
        llvm::FunctionType::get(
            Builder->getInt32Ty(),
            {Builder->getInt8Ty()->getPointerTo()},
            true
        ),
        llvm::Function::ExternalLinkage,
        "printf",
        CodeGenModule.get()
    );

    InitFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), false),
        llvm::Function::ExternalLinkage,
        "init",
        CodeGenModule.get()
    );

    HandleGoToFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), {Builder->getInt32Ty(), Builder->getInt32Ty()}, false),
        llvm::Function::ExternalLinkage,
        "handleGoTo",
        CodeGenModule.get()
    );

    HandleForwardFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), {Builder->getInt32Ty()}, false),
        llvm::Function::ExternalLinkage,
        "handleForward",
        CodeGenModule.get()
    );

    HandleBackwardFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), {Builder->getInt32Ty()}, false),
        llvm::Function::ExternalLinkage,
        "handleBackward",
        CodeGenModule.get()
    );

    HandleRightFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), {Builder->getInt32Ty()}, false),
        llvm::Function::ExternalLinkage,
        "handleRight",
        CodeGenModule.get()
    );

    HandleLeftFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), {Builder->getInt32Ty()}, false),
        llvm::Function::ExternalLinkage,
        "handleLeft",
        CodeGenModule.get()
    );

    HandlePenUpFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), false),
        llvm::Function::ExternalLinkage,
        "handlePenUp",
        CodeGenModule.get()
    );

    HandlePenDownFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), false),
        llvm::Function::ExternalLinkage,
        "handlePenDown",
        CodeGenModule.get()
    );

    FinishFunc = llvm::Function::Create(
        llvm::FunctionType::get(llvm::Type::getVoidTy(*CodeGenContext), false),
        llvm::Function::ExternalLinkage,
        "finish",
        CodeGenModule.get()
    );
}

void InitializeMainFunction() {
    llvm::FunctionType *FT = llvm::FunctionType::get(llvm::Type::getInt32Ty(*CodeGenContext), false);
    llvm::Function *F = llvm::Function::Create(FT, llvm::Function::ExternalLinkage, "main", CodeGenModule.get());
    llvm::BasicBlock *BB = llvm::BasicBlock::Create(*CodeGenContext, "entry", F);
    Builder->SetInsertPoint(BB);

    Builder->CreateCall(InitFunc);
}

void ConverIRtoObjectFile(){
    Builder->CreateCall(FinishFunc);
    Builder->CreateRet(Builder->getInt32(0));
    llvm::verifyModule(*CodeGenModule, &llvm::errs());

    CodeGenModule->print(llvm::errs(), nullptr);
    std::error_code EC;
    
    llvm::raw_fd_ostream outFile("output.ll", EC);
    if (EC) {
        llvm::errs() << "Error opening file: " << EC.message() << "\n";
        return;
    }
    
    llvm::Function *TheFunction = CodeGenModule->getFunction("main");
    if (TheFunction) {
        CodeGenModule->print(outFile, nullptr);
    } else {
        llvm::errs() << "No function 'main' found in the module.\n";
    }
    outFile.close();

    std::string llvmLinkCommand = "llvm-link output.ll ./CTurtle/CustomCTurtle.ll -S -o combined.ll";
    int result = system(llvmLinkCommand.c_str());
    if (result != 0) {
        llvm::errs() << "Error running llvm-link\n";
        return;
    }

    std::string llcCommand = "llc -filetype=obj -relocation-model=pic -o combined.o combined.ll";
    result = system(llcCommand.c_str());
    if (result != 0) {
        llvm::errs() << "Error running llc\n";
        return;
    }
    
    std::string gccCommand = "g++ combined.o -o output -lX11";
    result = system(gccCommand.c_str());
    if (result != 0) {
        llvm::errs() << "Error running gcc\n";
        return;
    }
    
    system("rm combined.ll combined.o");
    system("./output");
}