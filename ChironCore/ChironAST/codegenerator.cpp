// Include necessary headers
#include <map>
#include <iostream>
#include <vector>

#include "chironAST.hpp"  // AST (Abstract Syntax Tree) definitions

// LLVM headers for IR generation and optimization
#include <llvm/IR/Value.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/Constants.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Type.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/Verifier.h>
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/StandardInstrumentations.h"
#include "llvm/Transforms/Utils.h"
#include "llvm/Transforms/Utils/Mem2Reg.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Scalar/GVN.h"
#include "llvm/Transforms/InstCombine/InstCombine.h"
#include "llvm/Transforms/Scalar/Reassociate.h"
#include "llvm/Transforms/Scalar/SimplifyCFG.h"
#include "MyCustomPass.cpp"  // Custom optimization pass

// Constants for arithmetic operators
const char MINUS = '-';
const char PLUS = '+';
const char MUL = '*';
const char DIV = '/';
const char ASSIGN = '=';
const char NOT = '!';

// Constants for comparison operators
const std::string LT = "<";
const std::string GT = ">";
const std::string EQ = "==";
const std::string NEQ = "!=";
const std::string LTE = "<=";
const std::string GTE = ">=";

// Constants for logical operators
const std::string AND = "&&";
const std::string OR = "||";

// Global optimization flag
bool optim = false;

// LLVM context and module management
static std::unique_ptr<llvm::LLVMContext> CodeGenContext;
static std::unique_ptr<llvm::Module> CodeGenModule;
static std::unique_ptr<llvm::IRBuilder<>> Builder;
static std::map<std::string, llvm::AllocaInst*> SymbolTable;  // Symbol table for variables

// LLVM pass managers and analysis managers
static std::unique_ptr<llvm::FunctionPassManager> TheFPM;
static std::unique_ptr<llvm::LoopAnalysisManager> TheLAM;
static std::unique_ptr<llvm::FunctionAnalysisManager> TheFAM;
static std::unique_ptr<llvm::CGSCCAnalysisManager> TheCGAM;
static std::unique_ptr<llvm::ModuleAnalysisManager> TheMAM;
static std::unique_ptr<llvm::PassInstrumentationCallbacks> ThePIC;
static std::unique_ptr<llvm::StandardInstrumentations> TheSI;

// Function declarations for built-in functions
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

// Creates an alloca instruction in the entry block of the function
static llvm::AllocaInst *CreateEntryBlockAlloca(llvm::Function *TheFunction, llvm::StringRef VarName) {
    llvm::IRBuilder<> TmpB(&TheFunction->getEntryBlock(),
    TheFunction->getEntryBlock().begin());
    return TmpB.CreateAlloca(llvm::Type::getInt32Ty(*CodeGenContext), nullptr, VarName);
}

// Number expression code generation - creates a constant integer
llvm::Value* NumberExpressionAST::codegen() {
    return llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), val);
}

// Variable expression code generation - loads the variable's value from memory
llvm::Value* VariableExpressionAST::codegen() {
    llvm::AllocaInst *V = SymbolTable[name];
    if (!V) {
        throw std::runtime_error("Variable not declared: " + name);
    }
    return Builder->CreateLoad(V->getAllocatedType(), V, name.c_str());
}

// Binary arithmetic expression code generation
llvm::Value* BinArithExpressionAST::codegen() {
    if(op == ASSIGN){
        // Handle variable assignment
        VariableExpressionAST *LHSE = static_cast<VariableExpressionAST*>(LHS.get());
        llvm::AllocaInst *V = SymbolTable[LHSE->getName()];
        if (!V) {
            // Create alloca if variable doesn't exist
            V = CreateEntryBlockAlloca(Builder->GetInsertBlock()->getParent(), LHSE->getName());
            SymbolTable[LHSE->getName()] = V;
        }
        
        llvm::Value *R = RHS->codegen();
        if (!R) {
            throw std::runtime_error("Invalid right-hand side expression");
        }

        // llvm::Value* formatStr = Builder->CreateGlobalStringPtr("%d\n", "fmt");
        // Builder->CreateCall(printfFunc, {formatStr, R}, "prnt");

        return Builder->CreateStore(R, V);
    }

    // Handle other binary operations
    llvm::Value *L = LHS->codegen();
    llvm::Value *R = RHS->codegen();
    if(!L){
        throw std::runtime_error("Invalid left-hand side expression");
    }
    if(!R){
        throw std::runtime_error("Invalid right-hand side expression");
    }

    switch (op) {
        case PLUS:  return Builder->CreateAdd(L, R, "addtmp");
        case MINUS: return Builder->CreateSub(L, R, "subtmp");
        case MUL:   return Builder->CreateMul(L, R, "multmp");
        case DIV:   return Builder->CreateSDiv(L, R, "divtmp");
        default:    throw std::runtime_error("Invalid binary operator");
    }
}

// Unary arithmetic expression code generation
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

// Binary conditional expression code generation
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

// Function call expression code generation
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

// Pen up/down call code generation
llvm::Value* PenCallExprAST::codegen() {
    if (status) {
        return Builder->CreateCall(HandlePenUpFunc);
    } else {
        return Builder->CreateCall(HandlePenDownFunc);
    }
}

// Goto call code generation
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

// Move call code generation (forward, backward, left, right)
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

// If expression code generation
llvm::Value* IfExpressionAST::codegen() {
    llvm::Value *CondV = condition->codegen();
    if (!CondV){
        throw std::runtime_error("Invalid condition expression");
    }

    // Convert condition to boolean if needed
    if (!CondV->getType()->isIntegerTy(1)) {
        CondV = Builder->CreateICmpNE(
                    CondV, 
                    llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 0),
                    "ifcond");
    }

    llvm::Function *TheFunction = Builder->GetInsertBlock()->getParent();

    // Create basic blocks for then, else, and merge parts
    llvm::BasicBlock *ThenBB = llvm::BasicBlock::Create(*CodeGenContext, "then", TheFunction);
    llvm::BasicBlock *ElseBB = llvm::BasicBlock::Create(*CodeGenContext, "else");
    llvm::BasicBlock *MergeBB = llvm::BasicBlock::Create(*CodeGenContext, "ifcont");

    Builder->CreateCondBr(CondV, ThenBB, ElseBB);

    // Generate code for then block
    Builder->SetInsertPoint(ThenBB);
    for (size_t i = 0; i < thenBlock.size(); ++i) {
        llvm::Value* val = thenBlock[i]->codegen();
        if (!val){
            throw std::runtime_error("Invalid then block expression");
        }
    }
    Builder->CreateBr(MergeBB);
    ThenBB = Builder->GetInsertBlock();

    // Generate code for else block
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

    // Continue with merge block
    TheFunction->insert(TheFunction->end(), MergeBB);
    Builder->SetInsertPoint(MergeBB);

    return CondV;
}

// Loop expression code generation
llvm::Value* LoopExpressionAST::codegen(){
    // Create loop counter variable
    llvm::AllocaInst *RC = SymbolTable[varname];
    if(!RC){
        RC = CreateEntryBlockAlloca(Builder->GetInsertBlock()->getParent(), varname);
        SymbolTable[varname] = RC;
    }

    llvm::Value *RepCount = repCounter->codegen();
    if(!RepCount){
        throw std::runtime_error("Invalid repeat count expression");
    }
    
    Builder->CreateStore(RepCount, RC);

    llvm::Function *TheFunction = Builder->GetInsertBlock()->getParent();
    llvm::BasicBlock *LoopBB = llvm::BasicBlock::Create(*CodeGenContext, "loop", TheFunction);
    Builder->CreateBr(LoopBB);

    Builder->SetInsertPoint(LoopBB);

    // Generate loop body
    for(int i = 0; i < body.size(); i++){
        llvm::Value* val = body[i]->codegen();
        if(!val){
            throw std::runtime_error("Invalid loop body expression");
        }
    }

    // Decrement counter and check loop condition
    llvm::Value *Count = Builder->CreateLoad(RC->getAllocatedType(), RC, varname.c_str());
    llvm::Value *NextVal = Builder->CreateSub(Count, llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 1), "nextvar");
    Builder->CreateStore(NextVal, RC);

    llvm::Value *EndCond = Builder->CreateICmpNE(NextVal, llvm::ConstantInt::get(llvm::Type::getInt32Ty(*CodeGenContext), 0), "loopcond");

    llvm::BasicBlock *AfterBB = llvm::BasicBlock::Create(*CodeGenContext, "afterloop", TheFunction);
    Builder->CreateCondBr(EndCond, LoopBB, AfterBB);

    Builder->SetInsertPoint(AfterBB);

    return llvm::Constant::getNullValue(llvm::Type::getInt32Ty(*CodeGenContext));
}

// Function definition code generation
llvm::Value *FunctionAST::codegen() {
    // Create function type
    std::vector<llvm::Type*> argTypes(args.size(), llvm::Type::getInt32Ty(*CodeGenContext));
    llvm::FunctionType *FT = llvm::FunctionType::get(
        isVoid ? llvm::Type::getVoidTy(*CodeGenContext) : llvm::Type::getInt32Ty(*CodeGenContext),
        argTypes,
        false
    );

    // Create function
    llvm::Function *TheFunction = llvm::Function::Create(
        FT,
        llvm::Function::ExternalLinkage,
        name,
        CodeGenModule.get()
    );

    llvm::BasicBlock *BB = llvm::BasicBlock::Create(*CodeGenContext, "entry", TheFunction);
    Builder->SetInsertPoint(BB);

    // Save current symbol table and create new one for function scope
    std::map<std::string, llvm::AllocaInst*> StoredTable = SymbolTable;
    SymbolTable.clear();

    // Set up function arguments
    int i = 0;
    for(auto &arg : TheFunction->args()){
        arg.setName(args[i++]);
        llvm::AllocaInst *Alloca = CreateEntryBlockAlloca(TheFunction, arg.getName());
        Builder->CreateStore(&arg, Alloca);
        SymbolTable[std::string(arg.getName())] = Alloca;
    }

    // Generate function body
    for (size_t i = 0; i < body.size(); ++i) {
        llvm::Value* val = body[i]->codegen();
        if (!val) {
            TheFunction->eraseFromParent();
            SymbolTable = StoredTable;
            throw std::runtime_error("Invalid function body expression");
        }
    }

    // Handle return value
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

    // Verify and optimize the function
    llvm::verifyFunction(*TheFunction, &llvm::errs());
    TheFPM->run(*TheFunction, *TheFAM);
    SymbolTable = StoredTable;

    // Reset builder to main function
    Builder->SetInsertPoint(&CodeGenModule->getFunction("main")->getEntryBlock());

    return RV;
}

// Initialize LLVM module and components
void IntializeModule() {
    CodeGenContext = std::make_unique<llvm::LLVMContext>();
    CodeGenModule = std::make_unique<llvm::Module>("Chiron Module", *CodeGenContext);
    Builder = std::make_unique<llvm::IRBuilder<>>(*CodeGenContext);
    
    // Initialize pass and analysis managers
    TheFPM = std::make_unique<llvm::FunctionPassManager>();
    TheLAM = std::make_unique<llvm::LoopAnalysisManager>();
    TheFAM = std::make_unique<llvm::FunctionAnalysisManager>();
    TheCGAM = std::make_unique<llvm::CGSCCAnalysisManager>();
    TheMAM = std::make_unique<llvm::ModuleAnalysisManager>();
    ThePIC = std::make_unique<llvm::PassInstrumentationCallbacks>();
    TheSI = std::make_unique<llvm::StandardInstrumentations>(*CodeGenContext,
                                                            /*DebugLogging*/ true);
    // Add optimization passes if enabled
    if(optim){                                                
        TheFPM->addPass(llvm::PromotePass());      // Promote memory to registers
        TheFPM->addPass(DeadCodeEliminationPass());// Custom dead code elimination
        TheFPM->addPass(llvm::InstCombinePass());  // Instruction combining
        TheFPM->addPass(llvm::ReassociatePass());  // Reassociate expressions
        TheFPM->addPass(llvm::GVNPass());          // Global Value Numbering
        TheFPM->addPass(llvm::SimplifyCFGPass());  // Simplify control flow
    }
    
    // Register analysis managers
    llvm::PassBuilder PB;
    PB.registerModuleAnalyses(*TheMAM);
    PB.registerFunctionAnalyses(*TheFAM);
    PB.crossRegisterProxies(*TheLAM, *TheFAM, *TheCGAM, *TheMAM);

    // Declare printf function
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

    // Declare turtle graphics functions
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

// Initialize the main function
void InitializeMainFunction() {
    llvm::FunctionType *FT = llvm::FunctionType::get(llvm::Type::getInt32Ty(*CodeGenContext), false);
    llvm::Function *F = llvm::Function::Create(FT, llvm::Function::ExternalLinkage, "main", CodeGenModule.get());
    llvm::BasicBlock *BB = llvm::BasicBlock::Create(*CodeGenContext, "entry", F);
    Builder->SetInsertPoint(BB);

    // Call initialization function at start of main
    Builder->CreateCall(InitFunc);
}

// Convert LLVM IR to object file and executable
void ConverIRtoObjectFile(const std::string &output_filename, bool run_output, bool dump_ir, bool print_ir) {
    // Finalize the main function
    Builder->CreateCall(FinishFunc);
    Builder->CreateRet(Builder->getInt32(0));
    
    // Verify the module
    llvm::verifyModule(*CodeGenModule, &llvm::errs());
    
    // Get and optimize the main function
    llvm::Function *MainFunc = CodeGenModule->getFunction("main");
    if (MainFunc) {
        // Ensure main function has a terminator
        if (!MainFunc->getEntryBlock().getTerminator()) {
            Builder->CreateRet(Builder->getInt32(0));
        }
    
        // Verify and optimize main function
        llvm::verifyFunction(*MainFunc, &llvm::errs());
        TheFPM->run(*MainFunc, *TheFAM);
    }
    
    // Print IR if requested
    if(print_ir){
        CodeGenModule->print(llvm::errs(), nullptr);
    }

    // Write IR to file
    std::error_code EC;
    llvm::raw_fd_ostream outFile(output_filename + ".ll", EC);
    if (EC) {
        llvm::errs() << "Error opening file: " << EC.message() << "\n";
        return;
    }
    
    // Print module to file if main function exists
    llvm::Function *TheFunction = CodeGenModule->getFunction("main");
    if (TheFunction) {
        CodeGenModule->print(outFile, nullptr);
    } else {
        llvm::errs() << "No function 'main' found in the module.\n";
    }
    outFile.close();

    // Link with custom turtle graphics library
    std::string llvmLinkCommand = "llvm-link " + output_filename + ".ll ./CTurtle/CustomCTurtle.ll -S -o combined.ll";
    int result = system(llvmLinkCommand.c_str());
    if (result != 0) {
        llvm::errs() << "Error running llvm-link\n";
        return;
    }

    // Generate object file from LLVM IR
    std::string llcCommand = "llc -filetype=obj -relocation-model=pic -o combined.o combined.ll";
    result = system(llcCommand.c_str());
    if (result != 0) {
        llvm::errs() << "Error running llc\n";
        return;
    }
    
    // Link object file to create executable
    std::string gccCommand = "g++ combined.o -o " + output_filename + " -lX11";
    result = system(gccCommand.c_str());
    if (result != 0) {
        llvm::errs() << "Error running gcc\n";
        return;
    }
    
    // Clean up temporary files
    system("rm combined.ll combined.o");
    
    // Remove IR file if not requested to keep it
    if(!dump_ir){
        std::string rmCommand = "rm " + output_filename + ".ll";
        result = system(rmCommand.c_str());
    }

    // Run the output executable if requested
    if(run_output){
        std::string runCommand = "./" + output_filename;
        result = system(runCommand.c_str());
    }
}