from ChironSSA import ChironSSA
from cfg import cfgBuilder
import ChironTAC.ChironTAC as ChironTAC
import cfg.ChironCFG as ChironCFG 
import networkx as nx
import copy
import collections

class SSABuilder:
    def __init__(self, cfg : ChironCFG.ChironCFG):
        self.cfg = cfg
        self.globals = set()
        self.blocksMap = collections.defaultdict(set)
        self.counter = collections.defaultdict(int)
        self.stack = collections.defaultdict(list)

    def build(self):
        self.cfg.compute_dominance()
        self.insert_phi_nodes()
        self.rename_variables()

        # save the SSA CFG as png
        cfgBuilder.dumpCFG(self.cfg, "cfg")

    def rename_variables(self):
        for var in self.globals:
            self.counter[var] = 0
            self.stack[var] = []

        entry = None
        for block in self.cfg.nodes():
            if block.name == "START":
                entry = block
                break

        self.rename(entry)

    def rename(self, block): # TODO
        print("renaming block: ", block.name)
        for instr, _ in block.instrlist:
            temp = set()
            if isinstance(instr, ChironSSA.PhiCommand):
                temp.add(instr.lvar.name)
                instr.lvar = self.new_name(instr.lvar.name)

            elif isinstance(instr, ChironTAC.AssignmentCommand):
                instr.lvar = self.new_name(instr.lvar.name)
                if isinstance(instr.rvar1, ChironTAC.Var):
                    instr.rvar1 = ChironSSA.Var(instr.rvar1.name + "__" + str(self.stack[instr.rvar1.name][-1]))
                if isinstance(instr.rvar2, ChironTAC.Var):
                    instr.rvar2 = ChironSSA.Var(instr.rvar2.name + "__" + str(self.stack[instr.rvar2.name][-1]))

            elif isinstance(instr, ChironTAC.AssertCommand):
                if isinstance(instr.cond, ChironTAC.Var):
                    instr.cond = ChironSSA.Var(instr.cond.name + "__" + str(self.stack[instr.cond.name][-1]))

            elif isinstance(instr, ChironTAC.ConditionCommand):
                if isinstance(instr.cond, ChironTAC.Var):
                    instr.cond = ChironSSA.Var(instr.cond.name + "__" + str(self.stack[instr.cond.name][-1]))

            elif isinstance(instr, ChironTAC.MoveCommand):
                if isinstance(instr.var, ChironTAC.Var):
                    instr.var = ChironSSA.Var(instr.var.name + "__" + str(self.stack[instr.var.name][-1]))

            elif isinstance(instr, ChironTAC.GotoCommand):
                if isinstance(instr.xcor, ChironTAC.Var):
                    instr.xcor = ChironSSA.Var(instr.xcor.name + "__" + str(self.stack[instr.xcor.name][-1]))
                if isinstance(instr.ycor, ChironTAC.Var):
                    instr.ycor = ChironSSA.Var(instr.ycor.name + "__" + str(self.stack[instr.ycor.name][-1]))

        print("df: ", self.cfg.df[block], "idom: ", self.cfg.idom[block].name)
        for next in self.cfg.df[block]:
            print("idom: ", self.cfg.idom[next].name)
            if self.cfg.idom[next] == block:
                self.rename(next)

        for var in temp:
            self.stack[var].pop()

    def new_name(self, var):
        i = self.counter[var]
        self.counter[var] += 1
        self.stack[var].append(i)
        return ChironSSA.Var(var + "__" + str(i))

    def insert_phi_nodes(self):
        for var in self.get_globals():
            if var not in self.blocksMap:
                continue

            worklist = self.blocksMap[var]
            while len(worklist) > 0:
                block = worklist.pop()
                for next in self.cfg.df[block]:
                    found = False
                    for instr, _ in next.instrlist:
                        if isinstance(instr, ChironSSA.PhiCommand) and instr.lvar.name == var:
                            found = True
                            instr.rvars.append(ChironSSA.Var(var))
                            break

                    if not found:
                        phi = ChironSSA.PhiCommand(ChironSSA.Var(var), [ChironSSA.Var(var)])
                        next.instrlist.insert(0, (phi, None))
                        worklist.add(next)

    def get_globals(self):
        if len(self.globals) > 0:
            return self.globals

        for block in self.cfg.nodes():
            varkill = set()
            for instr, _ in block.instrlist:
                if isinstance(instr, ChironTAC.AssignmentCommand):
                    if isinstance(instr.rvar1, ChironTAC.Var) and instr.rvar1.name not in varkill:
                        self.globals.add(instr.rvar1.name)
                    if isinstance(instr.rvar2, ChironTAC.Var) and instr.rvar2.name not in varkill:
                        self.globals.add(instr.rvar2.name)

                    varkill.add(instr.lvar.name)
                    self.blocksMap[instr.lvar.name].add(block)

                elif isinstance(instr, ChironTAC.AssertCommand):
                    if isinstance(instr.cond, ChironTAC.Var) and instr.cond.name not in varkill:
                        self.globals.add(instr.cond.name)

                elif isinstance(instr, ChironTAC.ConditionCommand):
                    if isinstance(instr.cond, ChironTAC.Var) and instr.cond.name not in varkill:
                        self.globals.add(instr.cond.name)

                elif isinstance(instr, ChironTAC.MoveCommand):
                    if isinstance(instr.var, ChironTAC.Var) and instr.var.name not in varkill:
                        self.globals.add(instr.var.name)

                elif isinstance(instr, ChironTAC.GotoCommand):
                    if isinstance(instr.xcor, ChironTAC.Var) and instr.xcor.name not in varkill:
                        self.globals.add(instr.xcor.name)
                    if isinstance(instr.ycor, ChironTAC.Var) and instr.ycor.name not in varkill:
                        self.globals.add(instr.ycor.name)

        return self.globals

