import copy
import math
import sys
from typing import overload

sys.path.insert(0, "../ChironCore/")

import cfg.ChironCFG as cfgK
import cfg.cfgBuilder as cfgB
from lattice import  *
import ChironAST.ChironAST as ChironAST
import dataFlowAnalysis as DFA

from ssa import SSAInfo, vars_in_expr, vars_used_in, get_block_instr, get_block_ir_idx
from sccp import SCCP, ConstVal, OVERDEF, UNDEF
from adce import run_adce, dump_adce


'''
    Class to work with lattice elements.
    Implement these functions as required.
'''
class MovementDomain(Lattice):

    '''Initialize lattice value'''
    def __init__(self, data):
        pass

    '''To display lattice values'''
    def __str__(self):
        pass

    '''To check whether lattice value is bot or not'''
    def isBot(self):
        pass

    '''To check whether lattice value is Top or not'''
    def isTop(self):
        pass

    '''Implement the meet operator'''
    def meet(self, other):
        pass

    '''Implement the join operator'''
    def join(self, other):
        pass

    '''partial order with the other lattice value'''
    def __le__(self, other):
        pass

    '''equality check with other lattice value'''
    def __eq__(self, other):
        pass

    '''
        Add here required lattice operations
    '''
    pass


class MovementTransferFunction(TransferFunction):
    def __init__(self):
        pass

    def transferFunction(self, currBBIN, currBB):
        '''
            Transfer function for basic block 'currBB'
            args: In val for currBB, currBB
            Returns newly calculated values in a form of list

            This is the transfer function you write for DataFlow Analysis.
        '''
        #implement your transfer function here
        outVal = []
        return outVal

class ForwardAnalysis():
    def __init__(self):
        self.transferFunctionInstance = MovementTransferFunction()
        self.type = "MoveTF"

    '''
        This function is to initialize in of the basic block currBB
        Returns a dictionary of {varName -> MovementDomain values}
        isStartNode is a flag for stating whether currBB is start basic block or not
    '''
    def initialize(self, currBB, isStartNode):
        val = {}
        #Your additional initialisation code if any
        return val

    # just a dummy equallity check function for dictionary
    def isEqual(self, dA, dB):
        for i in dA.keys():
            if i not in dB.keys():
                return False
            if dA[i] != dB[i]:
                return False
        return True

    '''
        Define the meet operation.
        Implement this function as required.
        Returns a dictionary of {varName -> MovementDomain values}
    '''
    def meet(self, predList):
        assert isinstance(predList, list)
        meetVal = {}

        return meetVal

def optimizeUsingDFA(irHandler, args):
    '''
        get the cfg out of IR
        each basic block consists of single statement
    '''
    # call worklist and get the in/out values of each basic block
    dfaIntrp = DFA.DataFlowAnalysis(irHandler)
    bbIn, bbOut = dfaIntrp.worklistAlgorithm(irHandler.cfg)


    # NOTE: Implement your code below. Do not change anything above this line.
    # Implement your analysis according to the questions on each basic block

    do_fold = args.opt_constfold or args.opt_all
    do_simp = args.opt_algsimp or args.opt_all

    # TODO: Return the optimized IR in optIR
    optIR = irHandler.ir
    return optIR

# Milestone 1: Constant Folding and Algebraic Simplification

def simplify_expr(expr, do_fold=True, do_simp=True):
    if isinstance(expr, ChironAST.Sum):
        lexpr = simplify_expr(expr.lexpr, do_fold, do_simp)
        rexpr = simplify_expr(expr.rexpr, do_fold, do_simp)
        
        if do_fold and isinstance(lexpr, ChironAST.Num) and isinstance(rexpr, ChironAST.Num):
            return ChironAST.Num(lexpr.val + rexpr.val)
            
        if do_simp:
            if isinstance(lexpr, ChironAST.Num) and lexpr.val == 0:
                return rexpr
            if isinstance(rexpr, ChironAST.Num) and rexpr.val == 0:
                return lexpr
        
        return ChironAST.Sum(lexpr, rexpr)
        
    elif isinstance(expr, ChironAST.Diff):
        lexpr = simplify_expr(expr.lexpr, do_fold, do_simp)
        rexpr = simplify_expr(expr.rexpr, do_fold, do_simp)
        
        if do_fold and isinstance(lexpr, ChironAST.Num) and isinstance(rexpr, ChironAST.Num):
            return ChironAST.Num(lexpr.val - rexpr.val)
            
        if do_simp:
            if isinstance(rexpr, ChironAST.Num) and rexpr.val == 0:
                return lexpr
            if str(lexpr) == str(rexpr): # Basic check for :x - :x
                return ChironAST.Num(0)
                
        return ChironAST.Diff(lexpr, rexpr)
        
    elif isinstance(expr, ChironAST.Mult):
        lexpr = simplify_expr(expr.lexpr, do_fold, do_simp)
        rexpr = simplify_expr(expr.rexpr, do_fold, do_simp)
        
        if do_fold and isinstance(lexpr, ChironAST.Num) and isinstance(rexpr, ChironAST.Num):
            return ChironAST.Num(lexpr.val * rexpr.val)
            
        if do_simp:
            if (isinstance(lexpr, ChironAST.Num) and lexpr.val == 0) or \
               (isinstance(rexpr, ChironAST.Num) and rexpr.val == 0):
                return ChironAST.Num(0)
            if isinstance(lexpr, ChironAST.Num) and lexpr.val == 1:
                return rexpr
            if isinstance(rexpr, ChironAST.Num) and rexpr.val == 1:
                return lexpr
                
        return ChironAST.Mult(lexpr, rexpr)
    
    elif isinstance(expr, ChironAST.Div):
        lexpr = simplify_expr(expr.lexpr, do_fold, do_simp)
        rexpr = simplify_expr(expr.rexpr, do_fold, do_simp)
        
        if do_fold and isinstance(lexpr, ChironAST.Num) and isinstance(rexpr, ChironAST.Num):
            if rexpr.val != 0:
                return ChironAST.Num(lexpr.val // rexpr.val)
        
        if do_simp:
            if isinstance(rexpr, ChironAST.Num) and rexpr.val == 1:
                return lexpr
            if str(lexpr) == str(rexpr):
                return ChironAST.Num(1)

        return ChironAST.Div(lexpr, rexpr)
        
    elif isinstance(expr, ChironAST.UMinus):
        uexpr = simplify_expr(expr.expr, do_fold, do_simp)
        if do_fold and isinstance(uexpr, ChironAST.Num):
            return ChironAST.Num(-uexpr.val)
        return ChironAST.UMinus(uexpr)
    
    elif isinstance(expr, (ChironAST.LT, ChironAST.GT, ChironAST.LTE, ChironAST.GTE, ChironAST.EQ, ChironAST.NEQ, ChironAST.AND, ChironAST.OR)):
        lexpr = simplify_expr(expr.lexpr, do_fold, do_simp)
        rexpr = simplify_expr(expr.rexpr, do_fold, do_simp)
        return type(expr)(lexpr, rexpr)
    
    elif isinstance(expr, ChironAST.NOT):
        uexpr = simplify_expr(expr.expr, do_fold, do_simp)
        return ChironAST.NOT(uexpr)
        
    return expr

def substitute_expr(expr, var_map):
    if isinstance(expr, ChironAST.Var):
        if expr.varname in var_map:
            return ChironAST.Num(var_map[expr.varname])
        return expr
    elif isinstance(expr, (ChironAST.Sum, ChironAST.Diff, ChironAST.Mult, ChironAST.Div)):
        new_l = substitute_expr(expr.lexpr, var_map)
        new_r = substitute_expr(expr.rexpr, var_map)
        return type(expr)(new_l, new_r)
    elif isinstance(expr, ChironAST.UMinus):
        new_e = substitute_expr(expr.expr, var_map)
        return ChironAST.UMinus(new_e)
    elif isinstance(expr, (ChironAST.LT, ChironAST.GT, ChironAST.LTE, ChironAST.GTE,
                           ChironAST.EQ, ChironAST.NEQ, ChironAST.AND, ChironAST.OR)):
        new_l = substitute_expr(expr.lexpr, var_map)
        new_r = substitute_expr(expr.rexpr, var_map)
        return type(expr)(new_l, new_r)
    elif isinstance(expr, ChironAST.NOT):
        new_e = substitute_expr(expr.expr, var_map)
        return ChironAST.NOT(new_e)
    return expr


def apply_sccp(ir, cfg, ssa_info, sccp_result):
    new_ir = list(ir)

    for block in cfg.nodes():
        if not block.instrlist:
            continue
        instr, orig_idx = block.instrlist[0]

        var_map = {}
        for var in vars_used_in(instr):
            ver = ssa_info.var_version_use.get((var, block))
            if ver is not None:
                val = sccp_result.cell.get((var, ver), UNDEF)
                if isinstance(val, ConstVal) and isinstance(val.val, int):
                    var_map[var] = val.val

        if not var_map and not isinstance(instr, ChironAST.ConditionCommand):
            continue

        if isinstance(instr, ChironAST.AssignmentCommand):
            if var_map:
                new_rexpr = substitute_expr(instr.rexpr, var_map)
                new_rexpr = simplify_expr(new_rexpr, True, True)
                new_ir[orig_idx] = (ChironAST.AssignmentCommand(instr.lvar, new_rexpr), ir[orig_idx][1])

        elif isinstance(instr, ChironAST.ConditionCommand):
            cond_val = sccp_result._eval_expr(instr.cond, block)
            if isinstance(cond_val, ConstVal):
                if cond_val.val == True:
                    new_ir[orig_idx] = (ChironAST.ConditionCommand(ChironAST.BoolTrue()), ir[orig_idx][1])
                elif cond_val.val == False:
                    new_ir[orig_idx] = (ChironAST.ConditionCommand(ChironAST.BoolFalse()), ir[orig_idx][1])
            elif var_map:
                new_cond = substitute_expr(instr.cond, var_map)
                new_cond = simplify_expr(new_cond, True, True)
                new_ir[orig_idx] = (ChironAST.ConditionCommand(new_cond), ir[orig_idx][1])

        elif isinstance(instr, ChironAST.MoveCommand):
            if var_map:
                new_expr = substitute_expr(instr.expr, var_map)
                new_expr = simplify_expr(new_expr, True, True)
                new_ir[orig_idx] = (ChironAST.MoveCommand(instr.direction, new_expr), ir[orig_idx][1])

        elif isinstance(instr, ChironAST.GotoCommand):
            if var_map:
                new_x = substitute_expr(instr.xcor, var_map)
                new_y = substitute_expr(instr.ycor, var_map)
                new_x = simplify_expr(new_x, True, True)
                new_y = simplify_expr(new_y, True, True)
                new_ir[orig_idx] = (ChironAST.GotoCommand(new_x, new_y), ir[orig_idx][1])

    return new_ir


def apply_adce(ir, cfg, ssa_info, live_blocks, executable_blocks):
    new_ir = list(ir)

    for block in cfg.nodes():
        if block.name in ("START", "END"):
            continue
        if not block.instrlist:
            continue
        instr, orig_idx = block.instrlist[0]

        if block not in executable_blocks:
            if isinstance(instr, ChironAST.AssignmentCommand):
                if "__rep_counter_" not in str(instr.lvar):
                    new_ir[orig_idx] = (ChironAST.NoOpCommand(), 1)
            continue

        if block not in live_blocks:
            if isinstance(instr, ChironAST.AssignmentCommand):
                if "__rep_counter_" not in str(instr.lvar):
                    new_ir[orig_idx] = (ChironAST.NoOpCommand(), 1)

    return new_ir


def run_m1_passes(ir, do_fold, do_simp):
    """Run milestone 1 local optimizations (const fold + alg simp)."""
    for _ in range(10):
        changed = False
        new_ir = []
        for stmt, tgt in ir:
            new_stmt = stmt
            if isinstance(stmt, ChironAST.AssignmentCommand):
                new_rexpr = simplify_expr(stmt.rexpr, do_fold, do_simp)
                if str(new_rexpr) != str(stmt.rexpr):
                    new_stmt = ChironAST.AssignmentCommand(stmt.lvar, new_rexpr)
                    changed = True
            elif isinstance(stmt, ChironAST.MoveCommand):
                new_expr = simplify_expr(stmt.expr, do_fold, do_simp)
                if str(new_expr) != str(stmt.expr):
                    new_stmt = ChironAST.MoveCommand(stmt.direction, new_expr)
                    changed = True
            elif isinstance(stmt, ChironAST.ConditionCommand):
                new_cond = simplify_expr(stmt.cond, do_fold, do_simp)
                if str(new_cond) != str(stmt.cond):
                    new_stmt = ChironAST.ConditionCommand(new_cond)
                    changed = True
            elif isinstance(stmt, ChironAST.GotoCommand):
                new_xcor = simplify_expr(stmt.xcor, do_fold, do_simp)
                new_ycor = simplify_expr(stmt.ycor, do_fold, do_simp)
                if str(new_xcor) != str(stmt.xcor) or str(new_ycor) != str(stmt.ycor):
                    new_stmt = ChironAST.GotoCommand(new_xcor, new_ycor)
                    changed = True
            new_ir.append((new_stmt, tgt))
        ir = new_ir
        if not changed:
            break
    return ir


def optimize(irHandler, args):
    ir = copy.deepcopy(irHandler.ir)

    do_fold = args.opt_constfold or args.opt_all
    do_simp = args.opt_algsimp or args.opt_all
    do_sccp = args.opt_constprop or args.opt_all
    do_adce = args.opt_dce or args.opt_all

    if not (do_fold or do_simp or do_sccp or do_adce):
        return irHandler.ir

    if do_fold or do_simp:
        ir = run_m1_passes(ir, do_fold, do_simp)

    if do_sccp or do_adce:
        cfg = cfgB.buildCFG(ir, "opt_cfg", isSingle=True)

        ssa_info = SSAInfo(cfg)
        ssa_info.build()

        if do_sccp:
            sccp_result = SCCP(cfg, ssa_info)
            sccp_result.run()

            ir = apply_sccp(ir, cfg, ssa_info, sccp_result)

            if do_fold or do_simp:
                ir = run_m1_passes(ir, True, True)

        if do_adce:
            if do_sccp:
                executable_blocks = sccp_result.executable_blocks
            else:
                cfg = cfgB.buildCFG(ir, "opt_cfg", isSingle=True)
                ssa_info = SSAInfo(cfg)
                ssa_info.build()
                executable_blocks = set(cfg.nodes())

            live_blocks = run_adce(cfg, ssa_info, executable_blocks)

            ir = apply_adce(ir, cfg, ssa_info, live_blocks, executable_blocks)

    return ir
