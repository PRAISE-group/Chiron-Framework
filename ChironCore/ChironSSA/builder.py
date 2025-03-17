from numpy import format_float_scientific
from ChironSSA import ChironSSA
from cfg import cfgBuilder
import ChironTAC.ChironTAC as ChironTAC
import ChironSSA.ChironSSA as ChironSSA
import cfg.ChironCFG as ChironCFG 
import networkx as nx
import copy
import collections

class SSABuilder:
    def __init__(self, ir):
        self.convert(ir)
        self.cfg, self.line2BlockMap = cfgBuilder.buildCFG(ir)
        self.globals = set()
        self.blocksMap = collections.defaultdict(set)
        self.counter = collections.defaultdict(int)
        self.stack = collections.defaultdict(list)

    def build(self):
        self.cfg.compute_dominance()
        self.insert_phi_nodes()
        self.rename_variables()
        self.remove_empty_phi()

        return self.cfg
    
    def remove_empty_phi(self):
        for block in self.cfg.nodes():
            for instr, _ in block.instrlist:
                if isinstance(instr, ChironSSA.PhiCommand) and len(instr.rvars) == 0:
                    block.instrlist.remove((instr, None))

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

    def rename(self, block):
        temp = set()
        for instr, _ in block.instrlist:
            if isinstance(instr, ChironSSA.PhiCommand):
                temp.add(instr.lvar.name)
                instr.lvar = self.new_name(instr.lvar.name)

            elif isinstance(instr, ChironSSA.AssignmentCommand):
                temp.add(instr.lvar.name)
                instr.lvar = self.new_name(instr.lvar.name)
                if isinstance(instr.rvar1, ChironSSA.Var):
                    instr.rvar1 = ChironSSA.Var(instr.rvar1.name + "$" + str(self.stack[instr.rvar1.name][-1]))
                if isinstance(instr.rvar2, ChironSSA.Var):
                    instr.rvar2 = ChironSSA.Var(instr.rvar2.name + "$" + str(self.stack[instr.rvar2.name][-1]))

            elif isinstance(instr, ChironSSA.AssertCommand):
                if isinstance(instr.cond, ChironSSA.Var):
                    instr.cond = ChironSSA.Var(instr.cond.name + "$" + str(self.stack[instr.cond.name][-1]))

            elif isinstance(instr, ChironSSA.ConditionCommand):
                if isinstance(instr.cond, ChironSSA.Var):
                    instr.cond = ChironSSA.Var(instr.cond.name + "$" + str(self.stack[instr.cond.name][-1]))

            elif isinstance(instr, ChironSSA.MoveCommand):
                if isinstance(instr.var, ChironSSA.Var):
                    instr.var = ChironSSA.Var(instr.var.name + "$" + str(self.stack[instr.var.name][-1]))

            elif isinstance(instr, ChironSSA.GotoCommand):
                if isinstance(instr.xcor, ChironSSA.Var):
                    instr.xcor = ChironSSA.Var(instr.xcor.name + "$" + str(self.stack[instr.xcor.name][-1]))
                if isinstance(instr.ycor, ChironSSA.Var):
                    instr.ycor = ChironSSA.Var(instr.ycor.name + "$" + str(self.stack[instr.ycor.name][-1]))

            elif isinstance(instr, ChironSSA.SinCommand):
                temp.add(instr.lvar.name)
                instr.lvar = self.new_name(instr.lvar.name)
                if isinstance(instr.rvar, ChironSSA.Var):
                    instr.rvar = ChironSSA.Var(instr.rvar.name + "$" + str(self.stack[instr.rvar.name][-1]))

            elif isinstance(instr, ChironSSA.CosCommand):
                temp.add(instr.lvar.name)
                instr.lvar = self.new_name(instr.lvar.name)
                if isinstance(instr.rvar, ChironSSA.Var):
                    instr.rvar = ChironSSA.Var(instr.rvar.name + "$" + str(self.stack[instr.rvar.name][-1]))
            
            elif isinstance(instr, ChironSSA.DegToRadCommand):
                temp.add(instr.lvar.name)
                instr.lvar = self.new_name(instr.lvar.name)
                if isinstance(instr.rvar, ChironSSA.Var):
                    instr.rvar = ChironSSA.Var(instr.rvar.name + "$" + str(self.stack[instr.rvar.name][-1]))

        visited = set()
        def phi_dfs(curr, var):
            visited.add(curr)
            flag = False
            for instr, _ in curr.instrlist:
                if isinstance(instr, ChironSSA.PhiCommand):
                    if instr.lvar.name == var:
                        instr.rvars.append(ChironSSA.Var(instr.lvar.name + "$" + str(self.stack[instr.lvar.name][-1])))
                        flag = True

            if not flag:
                for next in self.cfg.successors(curr):
                    if next in visited:
                        continue
                    phi_dfs(next, var)

        for next in self.cfg.successors(block):
            for var in temp:
                phi_dfs(next, var)

        for next in self.cfg.dominator_tree[block]:
            self.rename(next)

        for var in temp:
            self.stack[var].pop()

    def new_name(self, var):
        i = self.counter[var]
        self.counter[var] += 1
        self.stack[var].append(i)
        return ChironSSA.Var(var + "$" + str(i))

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
                            break

                    if not found:
                        phi = ChironSSA.PhiCommand(ChironSSA.Var(var), [])
                        next.instrlist.insert(0, (phi, None))
                        worklist.add(next)

    def get_globals(self):
        if len(self.globals) > 0:
            return self.globals

        for block in self.cfg.nodes():
            varkill = set()
            for instr, _ in block.instrlist:
                if isinstance(instr, ChironSSA.AssignmentCommand):
                    if isinstance(instr.rvar1, ChironSSA.Var) and instr.rvar1.name not in varkill:
                        self.globals.add(instr.rvar1.name)
                    if isinstance(instr.rvar2, ChironSSA.Var) and instr.rvar2.name not in varkill:
                        self.globals.add(instr.rvar2.name)

                    varkill.add(instr.lvar.name)
                    self.blocksMap[instr.lvar.name].add(block)

                elif isinstance(instr, ChironSSA.AssertCommand):
                    if isinstance(instr.cond, ChironSSA.Var) and instr.cond.name not in varkill:
                        self.globals.add(instr.cond.name)

                elif isinstance(instr, ChironSSA.ConditionCommand):
                    if isinstance(instr.cond, ChironSSA.Var) and instr.cond.name not in varkill:
                        self.globals.add(instr.cond.name)

                elif isinstance(instr, ChironSSA.MoveCommand):
                    if isinstance(instr.var, ChironSSA.Var) and instr.var.name not in varkill:
                        self.globals.add(instr.var.name)

                elif isinstance(instr, ChironSSA.GotoCommand):
                    if isinstance(instr.xcor, ChironSSA.Var) and instr.xcor.name not in varkill:
                        self.globals.add(instr.xcor.name)
                    if isinstance(instr.ycor, ChironSSA.Var) and instr.ycor.name not in varkill:
                        self.globals.add(instr.ycor.name)

        return self.globals
    
    def convert(self, ir):
        # convert each statement from ChironTAC to ChironSSA
        for instr, tgt in ir:
            if isinstance(instr, ChironTAC.AssignmentCommand):
                lvar = ChironSSA.Var(instr.lvar.name)
                rvar1 = ChironSSA.Var(instr.rvar1.name) if isinstance(instr.rvar1, ChironTAC.Var) else ChironSSA.Num(instr.rvar1.value) if isinstance(instr.rvar1, ChironTAC.Num) else ChironSSA.Unused()
                rvar2 = ChironSSA.Var(instr.rvar2.name) if isinstance(instr.rvar2, ChironTAC.Var) else ChironSSA.Num(instr.rvar2.value) if isinstance(instr.rvar2, ChironTAC.Num) else ChironSSA.Unused()
                ir[ir.index((instr, tgt))] = (ChironSSA.AssignmentCommand(lvar, rvar1, rvar2, instr.op), tgt)

            elif isinstance(instr, ChironTAC.AssertCommand):
                cond = ChironSSA.Var(instr.cond.name) if isinstance(instr.cond, ChironTAC.Var) else ChironSSA.BoolTrue() if isinstance(instr.cond, ChironTAC.BoolTrue) else ChironSSA.BoolFalse()
                ir[ir.index((instr, tgt))] = (ChironSSA.AssertCommand(cond), tgt)

            elif isinstance(instr, ChironTAC.ConditionCommand):
                cond = ChironSSA.Var(instr.cond.name) if isinstance(instr.cond, ChironTAC.Var) else ChironSSA.BoolTrue() if isinstance(instr.cond, ChironTAC.BoolTrue) else ChironSSA.BoolFalse()
                ir[ir.index((instr, tgt))] = (ChironSSA.ConditionCommand(cond), tgt)

            elif isinstance(instr, ChironTAC.MoveCommand):
                var = ChironSSA.Var(instr.var.name) if isinstance(instr.var, ChironTAC.Var) else ChironSSA.Num(instr.var.value)
                ir[ir.index((instr, tgt))] = (ChironSSA.MoveCommand(instr.direction, var), tgt)

            elif isinstance(instr, ChironTAC.GotoCommand):
                xcor = ChironSSA.Var(instr.xcor.name) if isinstance(instr.xcor, ChironTAC.Var) else ChironSSA.Num(instr.xcor.value)
                ycor = ChironSSA.Var(instr.ycor.name) if isinstance(instr.ycor, ChironTAC.Var) else ChironSSA.Num(instr.ycor.value)
                ir[ir.index((instr, tgt))] = (ChironSSA.GotoCommand(xcor, ycor), tgt)

            elif isinstance(instr, ChironTAC.SinCommand):
                lvar = ChironSSA.Var(instr.lvar.name)
                rvar = ChironSSA.Var(instr.rvar.name) if isinstance(instr.rvar, ChironTAC.Var) else ChironSSA.Num(instr.rvar.value)
                ir[ir.index((instr, tgt))] = (ChironSSA.SinCommand(lvar, rvar), tgt)

            elif isinstance(instr, ChironTAC.CosCommand):
                lvar = ChironSSA.Var(instr.lvar.name)
                rvar = ChironSSA.Var(instr.rvar.name) if isinstance(instr.rvar, ChironTAC.Var) else ChironSSA.Num(instr.rvar.value)
                ir[ir.index((instr, tgt))] = (ChironSSA.CosCommand(lvar, rvar), tgt)

            elif isinstance(instr, ChironTAC.DegToRadCommand):
                lvar = ChironSSA.Var(instr.lvar.name)
                rvar = ChironSSA.Var(instr.rvar.name) if isinstance(instr.rvar, ChironTAC.Var) else ChironSSA.Num(instr.rvar.value)
                ir[ir.index((instr, tgt))] = (ChironSSA.DegToRadCommand(lvar, rvar), tgt)

            elif isinstance(instr, ChironTAC.PenCommand):
                ir[ir.index((instr, tgt))] = (ChironSSA.PenCommand(instr.status), tgt)

            elif isinstance(instr, ChironTAC.PauseCommand):
                ir[ir.index((instr, tgt))] = (ChironSSA.PauseCommand(), tgt)

            elif isinstance(instr, ChironTAC.NoOpCommand):
                ir[ir.index((instr, tgt))] = (ChironSSA.NoOpCommand(), tgt)

