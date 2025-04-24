#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" LiveOUT, VarKill and UEVar Computation for ChironLang CFG Basic Blocsk"""

from typing import Dict, Set, List, Tuple
import networkx as nx
from ChironAST.ChironAST import (
    Var, AssignmentCommand,
    MoveCommand, GotoCommand, ConditionCommand,
    BinArithOp, BinCondOp, UnaryArithOp, NOT,
    Num, BoolTrue, BoolFalse
)
from irhandler import IRHandler
from cfg.cfgBuilder import dumpCFG, buildCFG
from cfg.ChironCFG import BasicBlock, ChironCFG

# Function to recursively extract used variables in an expression
def get_used_vars(expr) -> Set[str]:
    if isinstance(expr, Var):
        return {expr.varname}
    elif isinstance(expr, (BinArithOp, BinCondOp)):
        return get_used_vars(expr.lexpr) | get_used_vars(expr.rexpr)
    elif isinstance(expr, (UnaryArithOp, NOT)):
        return get_used_vars(expr.expr)
    elif isinstance(expr, (Num, BoolTrue, BoolFalse)):
        return set()
    return set()


# Live Variable Analysis
def compute_live_vars(cfg: ChironCFG) -> Tuple[Dict, Dict, Dict, Dict]:
    live_in = {bb: set() for bb in cfg.nodes()}
    live_out = {bb: set() for bb in cfg.nodes()}
    ue_var = {bb: set() for bb in cfg.nodes()}
    var_kill = {bb: set() for bb in cfg.nodes()}

    # Compute UEVar and VarKill
    for bb in cfg.nodes():
        for instr, _ in bb.instrlist:
            used = set()
            defined = set()

            if isinstance(instr, AssignmentCommand):
                defined.add(instr.lvar.varname)
                used.update(get_used_vars(instr.rexpr))
            elif isinstance(instr, MoveCommand):
                used.update(get_used_vars(instr.expr))
            elif isinstance(instr, GotoCommand):
                used.update(get_used_vars(instr.xcor))
                used.update(get_used_vars(instr.ycor))
            elif isinstance(instr, ConditionCommand):
                used.update(get_used_vars(instr.cond))

            for var in used:
                if var not in var_kill[bb]:
                    ue_var[bb].add(var)
            var_kill[bb].update(defined)

    # Second pass: Iterate to fixed point
    changed = True
    while changed:
        changed = False
        for bb in cfg.nodes():
            new_live_out = set().union(*(live_in[s] for s in cfg.successors(bb)))
            new_live_in = ue_var[bb] | (new_live_out - var_kill[bb])
            
            if new_live_in != live_in[bb]:
                live_in[bb] = new_live_in
                live_out[bb] = new_live_out
                changed = True

    return ue_var, var_kill, live_in, live_out