#include <any>
#include <vector>
#include <stdexcept>
#include <string>
#include <utility>

#include "chironAST.hpp"

#include "tlangVisitor.h"

using namespace std;

static ExpressionAST* getSingleExpr(const any &result) {
        auto vec = any_cast<vector<InstrAST*>>(result);
        if (vec.empty())
            throw runtime_error("Expected at least one expression, got an empty vector");

        ExpressionAST* expr = dynamic_cast<ExpressionAST*>(vec[0]);
        if (!expr)
            throw runtime_error("First element is not of type ExpressionAST*");
        return expr;

 }

class ChironVisitorImpl : public tlangVisitor {
    int repeatInstrCount = 0;

public:
    any visitStart(tlangParser::StartContext *ctx) override {
        if (!ctx) {
            std::cerr << "Parser returned null context!" << std::endl;
        }
        return visit(ctx->instruction_list());
    }

    any visitInstruction_list(tlangParser::Instruction_listContext *ctx) override {
        vector<InstrAST*> instructions;
        for (auto *instr : ctx->instruction()) {
            auto subInstr = any_cast<vector<InstrAST*>>(visit(instr));
            instructions.insert(instructions.end(), subInstr.begin(), subInstr.end());
        }
        return instructions;
    }

    any visitStrict_ilist(tlangParser::Strict_ilistContext *ctx) override {
        vector<InstrAST*> instructions;
        for (auto *instr : ctx->instruction()) {
            auto subInstr = any_cast<vector<InstrAST*>>(visit(instr));
            instructions.insert(instructions.end(), subInstr.begin(), subInstr.end());
        }
        return instructions;
    }

    
    any visitInstruction(tlangParser::InstructionContext *ctx) override {
        if (ctx->assignment())    return visit(ctx->assignment());
        if (ctx->conditional())   return visit(ctx->conditional());
        if (ctx->loop())          return visit(ctx->loop());
        if (ctx->moveCommand())   return visit(ctx->moveCommand());
        if (ctx->penCommand())    return visit(ctx->penCommand());
        if (ctx->gotoCommand())   return visit(ctx->gotoCommand());
        if (ctx->pauseCommand())  return visit(ctx->pauseCommand());
        throw runtime_error("Unsupported instruction type");
    }

    any visitConditional(tlangParser::ConditionalContext *ctx) override {
        if (ctx->ifConditional()) {
            std::cerr << "visit(ctx->ifConditional())\n";
            return visit(ctx->ifConditional());
        }
        if (ctx->ifElseConditional()) {
            return visit(ctx->ifElseConditional());
        }
        throw runtime_error("Unsupported conditional type");
        //return visitChildren(ctx);
    }

    any visitIfConditional(tlangParser::IfConditionalContext *ctx) override {
        auto condResult = visit(ctx->condition());
       
        std::cerr << "visit(ctx->condition()) type: " << condResult.type().name() << "\n";
        ExpressionAST* cond = getSingleExpr(condResult);

        // Visit the then block
        auto thenResult = visit(ctx->strict_ilist());
        vector<InstrAST*> thenBlock = any_cast<vector<InstrAST*>>(thenResult);

        // Create the IfExpressionAST node
        return vector<InstrAST*>{
            new IfExpressionAST(
                unique_ptr<ExpressionAST>(cond),
                vector<unique_ptr<InstrAST>>(thenBlock.begin(), thenBlock.end()),
                vector<unique_ptr<InstrAST>>() // Empty else block
            )
        };
    }

    any visitIfElseConditional(tlangParser::IfElseConditionalContext *ctx) override {
        ExpressionAST* cond = getSingleExpr(visit(ctx->condition()));
        vector<InstrAST*> thenBlock = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist(0)));
        vector<InstrAST*> elseBlock = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist(1)));
        return vector<InstrAST*>{
            make_unique<IfExpressionAST>(
                unique_ptr<ExpressionAST>(cond),
                vector<unique_ptr<InstrAST>>{thenBlock.begin(), thenBlock.end()},
                vector<unique_ptr<InstrAST>>{elseBlock.begin(), elseBlock.end()}
            ).release()
        };
    }

    any visitLoop(tlangParser::LoopContext *ctx) override {
        repeatInstrCount++;
        ExpressionAST* repeatNum = getSingleExpr(visit(ctx->value()));
        NumberExpressionAST* rep = dynamic_cast<NumberExpressionAST*>(repeatNum);
        if (!rep)
            throw runtime_error("Loop count must be a number");
        
        string varname = "__rep_counter_" + to_string(repeatInstrCount);
        vector<InstrAST*> body = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist()));
        
        repeatInstrCount--;
        return vector<InstrAST*>{
            make_unique<LoopExpressionAST>(
                rep->getVal(),
                varname,
                vector<unique_ptr<InstrAST>>{body.begin(), body.end()}
            ).release()
        };
    }
    
    any visitAssignment(tlangParser::AssignmentContext *ctx) override {
        VariableExpressionAST* var = new VariableExpressionAST(ctx->VAR()->getText());
        ExpressionAST* expr = getSingleExpr(visit(ctx->expression()));
        return vector<InstrAST*>{
            new BinArithExpressionAST('=', unique_ptr<ExpressionAST>(var), unique_ptr<ExpressionAST>(expr))
        };
    }

    any visitGotoCommand(tlangParser::GotoCommandContext *ctx) override {
        ExpressionAST* x = getSingleExpr(visit(ctx->expression(0)));
        ExpressionAST* y = getSingleExpr(visit(ctx->expression(1)));
        vector<InstrAST*> result;
        result.push_back(
            make_unique<GotoCallExprAST>(unique_ptr<ExpressionAST>(x), unique_ptr<ExpressionAST>(y)).release()
        );
        return result;
    }

    any visitMoveCommand(tlangParser::MoveCommandContext *ctx) override {
        ExpressionAST* expr = getSingleExpr(visit(ctx->expression()));
        vector<InstrAST*> result;
        result.push_back(
            make_unique<MoveCallExprAST>(ctx->moveOp()->getText(), unique_ptr<ExpressionAST>(expr)).release()
        );
        return result;
    }

    any visitPenCommand(tlangParser::PenCommandContext *ctx) override {
        bool status = (ctx->getText() == "penup");
        return vector<InstrAST*>{ new PenCallExprAST(status) };
    }

    any visitPauseCommand(tlangParser::PauseCommandContext *ctx) override {
        return vector<InstrAST*>{ new CallExpressionAST("pause", vector<unique_ptr<ExpressionAST>>{}) };
    }

    any visitUnaryExpr(tlangParser::UnaryExprContext *ctx) override {
        ExpressionAST* expr = getSingleExpr(visit(ctx->expression()));
        vector<InstrAST*> result;
        result.push_back(
            make_unique<UnaryArithExpressionAST>('-', unique_ptr<ExpressionAST>(expr)).release()
        );
        return result;
    }

    any visitAddExpr(tlangParser::AddExprContext *ctx) override {
        ExpressionAST* lhs = getSingleExpr(visit(ctx->expression(0)));
        ExpressionAST* rhs = getSingleExpr(visit(ctx->expression(1)));
        string op = ctx->additive()->PLUS() ? "+" : "-";
        vector<InstrAST*> result;
        result.push_back(
            make_unique<BinArithExpressionAST>(
                op[0],
                unique_ptr<ExpressionAST>(lhs),
                unique_ptr<ExpressionAST>(rhs)
            ).release()
        );
        return result;
    }

    any visitMulExpr(tlangParser::MulExprContext *ctx) override {
        ExpressionAST* lhs = getSingleExpr(visit(ctx->expression(0)));
        ExpressionAST* rhs = getSingleExpr(visit(ctx->expression(1)));
        string op = ctx->multiplicative()->MUL() ? "*" : "/";
        vector<InstrAST*> result;
        result.push_back(
            make_unique<BinArithExpressionAST>(
                op[0],
                unique_ptr<ExpressionAST>(lhs),
                unique_ptr<ExpressionAST>(rhs)
            ).release()
        );
        return result;
    }

    any visitParenExpr(tlangParser::ParenExprContext *ctx) override {
        return visit(ctx->expression());
    }

    any visitCondition(tlangParser::ConditionContext *ctx) override {
        if (ctx->PENCOND()) {
            return vector<InstrAST*>{ new PenCallExprAST(false) };
        }
        if (ctx->NOT()) {
            auto condResult = visit(ctx->condition(0));
            ExpressionAST* cond = getSingleExpr(condResult);
            return vector<InstrAST*>{
                new UnaryArithExpressionAST('!', unique_ptr<ExpressionAST>(cond))
            };
        }
        if (ctx->logicOp()) {
            auto lhsResult = visit(ctx->condition(0));
            auto rhsResult = visit(ctx->condition(1));
            ExpressionAST* lhs = getSingleExpr(lhsResult);
            ExpressionAST* rhs = getSingleExpr(rhsResult);
            string op = ctx->logicOp()->AND() ? "&&" : "||";
            return vector<InstrAST*>{
                new BinCondExpressionAST(op, unique_ptr<ExpressionAST>(lhs), unique_ptr<ExpressionAST>(rhs))
            };
        }
        if (ctx->binCondOp()) {
            auto lhsResult = visit(ctx->expression(0));
            auto rhsResult = visit(ctx->expression(1));
            ExpressionAST* lhs = getSingleExpr(lhsResult);
            ExpressionAST* rhs = getSingleExpr(rhsResult);
            string op;
            if (ctx->binCondOp()->LT())      op = "<";
            else if (ctx->binCondOp()->GT()) op = ">";
            else if (ctx->binCondOp()->EQ()) op = "==";
            else if (ctx->binCondOp()->NEQ()) op = "!=";
            else if (ctx->binCondOp()->LTE()) op = "<=";
            else if (ctx->binCondOp()->GTE()) op = ">=";
            return vector<InstrAST*>{
                new BinCondExpressionAST(op, unique_ptr<ExpressionAST>(lhs), unique_ptr<ExpressionAST>(rhs))
            };
        }
        
        // may be one of the case - If the condition is parenthesized or otherwise has child conditions,
        // try returning the result of the first child condition.
        if (!ctx->condition().empty()) {
            auto childResult = visit(ctx->condition(0));
            // If that returns a nonempty vector, use it.
            auto vec = any_cast<vector<InstrAST*>>(childResult);
            if (!vec.empty())
                return childResult;
        }
        // other case - if there is a child expression, return that.
        if (!ctx->expression().empty()) {
            auto childResult = visit(ctx->expression(0));
            auto vec = any_cast<vector<InstrAST*>>(childResult);
            if (!vec.empty())
                return childResult;
        }
        // Fallback: do not call visitChildren, just return an empty vector - this is just added to check whether if we assume cond default result to be 1, then it is running or not.
        // return vector<InstrAST*>{ new NumberExpressionAST(1) };
        return vector<InstrAST*>{};
    }

    any visitValue(tlangParser::ValueContext *ctx) override {
        if (ctx->NUM()) {
            return vector<InstrAST*>{ new NumberExpressionAST(stoi(ctx->NUM()->getText())) };
        }
        if (ctx->VAR()) {
            return vector<InstrAST*>{ new VariableExpressionAST(ctx->VAR()->getText()) };
        }
        throw runtime_error("Invalid value");
    }

    // Default implementations for rules not used:
    any visitMoveOp(tlangParser::MoveOpContext*) override { return nullptr; }
    any visitAdditive(tlangParser::AdditiveContext*) override { return nullptr; }
    any visitMultiplicative(tlangParser::MultiplicativeContext*) override { return nullptr; }
    any visitUnaryArithOp(tlangParser::UnaryArithOpContext*) override { return nullptr; }
    any visitBinCondOp(tlangParser::BinCondOpContext*) override { return nullptr; }
    any visitLogicOp(tlangParser::LogicOpContext*) override { return nullptr; }
    any visitValueExpr(tlangParser::ValueExprContext *ctx) override { return visit(ctx->value()); }
};

tlangVisitor* createChironVisitor() {
    return new ChironVisitorImpl();
}



