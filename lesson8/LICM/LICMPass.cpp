#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/IR/Dominators.h"

#include "llvm/Analysis/ValueTracking.h"
#include "llvm/Transforms/Utils/Mem2Reg.h"


 #include "llvm/Transforms/Utils.h"
 #include "llvm-c/Initialization.h"
 #include "llvm-c/Transforms/Utils.h"
 #include "llvm/IR/LegacyPassManager.h"
 #include "llvm/InitializePasses.h"
 #include "llvm/Pass.h"
 #include "llvm/PassRegistry.h"

using namespace llvm;

namespace {
  struct LICMPass : public LoopPass {
    static char ID;
    LICMPass() : LoopPass(ID) {}

    virtual bool runOnLoop(Loop *L, LPPassManager &LPM) {
      bool changed = false;
      bool found_invariant = true;
      while (found_invariant) {
        BasicBlock *H = L->getHeader();
        found_invariant = false;
        for (BasicBlock *BB: L->blocks()) {
          for (Instruction &I: *BB) {
            bool made_invariant = false;
            bool is_invariant = L->makeLoopInvariant(&I, made_invariant);
            
            if (is_invariant) {
              //errs() << "Found invariant " << I << "\n";
              found_invariant = true;
              break;
            }
            // errs() << I << "\n";
            // errs() << is_invariant << "\n";
            
            // for (Value *Operand : (&I)->operands())
            //   errs() << "Operand " << Operand << " " << L->makeLoopInvariant(Operand, made_invariant) << "\n";

            // errs() << "\n\n";
            changed = changed || made_invariant;
          }

          if (found_invariant) {
            break;
          }
        }

        if (found_invariant) {
          continue;
        }
      }
      return changed;
    }

    void getAnalysisUsage(AnalysisUsage &AU) const override {
      AU.setPreservesCFG();
      AU.addRequired<LoopInfoWrapperPass>();
      AU.addRequired<DominatorTreeWrapperPass>();
      //AU.addRequiredID(PromoteMemoryToRegister::MemoryToRegisterID);
    }

  };
}

char LICMPass::ID = 0;

// For opt
static RegisterPass<LICMPass> X("LICMPass", "LICM Pass",
							 false /* Only looks at CFG */,
							 false /* Analysis Pass */);

// Automatically enable the pass.
// http://adriansampson.net/blog/clangpass.html
static void registerLICMPass(const PassManagerBuilder &,
                         legacy::PassManagerBase &PM) {
  PM.add(createPromoteMemoryToRegisterPass());
  PM.add(new LICMPass());
}
static RegisterStandardPasses
  RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
                 registerLICMPass);