#include "tlangVisitor.h"
#include "chironAST.hpp"
#include <any>
#include <vector>
#include <stdexcept>
#include <string>
#include <utility>

using namespace std;

// Helper function to extract a single ExpressionAST* from an any
static ExpressionAST* getSingleExpr(const any &result) {
    auto vec = any_cast<vector<InstrAST*>>(result);
    if (vec.size() != 1)
        throw runtime_error("Expected a single expression");
    ExpressionAST* expr = dynamic_cast<ExpressionAST*>(vec[0]);
    if (!expr)
        throw runtime_error("Expression is not of type ExpressionAST*");
    return expr;
}

class ChironVisitorImpl : public tlangVisitor {
    int repeatInstrCount = 0;

public:
    any visitStart(tlangParser::StartContext *ctx) override {
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
        return visitChildren(ctx);
    }

    any visitIfConditional(tlangParser::IfConditionalContext *ctx) override {
        ExpressionAST* cond = getSingleExpr(visit(ctx->condition()));
        vector<InstrAST*> thenBlock = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist()));
        vector<InstrAST*> result;
        result.push_back(
            make_unique<BinCondExpressionAST>(
                "if",
                unique_ptr<ExpressionAST>(cond),
                nullptr
            ).release()
        );
        result.insert(result.end(), thenBlock.begin(), thenBlock.end());
        return result;
    }

    any visitIfElseConditional(tlangParser::IfElseConditionalContext *ctx) override {
        ExpressionAST* cond = getSingleExpr(visit(ctx->condition()));
        vector<InstrAST*> thenBlock = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist(0)));
        vector<InstrAST*> elseBlock = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist(1)));
        vector<InstrAST*> result;
        result.push_back(
            make_unique<BinCondExpressionAST>(
                "ifelse",
                unique_ptr<ExpressionAST>(cond),
                nullptr
            ).release()
        );
        result.insert(result.end(), thenBlock.begin(), thenBlock.end());
        result.insert(result.end(), elseBlock.begin(), elseBlock.end());
        return result;
    }

    any visitLoop(tlangParser::LoopContext *ctx) override {
        repeatInstrCount++;
        ExpressionAST* repeatNum = getSingleExpr(visit(ctx->value()));
        VariableExpressionAST* counterVar = new VariableExpressionAST("__rep_counter_" + to_string(repeatInstrCount));
        vector<InstrAST*> instructions;
        {   // Create assignment: __rep_counter = repeatNum
            vector<unique_ptr<ExpressionAST>> args;
            args.push_back(counterVar->clone());
            args.push_back(unique_ptr<ExpressionAST>(repeatNum));
            instructions.push_back(
                make_unique<CallExpressionAST>("assign", move(args)).release()
            );
        }
        // Create while condition: __rep_counter > 0
        unique_ptr<ExpressionAST> cond = make_unique<BinCondExpressionAST>(
            ">",
            counterVar->clone(),
            make_unique<NumberExpressionAST>(0)
        );
        // Get loop body instructions.
        vector<InstrAST*> body = any_cast<vector<InstrAST*>>(visit(ctx->strict_ilist()));
        // Create decrement: __rep_counter = __rep_counter - 1
        unique_ptr<ExpressionAST> decrementExpr = make_unique<BinArithExpressionAST>(
            '-',
            counterVar->clone(),
            make_unique<NumberExpressionAST>(1)
        );
        vector<unique_ptr<ExpressionAST>> argsDec;
        argsDec.push_back(counterVar->clone());
        argsDec.push_back(move(decrementExpr));
        InstrAST* decrementCall = make_unique<CallExpressionAST>("assign", move(argsDec)).release();
        instructions.push_back(
            make_unique<BinCondExpressionAST>("while", move(cond), nullptr).release()
        );
        instructions.insert(instructions.end(), body.begin(), body.end());
        instructions.push_back(decrementCall);
        return instructions;
    }

    any visitGotoCommand(tlangParser::GotoCommandContext *ctx) override {
        ExpressionAST* x = getSingleExpr(visit(ctx->expression(0)));
        ExpressionAST* y = getSingleExpr(visit(ctx->expression(1)));
        auto xNum = dynamic_cast<NumberExpressionAST*>(x);
        auto yNum = dynamic_cast<NumberExpressionAST*>(y);
        if (!xNum || !yNum)
            throw runtime_error("Goto requires numeric arguments");
        vector<InstrAST*> result;
        result.push_back(
            make_unique<GotoCallExprAST>(xNum->getVal(), yNum->getVal()).release()
        );
        return result;
    }

    any visitAssignment(tlangParser::AssignmentContext *ctx) override {
        VariableExpressionAST* var = new VariableExpressionAST(ctx->VAR()->getText());
        ExpressionAST* expr = getSingleExpr(visit(ctx->expression()));
        return vector<InstrAST*>{
            new BinArithExpressionAST('=', unique_ptr<ExpressionAST>(var), unique_ptr<ExpressionAST>(expr))
        };
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
            ExpressionAST* cond = getSingleExpr(visit(ctx->condition(0)));
            return vector<InstrAST*>{
                make_unique<UnaryArithExpressionAST>('!', unique_ptr<ExpressionAST>(cond)).release()
            };
        }
        if (ctx->logicOp()) {
            ExpressionAST* lhs = getSingleExpr(visit(ctx->condition(0)));
            ExpressionAST* rhs = getSingleExpr(visit(ctx->condition(1)));
            string op = ctx->logicOp()->AND() ? "&&" : "||";
            return vector<InstrAST*>{
                make_unique<BinCondExpressionAST>(op, unique_ptr<ExpressionAST>(lhs), unique_ptr<ExpressionAST>(rhs)).release()
            };
        }
        if (ctx->binCondOp()) {
            ExpressionAST* lhs = getSingleExpr(visit(ctx->expression(0)));
            ExpressionAST* rhs = getSingleExpr(visit(ctx->expression(1)));
            string op;
            if (ctx->binCondOp()->LT())      op = "<";
            else if (ctx->binCondOp()->GT()) op = ">";
            else if (ctx->binCondOp()->EQ()) op = "==";
            else if (ctx->binCondOp()->NEQ()) op = "!=";
            else if (ctx->binCondOp()->LTE()) op = "<=";
            else if (ctx->binCondOp()->GTE()) op = ">=";
            return vector<InstrAST*>{
                make_unique<BinCondExpressionAST>(op, unique_ptr<ExpressionAST>(lhs), unique_ptr<ExpressionAST>(rhs)).release()
            };
        }
        return visitChildren(ctx);
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



