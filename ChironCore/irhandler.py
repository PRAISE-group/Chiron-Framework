import antlr4
import pickle

from turtparse.parseError import *
from turtparse.tlangParser import tlangParser
from turtparse.tlangLexer import tlangLexer

from ChironAST import ChironAST
from ChironAST import ChironTAC


def getParseTree(progfl):
    input_stream = antlr4.FileStream(progfl)
    print(input_stream)
    try:
        lexer = tlangLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        lexer._listeners = [SyntaxErrorListener()]
        tparser = tlangParser(stream)
        tparser._listeners = [SyntaxErrorListener()]
        tree = tparser.start()
    except Exception as e:
        print("\033[91m\n====================")
        print(e.__str__() + "\033[0m\n")
        exit(1)

    return tree


class IRHandler:
    def __init__(self, ir=None, cfg=None):
        # statement list
        self.ir = ir
        # control flow graph
        self.cfg = cfg

    def setIR(self, ir):
        self.ir = ir

    def setCFG(self, cfg):
        self.cfg = cfg

    def dumpIR(self, filename, ir):
        with open(filename, "wb") as f:
            pickle.dump(ir, f)

    def loadIR(self, filename):
        f = open(filename, "rb")
        ir = pickle.load(f)
        self.ir = ir
        return ir

    def updateJump(self, stmtList, index, pos):
        stmt, tgt = stmtList[index]
        # Don't update the conditional nodes whose
        # loops and targets are above the insertion point
        # since these don't get affected in any way.
        if tgt > 0 and index + tgt > pos:
            newTgt = tgt + 1
            # update curr conditional instruction's target
            stmtList[index] = (stmt, newTgt)
            # update the target instruction's jump value
            # if it is a backedge, else leave it as is.
            backJumpInstr, backJmpTgt = stmtList[index + tgt - 1]
            if backJmpTgt < 0:
                print(f"Loop Target : {backJumpInstr}, {backJmpTgt}")
                stmtList[index + tgt - 1] = (backJumpInstr, backJmpTgt - 1)

    def addInstruction(self, stmtList, inst, pos):
        """[summary]

        Args:
            stmtList ([List]): List of IR Statments
            inst ([ChironAST.Instruction type]): Instruction to be added. Should be of type Instruction(AST).
            pos ([int]): Position in IR List to add the instruction.
        """
        if pos >= len(stmtList):
            print("[error] POSITION given is past the instruction list.")
            return

        if isinstance(inst, ChironAST.ConditionCommand):
            print("[Skip] Instruction Type not supported for addition. \n")
            return
        index = 0

        # We must consider the conditional jumps and targets of
        # instructions that appear before the position where the
        # instruction must be added. Other conditional statements
        # will just shift without change of labels since
        # all the jump target numbers are relative.
        while index < pos:
            if isinstance(stmtList[index][0], ChironAST.ConditionCommand):
                # Update the target of this conditional statement and the
                # target statment's target number accordingly.
                updateJump(stmtList, index, pos)
            index += 1
        # We only allow non-jump statement addition as of now.
        stmtList.insert(pos, (inst, 1))

    def removeInstruction(self, stmtList, pos):
        """[summary]

        Replace by a no-op as of now. (Sumit: Kinda works)

        Args:
            stmtList ([List]): List of IR Statments
            pos ([int]): Position in IR List to remove the instruction.
        """
        if pos >= len(stmtList):
            print("[error] POSITION given is past the instruction list.")
            return

        inst = stmtList[pos][0]
        if isinstance(inst, ChironAST.ConditionCommand):
            print("[Skip] Instruction Type not supported for removal. \n")
            return

        if ":__rep_counter_" in str(stmtList[pos][0]):
            print("[Skip] Instruction affecting loop counter. \n")
            return

        # We only allow non-jump/non-conditional statement removal as of now.
        stmtList[pos] = (ChironAST.NoOpCommand(), 1)

    def pretty_print(self, irList):
        """
        We pass a IR list and print it here.
        """
        print("\n========== Chiron IR ==========\n")
        print(
            "The first label before the opcode name represents the IR index or label \non the control flow graph for that node.\n"
        )
        print(
            "The number after the opcode name represents the jump offset \nrelative to that statement.\n"
        )
        for idx, item in enumerate(irList):
            print(f"[L{idx}]".rjust(5), item[0], f"[{item[1]}]")


"""
Class for converting IR to Three Address Code (TAC)
"""


class TACGenerator:
    def __init__(self, ir):
        self.ir = ir
        self.tac = []
        self.tempCount = 0
        self.branchCount = 0
        self.assertCount = 0
        self.moveCount = 0
        self.gotoCount = 0
        self.ast_to_tac_line = {}
        self.line = 0

    def parseExpresssion(self, expr, dest):
        """
        Parse the expression and return the TAC for the expression.
        """
        if isinstance(expr, ChironAST.BinArithOp):
            left = None
            right = None
            if isinstance(expr.lexpr, ChironAST.Num):
                left = ChironTAC.TAC_Num(expr.lexpr.val)
            elif isinstance(expr.lexpr, ChironAST.Var):
                left = ChironTAC.TAC_Var(expr.lexpr.varname)
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                left = temp
                self.parseExpresssion(expr.lexpr, temp)

            if isinstance(expr.rexpr, ChironAST.Num):
                right = ChironTAC.TAC_Num(expr.rexpr.val)
            elif isinstance(expr.rexpr, ChironAST.Var):
                right = ChironTAC.TAC_Var(expr.rexpr.varname)
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                right = temp
                self.parseExpresssion(expr.rexpr, temp)

            self.line += 1
            self.tac.append(
                (ChironTAC.TAC_AssignmentCommand(dest, left, right, expr.symbol), 1)
            )
        elif isinstance(expr, ChironAST.UMinus):
            if isinstance(expr.expr, ChironAST.Num):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.TAC_AssignmentCommand(
                            dest,
                            ChironTAC.TAC_Num(0),
                            ChironTAC.TAC_Num(expr.expr.val),
                            "-",
                        ),
                        1,
                    ),
                )
            elif isinstance(expr.expr, ChironAST.Var):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.TAC_AssignmentCommand(
                            dest,
                            ChironTAC.TAC_Num(0),
                            ChironTAC.TAC_Var(expr.expr.varname),
                            "-",
                        ),
                        1,
                    ),
                )
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                self.parseExpresssion(expr.expr, temp)
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.TAC_AssignmentCommand(
                            dest, ChironTAC.TAC_Num(0), temp, "-"
                        ),
                        1,
                    )
                )
        elif isinstance(expr, ChironAST.BinCondOp) and not (
            isinstance(expr, ChironAST.AND)
            or isinstance(expr, ChironAST.OR)
            or isinstance(expr, ChironAST.NOT)
        ):
            left = None
            right = None
            if isinstance(expr.lexpr, ChironAST.Num):
                left = ChironTAC.TAC_Num(expr.lexpr.val)
            elif isinstance(expr.lexpr, ChironAST.Var):
                left = ChironTAC.TAC_Var(expr.lexpr.varname)
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                left = temp
                self.parseExpresssion(expr.lexpr, temp)

            if isinstance(expr.rexpr, ChironAST.Num):
                right = ChironTAC.TAC_Num(expr.rexpr.val)
            elif isinstance(expr.rexpr, ChironAST.Var):
                right = ChironTAC.TAC_Var(expr.rexpr.varname)
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                right = temp
                self.parseExpresssion(expr.rexpr, temp)

            self.line += 1
            self.tac.append(
                (ChironTAC.TAC_AssignmentCommand(dest, left, right, expr.symbol), 1)
            )
        elif isinstance(expr, ChironAST.AND) or isinstance(expr, ChironAST.OR):
            left = None
            right = None
            if isinstance(expr.lexpr, ChironAST.BoolTrue):
                left = ChironTAC.TAC_BoolTrue()
            elif isinstance(expr.lexpr, ChironAST.BoolFalse):
                left = ChironTAC.TAC_BoolFalse()
            elif isinstance(expr.lexpr, ChironAST.Var):
                left = ChironTAC.TAC_Var(expr.lexpr.varname)
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                left = temp
                self.parseExpresssion(expr.lexpr, temp)

            if isinstance(expr.rexpr, ChironAST.BoolTrue):
                right = ChironTAC.TAC_BoolTrue()
            elif isinstance(expr.rexpr, ChironAST.BoolFalse):
                right = ChironTAC.TAC_BoolFalse()
            elif isinstance(expr.rexpr, ChironAST.Var):
                right = ChironTAC.TAC_Var(expr.rexpr.varname)
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                right = temp
                self.parseExpresssion(expr.rexpr, temp)

            self.line += 1
            self.tac.append(
                (ChironTAC.TAC_AssignmentCommand(dest, left, right, expr.symbol), 1)
            )
        elif isinstance(expr, ChironAST.NOT):
            if isinstance(expr.expr, ChironAST.BoolTrue):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.TAC_AssignmentCommand(
                            dest,
                            ChironTAC.TAC_Unused(),
                            ChironTAC.TAC_BoolTrue(),
                            "not",
                        ),
                        1,
                    )
                )
            elif isinstance(expr.expr, ChironAST.BoolFalse):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.TAC_AssignmentCommand(
                            dest,
                            ChironTAC.TAC_Unused(),
                            ChironTAC.TAC_BoolFalse(),
                            "not",
                        ),
                        1,
                    )
                )
            elif isinstance(expr.expr, ChironAST.Var):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.TAC_AssignmentCommand(
                            dest,
                            ChironTAC.TAC_Unused(),
                            ChironTAC.TAC_Var(expr.expr.varname),
                            "not",
                        ),
                        1,
                    )
                )
            else:
                temp = ChironTAC.TAC_Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                self.parseExpresssion(expr.expr, temp)
                self.line += 1
                self.tac.append(
                    (ChironTAC.TAC_AssignmentCommand(dest, None, temp, "not"), 1)
                )
        elif isinstance(expr, ChironAST.Var):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.TAC_AssignmentCommand(
                        dest, ChironTAC.TAC_Num(0), ChironTAC.TAC_Var(expr.varname), "+"
                    ),
                    1,
                )
            )
        elif isinstance(expr, ChironAST.Num):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.TAC_AssignmentCommand(
                        dest, ChironTAC.TAC_Num(0), ChironTAC.TAC_Num(expr.val), "+"
                    ),
                    1,
                )
            )
        elif isinstance(expr, ChironAST.BoolTrue):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.TAC_AssignmentCommand(
                        dest, ChironTAC.TAC_Unused(), ChironTAC.TAC_BoolTrue(), ""
                    ),
                    1,
                )
            )
        elif isinstance(expr, ChironAST.BoolFalse):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.TAC_AssignmentCommand(
                        dest, ChironTAC.TAC_Unused(), ChironTAC.TAC_BoolFalse(), ""
                    ),
                    1,
                )
            )
        else:
            raise NotImplementedError(
                "Unknown expression: %s, %s." % (type(expr), expr)
            )

    def generateTAC(self):
        line_number = 0
        for stmt, tgt in self.ir:
            self.ast_to_tac_line[line_number] = self.line
            line_number += 1

            if isinstance(stmt, ChironAST.AssignmentCommand):
                self.parseExpresssion(stmt.rexpr, ChironTAC.TAC_Var(stmt.lvar.varname))

            elif isinstance(stmt, ChironAST.ConditionCommand):
                branchvar = None
                if isinstance(stmt.cond, ChironAST.BoolTrue):
                    branchvar = ChironTAC.TAC_BoolTrue()
                elif isinstance(stmt.cond, ChironAST.BoolFalse):
                    branchvar = ChironTAC.TAC_BoolFalse()
                elif isinstance(stmt.cond, ChironAST.Var):
                    branchvar = ChironTAC.TAC_Var(stmt.cond.varname)
                else:
                    branchvar = ChironTAC.TAC_Var(f":__branch_{self.branchCount}")
                    self.branchCount += 1
                    self.parseExpresssion(stmt.cond, branchvar)
                newtgt = line_number - 1 + tgt  # Adjusted later
                self.line += 1
                self.tac.append((ChironTAC.TAC_ConditionCommand(branchvar), newtgt))
            elif isinstance(stmt, ChironAST.AssertCommand):
                assertvar = ChironTAC.TAC_Var(f":__assert_{self.assertCount}")
                self.assertCount += 1
                self.parseExpresssion(stmt.cond, assertvar)
                self.line += 1
                self.tac.append((ChironTAC.TAC_AssertCommand(assertvar), 1))
            elif isinstance(stmt, ChironAST.MoveCommand):
                movevar = None
                if isinstance(stmt.expr, ChironAST.Num):
                    movevar = ChironTAC.TAC_Num(stmt.expr.val)
                elif isinstance(stmt.expr, ChironAST.Var):
                    movevar = ChironTAC.TAC_Var(stmt.expr.varname)
                else:
                    movevar = ChironTAC.TAC_Var(f":__move_{self.moveCount}")
                    self.moveCount += 1
                    self.parseExpresssion(stmt.expr, movevar)
                self.line += 1
                self.tac.append((ChironTAC.TAC_MoveCommand(stmt.direction, movevar), 1))
            elif isinstance(stmt, ChironAST.PenCommand):
                self.line += 1
                self.tac.append((ChironTAC.TAC_PenCommand(stmt.status), 1))
            elif isinstance(stmt, ChironAST.GotoCommand):
                xvar = None
                yvar = None
                if isinstance(stmt.xcor, ChironAST.Num):
                    xvar = ChironTAC.TAC_Num(stmt.xcor.val)
                elif isinstance(stmt.xcor, ChironAST.Var):
                    xvar = ChironTAC.TAC_Var(stmt.xcor.varname)
                else:
                    xvar = ChironTAC.TAC_Var(f":__x_{self.gotoCount}")
                    self.gotoCount += 1
                    self.parseExpresssion(stmt.xcor, xvar)
                if isinstance(stmt.ycor, ChironAST.Num):
                    yvar = ChironTAC.TAC_Num(stmt.ycor.val)
                elif isinstance(stmt.ycor, ChironAST.Var):
                    yvar = ChironTAC.TAC_Var(stmt.ycor.varname)
                else:
                    yvar = ChironTAC.TAC_Var(f":__y_{self.gotoCount}")
                    self.gotoCount += 1
                    self.parseExpresssion(stmt.ycor, yvar)
                self.line += 1
                self.tac.append((ChironTAC.TAC_GotoCommand(xvar, yvar), 1))
            elif isinstance(stmt, ChironAST.NoOpCommand):
                self.line += 1
                self.tac.append((ChironTAC.TAC_NoOpCommand(), 1))
            elif isinstance(stmt, ChironAST.PauseCommand):
                self.line += 1
                self.tac.append((ChironTAC.TAC_PauseCommand(), 1))
            else:
                raise NotImplementedError(
                    "Unknown instruction: %s, %s." % (type(stmt), stmt)
                )

        self.ast_to_tac_line[line_number] = self.line

        for i in range(len(self.tac)):
            stmt, tgt = self.tac[i]
            if isinstance(stmt, ChironTAC.TAC_ConditionCommand):
                newtgt = self.ast_to_tac_line[tgt] - i
                self.tac[i] = (stmt, newtgt)

    def printTAC(self):
        for (stmt, tgt), line in zip(self.tac, range(len(self.tac))):
            print(f"[L{line}]".rjust(5), stmt, f"[{tgt}]")
