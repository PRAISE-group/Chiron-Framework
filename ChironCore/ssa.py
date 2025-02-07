import ChironAST.ChironAST as ChironAST
import networkx as nx

class SSAConverter:
    def __init__(self, ir, cfg):
        self.ir = ir
        self.cfg = cfg
        self.globals = set()
        self.varBlocks = {}
        self.counter = {}
        self.stack = {}

    def getVariablesExpr(self, expr):
        vars = set()
        if isinstance(expr, ChironAST.Var):
            vars.add(expr.varname)
        elif isinstance(expr, ChironAST.BinArithOp):
            vars = vars.union(self.getVariablesExpr(expr.lexpr))
            vars = vars.union(self.getVariablesExpr(expr.rexpr))
        elif isinstance(expr, ChironAST.UnaryArithOp):
            vars = vars.union(self.getVariablesExpr(expr.expr))
        elif isinstance(expr, ChironAST.BinCondOp):
            vars = vars.union(self.getVariablesExpr(expr.lexpr))
            vars = vars.union(self.getVariablesExpr(expr.rexpr))
        elif isinstance(expr, ChironAST.NOT):
            vars = vars.union(self.getVariablesExpr(expr.expr))

        return vars

    def getVariablesInstr(self, instr):
        vars = set()
        
        if isinstance(instr, ChironAST.AssignmentCommand):
            vars.add(instr.lvar.varname)
            vars = vars.union(self.getVariablesExpr(instr.rexpr))
        elif isinstance(instr, ChironAST.ConditionCommand):
            vars = vars.union(self.getVariablesExpr(instr.cond))
        elif isinstance(instr, ChironAST.AssertCommand):
            vars = vars.union(self.getVariablesExpr(instr.cond))
        elif isinstance(instr, ChironAST.MoveCommand):
            vars = vars.union(self.getVariablesExpr(instr.expr))
        elif isinstance(instr, ChironAST.GotoCommand):
            vars = vars.union(self.getVariablesExpr(instr.xcor))
            vars = vars.union(self.getVariablesExpr(instr.ycor))

        return vars
    
    def getGlobals(self):
        for node in self.cfg.nodes():
            varkill = set()
            for instr, _ in node.instrlist:
                if isinstance(instr, ChironAST.AssignmentCommand):
                    rvars = self.getVariablesExpr(instr.rexpr)
                    for var in rvars:
                        if var not in varkill:
                            self.globals.add(var)

                    varkill.add(instr.lvar.varname)
                    if self.varBlocks.get(instr.lvar.varname) is None:
                        self.varBlocks[instr.lvar.varname] = set()
                    self.varBlocks[instr.lvar.varname].add(node)
                if isinstance(instr, ChironAST.ConditionCommand):
                    rvars = self.getVariablesExpr(instr.cond)
                    for var in rvars:
                        if var not in varkill:
                            self.globals.add(var)
                if isinstance(instr, ChironAST.AssertCommand):
                    rvars = self.getVariablesExpr(instr.cond)
                    for var in rvars:
                        if var not in varkill:
                            self.globals.add(var)
                if isinstance(instr, ChironAST.MoveCommand):
                    rvars = self.getVariablesExpr(instr.expr)
                    for var in rvars:
                        if var not in varkill:
                            self.globals.add(var)
                if isinstance(instr, ChironAST.GotoCommand):
                    rvars = self.getVariablesExpr(instr.xcor)
                    for var in rvars:
                        if var not in varkill:
                            self.globals.add(var)
                    rvars = self.getVariablesExpr(instr.ycor)
                    for var in rvars:
                        if var not in varkill:
                            self.globals.add(var)
    
        return self.globals

    def addPhiFunctions(self):
        for var in self.globals:
            if self.varBlocks.get(var) is None:
                continue

            worklist = self.varBlocks[var]
            while len(worklist) > 0:
                node = worklist.pop()
                
                for block in self.cfg.df[node]:
                    found = False
                    for instr, _ in block.instrlist:
                        if not isinstance(instr, ChironAST.PhiAssignmentCommand):
                            continue
                        if instr.lvar.varname == var:
                            found = True
                            # instr.varlist.append(ChironAST.Var(var))
                            break

                    if not found:
                        block.prepend((ChironAST.PhiAssignmentCommand(ChironAST.Var(var), []), 1))
                        worklist.add(block)

    def renameVariables(self):
        for var in self.globals:
            self.counter[var] = 0
            self.stack[var] = []
        for node in self.cfg.nodes():
            if node.name == "START":
                self.rename(node)

    def newName(self, var):
        var = var.split("#")[0]
        self.stack[var].append(var + "#" + str(self.counter[var]))
        self.counter[var] += 1
        return self.stack[var][-1]
    
    def renameVar(self, expr, oldvar, newvar):
        if isinstance(expr, ChironAST.Var):
            if expr.varname.split('#')[0] == oldvar:
                return ChironAST.Var(newvar)
            return expr
        if isinstance(expr, ChironAST.BinArithOp):
            return ChironAST.BinArithOp(self.renameVar(expr.lexpr, oldvar, newvar), self.renameVar(expr.rexpr, oldvar, newvar), expr.symbol)
        if isinstance(expr, ChironAST.UnaryArithOp):
            return ChironAST.UnaryArithOp(self.renameVar(expr.expr, oldvar, newvar), expr.symbol)
        if isinstance(expr, ChironAST.BinCondOp):
            return ChironAST.BinCondOp(self.renameVar(expr.lexpr, oldvar, newvar), self.renameVar(expr.rexpr, oldvar, newvar), expr.symbol)
        if isinstance(expr, ChironAST.NOT):
            return ChironAST.NOT(self.renameVar(expr.expr, oldvar, newvar))
        return expr

    def rename(self, block):
        print("Renaming block: ", block.name)
        for instr, _ in block.instrlist:
            if isinstance(instr, ChironAST.PhiAssignmentCommand):
                print("renaming phi function: ", instr, " to ", end="")
                instr.lvar.varname = self.newName(instr.lvar.varname)
                print(instr)
        
        for instr, _ in block.instrlist:
            print("Renaming instruction: ", instr, " to ", end="")
            if isinstance(instr, ChironAST.AssignmentCommand):
                rvars = self.getVariablesExpr(instr.rexpr)
                for var in rvars:
                    var = var.split("#")[0]
                    if var in self.globals and len(self.stack[var]) > 0:
                        instr.rexpr = self.renameVar(instr.rexpr, var, self.stack[var][-1])
                instr.lvar.varname = self.newName(instr.lvar.varname)
            if isinstance(instr, ChironAST.ConditionCommand):
                rvars = self.getVariablesExpr(instr.cond)
                for var in rvars:
                    var = var.split("#")[0]
                    if var in self.globals and len(self.stack[var]) > 0:
                        instr.cond = self.renameVar(instr.cond, var, self.stack[var][-1])
            if isinstance(instr, ChironAST.AssertCommand):
                rvars = self.getVariablesExpr(instr.cond)
                for var in rvars:
                    var = var.split("#")[0]
                    if var in self.globals and len(self.stack[var]) > 0:
                        instr.cond = self.renameVar(instr.cond, var, self.stack[var][-1])
            if isinstance(instr, ChironAST.MoveCommand):
                rvars = self.getVariablesExpr(instr.expr)
                for var in rvars:
                    var = var.split("#")[0]
                    if var in self.globals and len(self.stack[var]) > 0:
                        instr.expr = self.renameVar(instr.expr, var, self.stack[var][-1])
            if isinstance(instr, ChironAST.GotoCommand):
                rvars = self.getVariablesExpr(instr.xcor)
                for var in rvars:
                    var = var.split("#")[0]
                    if var in self.globals and len(self.stack[var]) > 0:
                        instr.xcor = self.renameVar(instr.xcor, var, self.stack[var][-1])
                rvars = self.getVariablesExpr(instr.ycor)
                for var in rvars:
                    var = var.split("#")[0]
                    if var in self.globals and len(self.stack[var]) > 0:
                        instr.ycor = self.renameVar(instr.ycor, var, self.stack[var][-1])

            print(instr)

        for succ in self.cfg.successors(block):
            print("Filing phi functions for block: ", succ.name)
            for instr, _ in succ.instrlist:
                if not isinstance(instr, ChironAST.PhiAssignmentCommand):
                    continue
                var = instr.lvar.varname
                var = var.split("#")[0]
                if len(self.stack[var]) == 0:
                    continue
                
                instr.varlist.append(ChironAST.Var(self.stack[var][-1]))

        for succ in self.cfg.successors(block):
            # check if succ is next in dominator tree
            if self.cfg.idom[succ] == block:
                self.rename(succ) 

        for instr, _ in block.instrlist:
            if isinstance(instr, ChironAST.PhiAssignmentCommand) or isinstance(instr, ChironAST.AssignmentCommand):
                var = instr.lvar.varname
                var = var.split("#")[0]
                self.stack[var].pop()

        
    def convert(self):

        self.getGlobals()
        print("Globals: ", self.globals)
        self.addPhiFunctions()
        # dump newly created CFG image
        G = self.cfg.nxgraph
        labels = {}
        for node in self.cfg:
            labels[node] = node.name + "\n" + node.label()

        G = nx.relabel_nodes(G, labels)
        A = nx.nx_agraph.to_agraph(G)
        A.layout('dot')
        A.draw('cfg_before_renaming.png')
        self.renameVariables()


        # dump newly created CFG image
        G = self.cfg.nxgraph
        labels = {}
        for node in self.cfg:
            labels[node] = node.name + "\n" + node.label()

        G = nx.relabel_nodes(G, labels)
        A = nx.nx_agraph.to_agraph(G)
        A.layout('dot')
        A.draw('cfg_after_renaming.png')
        


        

            
