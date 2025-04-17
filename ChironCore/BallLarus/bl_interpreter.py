from interpreter import ConcreteInterpreter, Interpreter, ProgramContext, addContext
from ChironAST import ChironAST
from ChironHooks import Chironhooks
import os

class BallLarusInterpreter(ConcreteInterpreter):
    """
    A specialized interpreter that extends ConcreteInterpreter with Ball-Larus path profiling.
    It preserves all original functionality while adding support for PrintCommand, IncrementCommand,
    and DumpCommand instructions.
    """
    
    def __init__(self, irHandler, params,predictor_hashMap = {}, is_bl_op = False, is_training=False):
        super().__init__(irHandler, params)
        # Initialize the hashMap for path register tracking
        self.hashMap = {}
        self.predictor = predictor_hashMap
        self.bl_op = is_bl_op
        self.isTraining = is_training
        self.total_cnt = 0
        self.correct_cnt = 0
    def interpret(self):
        """
        Executes one instruction at the current program counter. Returns True when the program finishes,
        False otherwise.
        """
        print("Program counter : ", self.pc)
        stmt, tgt = self.ir[self.pc]
        print(stmt, stmt.__class__.__name__, tgt)

        self.sanityCheck(self.ir[self.pc])

        if isinstance(stmt, ChironAST.AssignmentCommand):
            ntgt = self.handleAssignment(stmt, tgt)
        elif isinstance(stmt, ChironAST.ConditionCommand):
            if self.bl_op:
                ntgt = self.handleCondition_bl(stmt, tgt)
            else:
                ntgt = self.handleCondition(stmt, tgt)
        elif isinstance(stmt, ChironAST.MoveCommand):
            ntgt = self.handleMove(stmt, tgt)
        elif isinstance(stmt, ChironAST.PenCommand):
            ntgt = self.handlePen(stmt, tgt)
        elif isinstance(stmt, ChironAST.GotoCommand):
            ntgt = self.handleGotoCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.NoOpCommand):
            ntgt = self.handleNoOpCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.PrintCommand):
            ntgt = self.handlePrintCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.IncrementCommand):
            ntgt = self.handleIncrementCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.DumpCommand):
            ntgt = self.handleDumpCommand(stmt, tgt)
        else:
            raise NotImplementedError("Unknown instruction: %s, %s." % (type(stmt), stmt))

        self.pc += ntgt

        if self.pc >= len(self.ir):
            # This is the ending of the interpreter.
            if self.bl_op and self.isTraining == False:
                with open("predictor_accuracy.txt", "a") as f:
                    f.write(f"Total Count: {self.total_cnt}\n")
                    f.write(f"Correct Count: {self.correct_cnt}\n")
                    f.write(f"Accuracy: {self.correct_cnt / self.total_cnt if self.total_cnt > 0 else 0}\n")
                    f.write("-----------------------\n")

            self.trtl.write("End, Press ESC", font=("Arial", 15, "bold"))
            if self.args is not None and self.args.hooks:
                self.chironhook.ChironEndHook(self)
            return True
        else:
            return False
    
    def handleCondition_bl(self, stmt, tgt):
        print("  Branch Instruction")
        condstr = addContext(stmt)
        exec("self.cond_eval = %s" % (condstr))
        exprStr = addContext(":blPathRegister")
        path_reg_val = eval(exprStr)
        if(self.isTraining):
            if self.cond_eval:
                self.predictor[(path_reg_val, self.pc)] = self.predictor.get((path_reg_val, self.pc), 0) + 1
            else:
                self.predictor[(path_reg_val, self.pc)] = self.predictor.get((path_reg_val, self.pc), 0) - 1

        else:
            self.total_cnt += 1
            predictor_val = self.predictor.get((path_reg_val, self.pc), 0)
            if predictor_val >= 0 and self.cond_eval:
                self.correct_cnt += 1
            elif predictor_val < 0 and not self.cond_eval:
                self.correct_cnt += 1
            # if (path_reg_val, self.pc) in self.predictor:
            #     if self.cond_eval and self.predictor[(path_reg_val, self.pc)] > 0:
            #         self.correct_cnt += 1
            #     elif not self.cond_eval and self.predictor[(path_reg_val, self.pc)] < 0:
            #         self.correct_cnt += 1
        return 1 if self.cond_eval else tgt
    
    def handlePrintCommand(self, stmt, tgt):
        """
        Handles a PrintCommand by evaluating the expression and writing the result to print_output.txt.
        """
        print(" PrintCommand")
        # Convert the expression to a string that can be evaluated
        exprStr = addContext(stmt.expr)
        # Evaluate the expression in the current program context
        result = eval(exprStr)
        # Dump the result to a file instead of printing to the console
        with open("print_output.txt", "a") as f:
            f.write(str(exprStr) + " = " + str(result) + "\n")
        return 1

    def handleIncrementCommand(self, stmt, tgt):
        """
        Handles an IncrementCommand by incrementing the value for the specified key in the hashMap.
        """
        print("  IncrementCommand")
        exprStr = addContext(stmt.var)
        key = eval(exprStr)
        current_value = self.hashMap.get(key, 0)
        self.hashMap[key] = current_value + 1
        return 1

    def handleDumpCommand(self, stmt, tgt):
        """
        Merge current self.hashMap into hash_dump.txt:
        - For keys already in the file, add the new count.
        - For new keys, append them.
        """
        print("  DumpCommand")
        dump_file = "hash_dump.txt"
        
        # 1) Load existing counts from disk (if the file exists)
        existing = {}

        if os.path.exists(dump_file):
            with open(dump_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Expect lines like "key: value"
                    key, val = line.split(":", 1)
                    existing[key.strip()] = existing.get(key.strip(), 0) + int(val.strip())

        # 2) Merge in-memory hashMap counts
        for k, v in self.hashMap.items():
            existing[str(k)] = existing.get(str(k), 0) + v

        # 3) Write the merged result back out
        with open(dump_file, "w") as f:
            for key, val in existing.items():
                f.write(f"{key}: {val}\n")

        return 1
