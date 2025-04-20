// MyCustomPass.h
#pragma once
#include "llvm/IR/PassManager.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Transforms/Utils/Local.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/Instructions.h"
struct DeadCodeEliminationPass : public llvm::PassInfoMixin<DeadCodeEliminationPass> {
    llvm::PreservedAnalyses run(llvm::Function &F, llvm::FunctionAnalysisManager &) {
        bool changed = false;
        int count;
        do{
            count=0;
        llvm::SmallVector<llvm::Instruction *, 8> toErase;
        for (llvm::BasicBlock &BB : F) {
            for (llvm::Instruction &I : BB) {
                if (I.isTerminator()) continue;
                if (I.use_empty() && !I.mayHaveSideEffects()) {
                    toErase.push_back(&I);count++;
                }
            }
        }
        for (llvm::Instruction *I : toErase) {
            llvm::errs() << "Erasing dead instruction: " << *I << "\n";
            I->eraseFromParent();
            changed = true;
        }
    } while(count);
        return changed ? llvm::PreservedAnalyses::none() : llvm::PreservedAnalyses::all();
    }
};