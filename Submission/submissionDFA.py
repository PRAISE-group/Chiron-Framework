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

def optimizeUsingDFA(irHandler):
    '''
        get the cfg out of IR
        each basic block consists of single statement
    '''
    # call worklist and get the in/out values of each basic block
    dfaIntrp = DFA.DataFlowAnalysis(irHandler)
    bbIn, bbOut = dfaIntrp.worklistAlgorithm(irHandler.cfg)


    # NOTE: Implement your code below. Do not change anything above this line.
    # Implement your analysis according to the questions on each basic block



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

def optimize(irHandler, args):
    ir = copy.deepcopy(irHandler.ir)
    
    do_fold = args.opt_constfold or args.opt_all
    do_simp = args.opt_algsimp or args.opt_all
    
    if not (do_fold or do_simp or args.opt_constprop or args.opt_dce):
        # If no specific optimization is selected but we are here, 
        # it might be from -dfa flag.
        return optimizeUsingDFA(irHandler)

    for _ in range(10): # Max 10 iterations
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
