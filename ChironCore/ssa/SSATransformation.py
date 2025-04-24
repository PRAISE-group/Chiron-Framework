#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""SSA Transformation Implementation for ChironLang"""

from typing import Dict, Set, List, Tuple
import bisect
import networkx as nx

from ChironAST.ChironAST import (
    Instruction, PhiCommand, Var, AssignmentCommand,
    MoveCommand, GotoCommand, ConditionCommand,
    BinArithOp, BinCondOp, UnaryArithOp, NOT,
    Num, BoolTrue, BoolFalse
)
from cfg.cfgBuilder import dumpCFG, buildCFG
from cfg.ChironCFG import BasicBlock, ChironCFG
from dominanceFrontiers import (
    compute_dominators, compute_dominator_tree, 
    compute_dominance_frontiers
)
from liveVariables import compute_live_vars


def get_used_vars_expr(expr) -> Set[str]:
    """Recursively extract used variables in an expression"""
    if isinstance(expr, Var):
        return {expr.varname}
    elif isinstance(expr, (BinArithOp, BinCondOp)):
        return get_used_vars_expr(expr.lexpr) | get_used_vars_expr(expr.rexpr)
    elif isinstance(expr, (UnaryArithOp, NOT)):
        return get_used_vars_expr(expr.expr)
    elif isinstance(expr, (Num, BoolTrue, BoolFalse)):
        return set()
    return set()

def get_used_vars_instr(instr):
    """Returns the set of used variables in an instruction"""
    used = set()
    if isinstance(instr, AssignmentCommand):
        used = get_used_vars_expr(instr.rexpr)
    elif isinstance(instr, MoveCommand):
        used = get_used_vars_expr(instr.expr)
    elif isinstance(instr, GotoCommand):
        used = get_used_vars_expr(instr.xcor) | get_used_vars_expr(instr.ycor)
    elif isinstance(instr, ConditionCommand):
        used = get_used_vars_expr(instr.cond)
    return used


class SSATransformer:
    """Class for SSA (Static Single Assignment) Transformation"""
    
    def __init__(self, ir, cfg: ChironCFG):
        """Initialize the SSA transformer"""
        self.cfg = cfg
        self.ir = ir
        self.dominators = compute_dominators(cfg)
        self.dom_tree = compute_dominator_tree(self.dominators)
        self.df = compute_dominance_frontiers(cfg, self.dominators)
        self.ue_var, self.var_kill, self.live_in, self.live_out = compute_live_vars(cfg)
        self.globals = self._compute_globals()

    def _compute_globals(self) -> Set[str]:
        """Compute global variables (variables whose liveness span multiple blocks)"""
        return set().union(*self.ue_var.values())

    def insert_phi_in_ir(self, idx_phi):
        """Insert phi-functions in the IR using positions known from CFG"""
        idx_phi.sort(key=lambda pair: pair[0])
        offset = 0

        for index, phi_command in idx_phi:
            insertion_index = index + offset
            self.ir.insert(insertion_index, (phi_command, 1))
            offset += 1

    def synchronize_cfg_ir(self, idx_phi):
        phi_indices = [idx for idx, _ in idx_phi]
        
        # First pass: Update non-phi instructions
        for basic_block in self.cfg.nodes():
            for i, (instruction, idx) in enumerate(basic_block.instrlist):
                if not isinstance(instruction, PhiCommand):
                    offset = bisect.bisect_right(phi_indices, idx)
                    basic_block.instrlist[i] = (instruction, idx + offset)
        
        # Second pass: Update phi instructions
        for basic_block in self.cfg.nodes():
            # Count phi instructions at the beginning of the block
            phi_count = 0
            for instruction, _ in basic_block.instrlist:
                if isinstance(instruction, PhiCommand):
                    phi_count += 1
                else:
                    break
            
            # Update phi instruction indices
            if phi_count > 0:
                first_non_phi_idx = basic_block.instrlist[phi_count][1] if phi_count < len(basic_block.instrlist) else len(self.ir)
                # Update each phi instruction
                for j in range(phi_count):
                    instruction = basic_block.instrlist[j][0]
                    new_idx = first_non_phi_idx - phi_count + j
                    basic_block.instrlist[j] = (instruction, new_idx)
            
    def update_jump_offsets(self):
        """Update Jump Offsets in IR after inserting instructions"""
        for bb in self.cfg.nodes():
            # Skip empty blocks that aren't the END block
            if len(bb.instrlist) == 0 and bb.name != 'END':
                continue
                
            if bb.name == 'END' and len(bb.instrlist) == 0:
                self._update_end_block_offsets(bb)
            else:
                self._update_regular_block_offsets(bb)

    def _update_end_block_offsets(self, end_block):
        """Update jump offsets for the special END block case"""
        for pred_block in self.cfg.predecessors(end_block):
            last_instr_idx_pred = pred_block.instrlist[-1][1]
            self.ir[last_instr_idx_pred] = (
                self.ir[last_instr_idx_pred][0],
                len(self.ir) - last_instr_idx_pred
            )

    def _update_regular_block_offsets(self, block):
        """Update jump offsets for regular blocks"""
        first_instr_idx_bb = block.instrlist[0][1]
        for pred_block in self.cfg.predecessors(block):
            last_instr_idx_pred = pred_block.instrlist[-1][1]
            
            # Update jump offset for conditional false edges
            if self.cfg.get_edge_label(pred_block, block) == 'Cond_False':
                current_target = last_instr_idx_pred + self.ir[last_instr_idx_pred][1]
                if current_target != first_instr_idx_bb:
                    self.ir[last_instr_idx_pred] = (
                        self.ir[last_instr_idx_pred][0],
                        first_instr_idx_bb - last_instr_idx_pred
                    )

    def insert_phi_functions(self):
        """Insert phi-functions for global variables at dominance frontiers"""
        idx_phi = []  # List to keep track of positions to insert in IR
        for var in self.globals:
            worklist = [
                bb for bb in self.cfg.nodes() 
                if any(
                    isinstance(instr, AssignmentCommand) and instr.lvar.varname == var
                    for instr, _ in bb.instrlist
                )
            ]
            
            while worklist:
                bb = worklist.pop(0)
                for df_node in self.df[bb]:
                    if not self._has_phi_for_var(df_node, var):
                        num_preds = len(list(self.cfg.predecessors(df_node)))
                        phi = PhiCommand(var, [""] * num_preds)
                        
                        if len(df_node.instrlist) != 0:
                            idx_in_ir = df_node.instrlist[0][1]
                        else:
                            idx_in_ir = len(self.ir)
                            
                        df_node.instrlist.insert(0, (phi, idx_in_ir))
                        idx_phi.append((idx_in_ir, phi))
                        
                        if df_node not in worklist:
                            worklist.append(df_node)

        # Adding phi-instructions to the actual IR
        self.insert_phi_in_ir(idx_phi)

        # Synchronizing instruction indices in CFG and IR
        self.synchronize_cfg_ir(idx_phi)
        
        # Updating jump offsets in original IR
        self.update_jump_offsets()

        dumpCFG(self.cfg, "cfg1_old_after_phi_insertion")
        return self.cfg

    def _has_phi_for_var(self, bb: BasicBlock, var: str) -> bool:
        """Check if a basic block already has phi-function for a variable"""
        return any(
            isinstance(instr, PhiCommand) and instr.var == var
            for instr, _ in bb.instrlist
        )

    def _rename_in_expr(self, expr, stacks: Dict[str, List[str]]):
        """Recursively rename variables in arithmetic or boolean expressions"""
        if isinstance(expr, Var):
            if expr.varname in stacks and stacks[expr.varname]:
                expr.varname = stacks[expr.varname][-1]
        elif isinstance(expr, (BinArithOp, BinCondOp)):
            self._rename_in_expr(expr.lexpr, stacks)
            self._rename_in_expr(expr.rexpr, stacks)
        elif isinstance(expr, (UnaryArithOp, NOT)):
            self._rename_in_expr(expr.expr, stacks)
    
    def all_vars_in_ir(self):
        all_vars = set()
        #Identify all variables
        for bb in self.cfg.nodes():
            for instr, _ in bb.instrlist:
                # Variables defined
                if isinstance(instr, (AssignmentCommand, PhiCommand)):
                    var_name = instr.lvar.varname if isinstance(instr, AssignmentCommand) else instr.var
                    all_vars.add(var_name)
                
                # Variables used
                if isinstance(instr, (AssignmentCommand, MoveCommand, GotoCommand, ConditionCommand)):
                    used = get_used_vars_instr(instr)
                    all_vars.update(used)
                
                if isinstance(instr, PhiCommand):
                    all_vars.update(op for op in instr.operands if op)
        
        return all_vars

    def rename_variables(self) -> ChironCFG:
        """Perform variable renaming for all instructions"""
        all_vars = self.all_vars_in_ir()
        ssa_to_base = {}  # Tracks SSA names to original bases

        #Initialize renaming 
        counters = {var: 0 for var in all_vars}
        stacks = {var: [] for var in all_vars}
        
        # Initialize stacks with version 0
        for var in all_vars:
            stacks[var].append(f"{var}_0")
            ssa_to_base[var] = var
            counters[var] = 1  # Next version will be _1

        def new_name(var: str) -> str:
            """Generate new SSA name and track base mapping"""
            version = counters[var]
            ssa_name = f"{var}_{version}"
            ssa_to_base[ssa_name] = var  # Track original base
            counters[var] += 1
            stacks[var].append(ssa_name)
            return ssa_name

        def process_block(bb: BasicBlock):
            """Process a single block for variable renaming"""
            defined_vars = dict()

            for idx, (instr, _) in enumerate(bb.instrlist):
                if isinstance(instr, PhiCommand):
                    ssa_name = instr.var
                    base_var = ssa_to_base.get(ssa_name, ssa_name)
                    new_var = new_name(base_var)
                    instr.var = new_var
                    defined_vars[base_var] = defined_vars.get(base_var, 0) + 1
                elif isinstance(instr, AssignmentCommand):
                    original_var = ssa_to_base.get(instr.lvar.varname, instr.lvar.varname)
                    self._rename_in_expr(instr.rexpr, stacks)
                    new_var = new_name(original_var)
                    instr.lvar = Var(new_var)
                    defined_vars[original_var] = defined_vars.get(original_var, 0) + 1
                elif isinstance(instr, MoveCommand):
                    self._rename_in_expr(instr.expr, stacks)
                elif isinstance(instr, GotoCommand):
                    self._rename_in_expr(instr.xcor, stacks)
                    self._rename_in_expr(instr.ycor, stacks)
                elif isinstance(instr, ConditionCommand):
                    self._rename_in_expr(instr.cond, stacks)

            # Update phi operands in successors
            for succ in self.cfg.successors(bb):
                preds = list(self.cfg.predecessors(succ))
                pred_idx = preds.index(bb)
                
                for phi_instr, _ in succ.instrlist:
                    if isinstance(phi_instr, PhiCommand):
                        ssa_name = phi_instr.var
                        base_var = ssa_to_base.get(ssa_name, None)
                        if base_var is not None:
                            phi_instr.operands[pred_idx] = stacks[base_var][-1]

            # Process children in dominator tree
            for child in self.dom_tree.get(bb, []):
                process_block(child)

            # Roll back stacks
            for var in defined_vars.keys():
                while defined_vars[var]:
                    if stacks[var]:
                        stacks[var].pop()
                    defined_vars[var] -= 1

        # Start processing from entry block
        entry_node = next(n for n in self.cfg.nodes() if n.name == 'START')
        process_block(entry_node)
        dumpCFG(self.cfg, "cfg2_old_after_rename")
        return self.cfg


def build_ssa(ir, cfg: ChironCFG) -> ChironCFG:
    """Interface to perform SSA transformation"""
    transformer = SSATransformer(ir, cfg)
    transformer.insert_phi_functions()
    transformer.rename_variables()
    post_ssa_CFG = buildCFG(ir, "post_ssa_control_flow_graph")
    dumpCFG(post_ssa_CFG, "cfg3_new_post_ssa")
    return post_ssa_CFG