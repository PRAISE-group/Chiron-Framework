#include "tlangVisitor.h"
#include "chironAST.hpp"
#include <any>
#include <memory>
#include <vector>
#include <stdexcept>

using namespace std;

class ChironVisitorImpl : public tlangVisitor {
    int repeatInstrCount = 0;

public:
    any visitStart(tlangParser::StartContext *ctx) override {
        return visit(ctx->instruction_list());
    }

    any visitInstruction_list(tlangParser::Instruction_listContext *ctx) override {
        vector<unique_ptr<InstrAST>> instructions;
        for (auto *instr : ctx->instruction()) {
            auto result = any_cast<vector<unique_ptr<InstrAST>>>(visit(instr));
            move(result.begin(), result.end(), back_inserter(instructions));
        }
        return instructions;
    }

    any visitStrict_ilist(tlangParser::Strict_ilistContext *ctx) override {
        vector<unique_ptr<InstrAST>> instructions;
        for (auto *instr : ctx->instruction()) {
            auto result = any_cast<vector<unique_ptr<InstrAST>>>(visit(instr));
            move(result.begin(), result.end(), back_inserter(instructions));
        }
        return instructions;
    }

    any visitInstruction(tlangParser::InstructionContext *ctx) override {
        if (auto assign = ctx->assignment()) return visit(assign);
        if (auto cond = ctx->conditional()) return visit(cond);
        if (auto loop = ctx->loop()) return visit(loop);
        if (auto move = ctx->moveCommand()) return visit(move);
        if (auto pen = ctx->penCommand()) return visit(pen);
        if (auto gotoCmd = ctx->gotoCommand()) return visit(gotoCmd);
        throw runtime_error("Unsupported instruction type");
    }

    any visitConditional(tlangParser::ConditionalContext *ctx) override {
        return visitChildren(ctx);
    }

    any visitIfConditional(tlangParser::IfConditionalContext *ctx) override {
        auto cond = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->condition()));
        auto thenBlock = any_cast<vector<unique_ptr<InstrAST>>>(visit(ctx->strict_ilist()));
        
        vector<unique_ptr<InstrAST>> result;
        result.push_back(make_unique<BinCondExpressionAST>("if", move(cond), nullptr));
        move(thenBlock.begin(), thenBlock.end(), back_inserter(result));
        return result;
    }

    any visitIfElseConditional(tlangParser::IfElseConditionalContext *ctx) override {
        auto cond = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->condition()));
        auto thenBlock = any_cast<vector<unique_ptr<InstrAST>>>(visit(ctx->strict_ilist(0)));
        auto elseBlock = any_cast<vector<unique_ptr<InstrAST>>>(visit(ctx->strict_ilist(1)));
        
        vector<unique_ptr<InstrAST>> result;
        result.push_back(make_unique<BinCondExpressionAST>("ifelse", move(cond), nullptr));
        move(thenBlock.begin(), thenBlock.end(), back_inserter(result));
        move(elseBlock.begin(), elseBlock.end(), back_inserter(result));
        return result;
    }

    any visitGotoCommand(tlangParser::GotoCommandContext *ctx) override {
        auto x = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(0)));
        auto y = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(1)));
        
        auto xNum = dynamic_cast<NumberExpressionAST*>(x.get());
        auto yNum = dynamic_cast<NumberExpressionAST*>(y.get());
        if (!xNum || !yNum) throw runtime_error("Goto requires numeric arguments");
        
        return vector<unique_ptr<InstrAST>>{make_unique<GotoCallExprAST>(xNum->getVal(), yNum->getVal())};
    }

    any visitAssignment(tlangParser::AssignmentContext *ctx) override {
        auto var = make_unique<VariableExpressionAST>(ctx->VAR()->getText());
        auto expr = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression()));
        
        vector<unique_ptr<ExpressionAST>> args;
        args.push_back(move(var));
        args.push_back(move(expr));
        return vector<unique_ptr<InstrAST>>{make_unique<CallExpressionAST>("assign", move(args))};
    }

    any visitMoveCommand(tlangParser::MoveCommandContext *ctx) override {
        auto expr = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression()));
        return vector<unique_ptr<InstrAST>>{
            make_unique<MoveCallExprAST>(ctx->moveOp()->getText(), move(expr))
        };
    }

    any visitPenCommand(tlangParser::PenCommandContext *ctx) override {
        bool status = ctx->getText() == "penup";
        return vector<unique_ptr<InstrAST>>{make_unique<PenCallExprAST>(status)};
    }

    any visitUnaryExpr(tlangParser::UnaryExprContext *ctx) override {
        auto expr = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression()));
        return vector<unique_ptr<InstrAST>>{make_unique<UnaryArithExpressionAST>('-', move(expr))};
    }

    any visitAddExpr(tlangParser::AddExprContext *ctx) override {
        auto lhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(0)));
        auto rhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(1)));
        string op = ctx->additive()->PLUS() ? "+" : "-";
        return vector<unique_ptr<InstrAST>>{make_unique<BinArithExpressionAST>(op[0], move(lhs), move(rhs))};
    }

    any visitMulExpr(tlangParser::MulExprContext *ctx) override {
        auto lhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(0)));
        auto rhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(1)));
        string op = ctx->multiplicative()->MUL() ? "*" : "/";
        return vector<unique_ptr<InstrAST>>{make_unique<BinArithExpressionAST>(op[0], move(lhs), move(rhs))};
    }

    any visitParenExpr(tlangParser::ParenExprContext *ctx) override {
        return visit(ctx->expression());
    }

    any visitCondition(tlangParser::ConditionContext *ctx) override {
        if (ctx->PENCOND()) {
            return vector<unique_ptr<InstrAST>>{make_unique<PenCallExprAST>(false)};
        }

        if (ctx->NOT()) {
            auto cond = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->condition(0)));
            return vector<unique_ptr<InstrAST>>{make_unique<UnaryArithExpressionAST>('!', move(cond))};
        }

        if (auto logicOp = ctx->logicOp()) {
            auto lhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->condition(0)));
            auto rhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->condition(1)));
            string op = logicOp->AND() ? "&&" : "||";
            return vector<unique_ptr<InstrAST>>{make_unique<BinCondExpressionAST>(op, move(lhs), move(rhs))};
        }

        if (auto binOp = ctx->binCondOp()) {
            auto lhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(0)));
            auto rhs = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->expression(1)));
            string op;
            if (binOp->LT()) op = "<";
            else if (binOp->GT()) op = ">";
            else if (binOp->EQ()) op = "==";
            else if (binOp->NEQ()) op = "!=";
            else if (binOp->LTE()) op = "<=";
            else if (binOp->GTE()) op = ">=";
            return vector<unique_ptr<InstrAST>>{make_unique<BinCondExpressionAST>(op, move(lhs), move(rhs))};
        }

        return visitChildren(ctx);
    }

    any visitValue(tlangParser::ValueContext *ctx) override {
        if (ctx->NUM()) {
            return vector<unique_ptr<InstrAST>>{make_unique<NumberExpressionAST>(stoi(ctx->NUM()->getText()))};
        }
        if (ctx->VAR()) {
            return vector<unique_ptr<InstrAST>>{make_unique<VariableExpressionAST>(ctx->VAR()->getText())};
        }
        throw runtime_error("Invalid value");
    }

    any visitLoop(tlangParser::LoopContext *ctx) override {
        repeatInstrCount++;
        auto repeatNum = any_cast<unique_ptr<ExpressionAST>>(visit(ctx->value()));
        
        auto counterVar = make_unique<VariableExpressionAST>(
            "__rep_counter_" + to_string(repeatInstrCount));
        
        vector<unique_ptr<InstrAST>> instructions;
        instructions.push_back(make_unique<CallExpressionAST>("assign", 
            vector<unique_ptr<ExpressionAST>>{
                counterVar->clone(),
                move(repeatNum)
            }
        ));

        auto zero = make_unique<NumberExpressionAST>(0);
        auto cond = make_unique<BinCondExpressionAST>(">", 
            counterVar->clone(),
            move(zero));

        auto body = any_cast<vector<unique_ptr<InstrAST>>>(visit(ctx->strict_ilist()));

        auto one = make_unique<NumberExpressionAST>(1);
        auto decrement = make_unique<CallExpressionAST>("assign",
            vector<unique_ptr<ExpressionAST>>{
                counterVar->clone(),
                make_unique<BinArithExpressionAST>('-', 
                    counterVar->clone(),
                    move(one))
            }
        );

        instructions.push_back(make_unique<BinCondExpressionAST>("while", move(cond), nullptr));
        move(body.begin(), body.end(), back_inserter(instructions));
        instructions.push_back(move(decrement));

        return instructions;
    }

    // Default implementations for remaining rules
    any visitMoveOp(tlangParser::MoveOpContext*) override { return nullptr; }
    any visitPauseCommand(tlangParser::PauseCommandContext*) override { return nullptr; }
    any visitValueExpr(tlangParser::ValueExprContext *ctx) override { return visit(ctx->value()); }
    any visitMultiplicative(tlangParser::MultiplicativeContext*) override { return nullptr; }
    any visitAdditive(tlangParser::AdditiveContext*) override { return nullptr; }
    any visitUnaryArithOp(tlangParser::UnaryArithOpContext*) override { return nullptr; }
    any visitBinCondOp(tlangParser::BinCondOpContext*) override { return nullptr; }
    any visitLogicOp(tlangParser::LogicOpContext*) override { return nullptr; }

private:
    template<typename T, typename U>
    unique_ptr<T> dynamic_unique_ptr_cast(unique_ptr<U>&& src) {
        if (auto ptr = dynamic_cast<T*>(src.get())) {
            src.release();
            return unique_ptr<T>(ptr);
        }
        throw bad_cast();
    }
};

unique_ptr<tlangVisitor> createChironVisitor() {
    return make_unique<ChironVisitorImpl>();
}