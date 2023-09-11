import antlr4
import pickle

from turtparse.parseError import *
from turtparse.tlangParser import tlangParser
from turtparse.tlangLexer import tlangLexer

from ChironAST import ChironAST


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

        if "__rep_counter_" in str(stmtList[pos][0]):
            print("[Skip] Instruction affecting loop counter. \n")
            return

        # We only allow non-jump/non-conditional statement removal as of now.
        stmtList[pos] = (ChironAST.NoOpCommand(), 1)

    def pretty_print(self, irList):
        """
            We pass a IR list and print it here.
        """
        print("\n========== Chiron IR ==========\n")
        print("The first label before the opcode name represents the IR index or label \non the control flow graph for that node.\n")
        print("The number after the opcode name represents the jump offset \nrelative to that statement.\n")
        for idx, item in enumerate(irList):
            print(f"[L{idx}]".rjust(5), item[0], f"[{item[1]}]")