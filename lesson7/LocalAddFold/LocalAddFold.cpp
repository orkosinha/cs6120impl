#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include "llvm/IR/InstVisitor.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include <stack>
using namespace llvm;

namespace {
  struct LocalAddFoldPass : public FunctionPass {
    static char ID;
    LocalAddFoldPass() : FunctionPass(ID) {}

    virtual bool runOnFunction(Function &F) {
      bool changed = false;
      std::stack<Instruction*> replaced;
      for (auto &BB: F) {
        for (auto &I: BB) {
          if (auto* op = dyn_cast<BinaryOperator>(&I)) {

            IRBuilder<> builder(op);
            if (op->getOpcode() == Instruction::Add) {
              ConstantInt* lhs = dyn_cast<ConstantInt>(op->getOperand(0));
              ConstantInt* rhs = dyn_cast<ConstantInt>(op->getOperand(1));
              
              if (lhs != NULL && rhs !=NULL) {
                int64_t value = lhs->getSExtValue() + rhs->getSExtValue();
                Type* t = lhs->getType();
                Value* llvm_value = ConstantInt::get(t, value);
                op->replaceAllUsesWith(llvm_value);
                replaced.push(op);
                changed = true;
              }

              errs() << *op << "\n";
            }
          }
        }
      }
      while (!replaced.empty()) {
        replaced.top()->eraseFromParent();
        replaced.pop();
      }
      
      return changed;
    }
  };
}

char LocalAddFoldPass::ID = 0;

// Automatically enable the pass.
// http://adriansampson.net/blog/clangpass.html
static void registerSkeletonPass(const PassManagerBuilder &,
                         legacy::PassManagerBase &PM) {
  PM.add(new LocalAddFoldPass());
}
static RegisterStandardPasses
  RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
                 registerSkeletonPass);
