'''
This file is used to convert the SSA IR to SMT-LIB format.
'''
import z3
from ChironSSA import ChironSSA
from cfg import cfgBuilder

class BMC:
    def __init__(self, cfg):
        self.solver = z3.Solver()
        self.cfg = cfg

        self.bbConditions = {} # bbConditions[bb] = condition for bb
        for bb in self.cfg:
            self.bbConditions[bb] = None

        self.buildConditions()

        self.varConditions = {} # varConditions[var] = condition for var
        for bb in self.cfg.nodes():
            for stmt, _ in bb.instrlist:
                if isinstance(stmt, ChironSSA.PhiCommand):
                    self.varConditions[stmt.lvar.name] = self.bbConditions[bb]
                elif isinstance(stmt, ChironSSA.AssignmentCommand):
                    self.varConditions[stmt.lvar.name] = self.bbConditions[bb]

    def buildConditions(self):
        topological_order = list(self.cfg.get_topological_order())
        start = topological_order[0]
        start.set_condition(z3.BoolVal(True))
        topological_order.pop(0)
        for node in topological_order:
            for pred in self.cfg.predecessors(node):
                instr = pred.instrlist[-1][0]
                current_cond = node.get_condition()
                if isinstance(instr, ChironSSA.ConditionCommand) and type(instr.cond) == ChironSSA.Var:
                    cond = z3.Bool(instr.cond.name)
                    label = self.cfg.get_edge_label(pred, node)
                    if label == 'Cond_True':
                        node.set_condition(z3.Or(current_cond, z3.And(pred.get_condition(), cond)))
                    elif label == 'Cond_False':
                        node.set_condition(z3.Or(current_cond, z3.And(pred.get_condition(), z3.Not(cond))))
                else:
                    node.set_condition(z3.Or(pred.get_condition(), current_cond))
            
            t = z3.Tactic('ctx-simplify').apply(node.get_condition()).as_expr()
            node.set_condition(t)
            self.bbConditions[node] = node.get_condition()

    def convertSSAtoSMT(self):
        for bb in self.cfg.nodes():
            for stmt, _ in bb.instrlist:
                if isinstance(stmt, ChironSSA.PhiCommand):
                    lvar = z3.Int(stmt.lvar.name)
                    rvars = [z3.Int(rvar.name) for rvar in stmt.rvars]
                    
                    rhs_expr = rvars[0]
                    for i in range(1, len(stmt.rvars)):
                        rhs_expr = z3.If(self.varConditions[stmt.rvars[i].name], rvars[i], (rhs_expr))
    
                    self.solver.add(lvar == rhs_expr)
    
                elif isinstance(stmt, ChironSSA.AssignmentCommand):
                    lvar = None
                    rvar1 = ChironSSA.Unused()
                    rvar2 = ChironSSA.Unused()
                    if stmt.op in ["+", "-", "*", "/", "%"]:
                        lvar = z3.Int(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Int(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.Num):
                            rvar1 = z3.IntVal(stmt.rvar1.value)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Int(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.Num):
                            rvar2 = z3.IntVal(stmt.rvar2.value)
                    elif stmt.op in ["<", ">", "<=", ">=", "==", "!="]:
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Int(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.Num):
                            rvar1 = z3.IntVal(stmt.rvar1.value)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Int(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.Num):
                            rvar2 = z3.IntVal(stmt.rvar2.value)
                    elif stmt.op in ["and", "or"]:
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar1, ChironSSA.Var):
                            rvar1 = z3.Bool(stmt.rvar1.name)
                        elif isinstance(stmt.rvar1, ChironSSA.BoolTrue):
                            rvar1 = z3.BoolVal(True)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Bool(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.BoolFalse):
                            rvar2 = z3.BoolVal(False)
                    elif stmt.op == "not":
                        lvar = z3.Bool(stmt.lvar.name)
                        if isinstance(stmt.rvar2, ChironSSA.Var):
                            rvar2 = z3.Bool(stmt.rvar2.name)
                        elif isinstance(stmt.rvar2, ChironSSA.BoolTrue):
                            rvar2 = z3.BoolVal(True)
                        elif isinstance(stmt.rvar2, ChironSSA.BoolFalse):
                            rvar2 = z3.BoolVal(False)
                    elif stmt.op == "":
                        continue
                    else:
                        raise Exception("Unknown SSA instruction")                    
    
                    if stmt.op == "+":
                        self.solver.add(lvar == (rvar1 + rvar2))
                    elif stmt.op == "-":
                        self.solver.add(lvar == (rvar1 - rvar2))
                    elif stmt.op == "*":
                        self.solver.add(lvar == (rvar1 * rvar2))
                    elif stmt.op == "/":
                        self.solver.add(lvar == (rvar1 / rvar2))
                    elif stmt.op == "%":
                        self.solver.add(lvar == (rvar1 % rvar2))
                    elif stmt.op == "<":
                        self.solver.add(lvar == (rvar1 < rvar2))
                    elif stmt.op == ">":
                        self.solver.add(lvar == (rvar1 > rvar2))
                    elif stmt.op == "<=":
                        self.solver.add(lvar == (rvar1 <= rvar2))
                    elif stmt.op == ">=":
                        self.solver.add(lvar == (rvar1 >= rvar2))
                    elif stmt.op == "==":
                        self.solver.add(lvar == (rvar1 == rvar2))
                    elif stmt.op == "!=":
                        self.solver.add(lvar == (rvar1 != rvar2))
                    elif stmt.op == "and":
                        self.solver.add(lvar == z3.And(rvar1, rvar2))
                    elif stmt.op == "or":
                        self.solver.add(lvar == z3.Or(rvar1, rvar2))
                    elif stmt.op == "not":
                        self.solver.add(lvar == z3.Not(rvar2))
    
                elif isinstance(stmt, ChironSSA.AssertCommand):
                    cond = None
                    if isinstance(stmt.cond, ChironSSA.BoolTrue):
                        cond = z3.BoolVal(True)
                    elif isinstance(stmt.cond, ChironSSA.BoolFalse):
                        cond = z3.BoolVal(False)
                    elif isinstance(stmt.cond, ChironSSA.Var):
                        cond = z3.Bool(stmt.cond.name)
                    self.solver.add(z3.Not(cond))

                elif isinstance(stmt, ChironSSA.DegToRadCommand):
                    rvar = None
                    if isinstance(stmt.rvar1, ChironSSA.Var):
                        rvar = z3.Real(stmt.rvar1.name)
                    elif isinstance(stmt.rvar1, ChironSSA.Num):
                        rvar = z3.RealVal(stmt.rvar1.value)
                    lvar = z3.Real(stmt.lvar.name)
                    self.solver.add(lvar == (rvar * 3.141592653589793 / 180))

                # elif isinstance(stmt, ChironSSA.CosCommand):         # Problem: z3.Cos, z3.Sin is not supported
                #     self.solver.add(z3.Real(stmt.lvar.name) == z3.Cos(z3.Real(stmt.rvar1.name)))
                # elif isinstance(stmt, ChironSSA.SinCommand):
                #     self.solver.add(z3.Real(stmt.lvar.name) == z3.Sin(z3.Real(stmt.rvar1.name)))
    
                # elif isinstance(stmt, ChironSSA.MoveCommand):
                # elif isinstance(stmt, ChironSSA.PenCommand):
                # elif isinstance(stmt, ChironSSA.GotoCommand):
                elif isinstance(stmt, ChironSSA.ConditionCommand):
                    pass
                elif isinstance(stmt, ChironSSA.NoOpCommand):
                    pass
                elif isinstance(stmt, ChironSSA.PauseCommand):
                    pass
            # else:
                # raise Exception("Unknown SSA instruction")

    def solve(self, inputVars):
        sat = self.solver.check()
        if sat == z3.sat:
            print("Condition not satisfied! Bug found for the following input:")
            model = self.solver.model()
            for var in model:
                varname = str(var).split("$")[0]
                if varname in inputVars:
                    print(varname + " = " + str(model[var]))

        else:
            print("Condition always holds true!")

