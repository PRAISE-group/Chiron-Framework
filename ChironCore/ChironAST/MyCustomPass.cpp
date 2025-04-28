// MyCustomPass.h
#pragma once

// Include necessary LLVM headers
#include "llvm/IR/PassManager.h"          
#include "llvm/IR/Function.h"             
#include "llvm/IR/IRBuilder.h"            
#include "llvm/Transforms/Utils/Local.h" 
#include "llvm/Support/raw_ostream.h"     
#include "llvm/IR/Instructions.h"         

// Define a custom pass for Dead Code Elimination
struct DeadCodeEliminationPass : public llvm::PassInfoMixin<DeadCodeEliminationPass> {
    // The main function that runs the pass on a given LLVM Function
    llvm::PreservedAnalyses run(llvm::Function &F, llvm::FunctionAnalysisManager &) {
        bool changed = false; // Flag to track if any changes were made
        int count;            // Counter to track the number of instructions erased

        // Repeat the process until no more dead instructions are found
        do {
            count = 0; // Reset the counter for each iteration

            // Vector to store instructions marked for deletion
            llvm::SmallVector<llvm::Instruction *, 8> toErase;

            // Iterate over all basic blocks in the function
            for (llvm::BasicBlock &BB : F) {
                // Iterate over all instructions in the basic block
                for (llvm::Instruction &I : BB) {
                    // Skip terminator instructions (e.g., return, branch)
                    if (I.isTerminator()) continue;

                    // Check if the instruction has no uses and no side effects
                    if (I.use_empty() && !I.mayHaveSideEffects()) {
                        toErase.push_back(&I); // Mark the instruction for deletion
                        count++;               // Increment the counter
                    }
                }
            }

            // Erase all marked instructions
            for (llvm::Instruction *I : toErase) {
                llvm::errs() << "Erasing dead instruction: " << *I << "\n"; // Debug output
                I->eraseFromParent(); // Remove the instruction from its parent
                changed = true;       // Indicate that a change was made
            }
        } while (count); // Repeat until no more instructions are erased

        // Return the appropriate analysis preservation status
        return changed ? llvm::PreservedAnalyses::none() : llvm::PreservedAnalyses::all();
    }
};