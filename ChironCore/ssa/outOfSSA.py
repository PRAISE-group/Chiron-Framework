#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Out-of-SSA Transformation for ChironLang"""

from typing import List, Tuple, Dict, Set
from ChironAST.ChironAST import (
    Instruction, PhiCommand, AssignmentCommand, ConditionCommand, BoolExpr, BoolFalse, Var, Num
)
from irhandler import IRHandler
from cfg.cfgBuilder import buildCFG, dumpCFG
from cfg.ChironCFG import ChironCFG, BasicBlock
from ssa.latticeValue import LatticeValue


class OutOfSSATransformer:
    """Class to handle all functions for Out of SSA Transformation."""
    
    def __init__(self, ir: List, cfg: ChironCFG, sscp_results: Dict[str, LatticeValue] = None):
        """Initialize the Out-of-SSA transformer."""
        self.ir = ir
        self.cfg = cfg
        self.ir_handler = IRHandler()
        self.split_blocks = {}  # Maps critical edges to new blocks
        self.preds_list = {}  # Dict: v, list of predecessors in original order
        self.sscp_results = sscp_results
        self.initial_node_order = self.compute_initial_node_order()

    def compute_initial_node_order(self):
        """Compute the initial order of nodes based on instruction indices."""
        initial_node_order = []
        for node in self.cfg.nodes():
            if not node.instrlist:
                continue
            initial_node_order.append((node.instrlist[0][1], node))
        
        initial_node_order.sort(key=lambda x: x[0])
        return [node[1] for node in initial_node_order]

    def find_all_preds_list(self):
        """Convert predecessors set in nx.graph to a list to retain indices."""
        for bb in list(self.cfg.nodes()):
            self.preds_list[bb] = list(self.cfg.predecessors(bb))
    
    def find_critical_edges(self) -> List[Tuple[BasicBlock, BasicBlock]]:
        """Identify all critical edges in the CFG."""
        critical_edges = []
        for u, v in self.cfg.edges():
            if self.cfg.out_degree(u) > 1 and self.cfg.in_degree(v) > 1:
                critical_edges.append((u, v))
        return critical_edges

    def split_critical_edge(self, u: BasicBlock, v: BasicBlock):
        """Insert a new block between u and v to split a critical edge."""
        # Create new block
        new_id = len(self.cfg.nodes()) + 1
        new_block = BasicBlock(new_id)
        self.cfg.add_node(new_block)
        false_cmd = ConditionCommand(BoolFalse())
        new_block.instrlist.append((false_cmd, 0))
        
        # Redirect u -> v to u -> new_block -> v
        old_idx_u = self.preds_list[v].index(u)

        old_label = self.cfg.get_edge_label(u, v)
        self.cfg.nxgraph.remove_edge(u, v)
        self.cfg.add_edge(u, new_block, label=old_label)
        self.cfg.add_edge(new_block, v, label='Cond_False')
        self.preds_list[v][old_idx_u] = new_block
        self.split_blocks[(u, v)] = new_block
        
        # This case will never likely never be it. Still needs to be formally argued.
        if old_label == 'Cond_True':
            v_index = self.initial_node_order.index(v)
            self.initial_node_order.insert(v_index, new_block)

    def split_all_critical_edges(self):
        """Split all critical edges in the CFG."""
        critical_edges = self.find_critical_edges()
        for u, v in critical_edges:
            self.split_critical_edge(u, v)

    def replace_phi_with_copies(self):
        """Replace φ-functions with copy instructions in predecessors."""
        for bb in list(self.cfg.nodes()):
            phis = []
            other_instrs = []
            
            # Separate phi instructions from other instructions
            for instr, offset in bb.instrlist:
                if isinstance(instr, PhiCommand):
                    phis.append((instr, offset))
                else:
                    other_instrs.append((instr, offset))
            
            # Remove φ-functions from current block
            bb.instrlist = other_instrs
            
            # Process each φ-function
            for phi, offset in phis:
                var = phi.var
                operands = phi.operands
                predecessors = self.preds_list[bb]
                
                for idx, pred in enumerate(predecessors):
                    operand = operands[idx]
                    
                    # Handle special case for operands ending with "_0"
                    if operand.endswith("_0"):
                        temp_assignment = AssignmentCommand(Var(var), Num(0))
                        self._insert_assignment_to_predecessor(pred, temp_assignment)
                    else:
                        # Create assignment: var = operand
                        lhs_assgn = self._get_operand_value(operand)
                        assignment = AssignmentCommand(Var(var), lhs_assgn)
                        self._insert_assignment_to_predecessor(pred, assignment)
    
    def _get_operand_value(self, operand):
        """Get the appropriate value for an operand based on SSCP results."""
        if (self.sscp_results is not None and 
            operand in self.sscp_results and 
            self.sscp_results[operand].is_constant()):
            return Num(self.sscp_results[operand].get_constant())
        return Var(operand)
    
    def _insert_assignment_to_predecessor(self, pred, assignment):
        """Insert assignment instruction to a predecessor block."""
        if isinstance(pred.instrlist[-1][0], ConditionCommand):
            pred.instrlist.insert(len(pred.instrlist) - 1, (assignment, 0))
        else:
            pred.instrlist.append((assignment, 0))
        
    def handle_preds_of_end(self):
        """Handle predecessors of 'END' block."""
        for node in self.cfg.nodes():
            if node.name == 'END':
                for pred in self.cfg.predecessors(node):
                    if self.cfg.get_edge_label(pred, node) != 'Cond_False':
                        pred.instrlist.append((ConditionCommand(BoolFalse()), 1))
                break

    def instructions_in_original_order(self):
        """Traverse the CFG and return instructions in the original IR order."""
        idx_in_ir = 0
        
        # Add any missing nodes to initial_node_order
        for node in self.cfg.nodes():
            if node not in self.initial_node_order and node.instrlist:
                self.initial_node_order.append(node)
        
        # Update IR with instructions from all nodes
        for node in self.initial_node_order:
            for i, (instr, _) in enumerate(node.instrlist):
                if idx_in_ir < len(self.ir):
                    self.ir[idx_in_ir] = (instr, 1)
                else:
                    self.ir.append((instr, 1))
                node.instrlist[i] = (node.instrlist[i][0], idx_in_ir)
                idx_in_ir += 1

    def update_jump_offsets(self):
        """Update jump offsets in IR after inserting instructions."""
        for bb in self.cfg.nodes():
            if not bb.instrlist and bb.name != 'END':
                continue
                
            if bb.name == 'END':
                self._update_offsets_for_end_block(bb)
            else:
                self._update_offsets_for_normal_block(bb)
    
    def _update_offsets_for_end_block(self, end_block):
        """Update jump offsets for predecessors of the END block."""
        for pred_block in self.cfg.predecessors(end_block):
            last_instr_idx_pred = pred_block.instrlist[-1][1]
            self.ir[last_instr_idx_pred] = (
                self.ir[last_instr_idx_pred][0], 
                len(self.ir) - last_instr_idx_pred
            )
    
    def _update_offsets_for_normal_block(self, bb):
        """Update jump offsets for predecessors of normal blocks."""
        first_instr_idx_bb = bb.instrlist[0][1]
        for pred_block in self.cfg.predecessors(bb):
            last_instr_idx_pred = pred_block.instrlist[-1][1]
            if self.cfg.get_edge_label(pred_block, bb) == 'Cond_False':
                if last_instr_idx_pred + self.ir[last_instr_idx_pred][1] != first_instr_idx_bb:
                    self.ir[last_instr_idx_pred] = (
                        self.ir[last_instr_idx_pred][0], 
                        first_instr_idx_bb - last_instr_idx_pred
                    )
        
    def transform(self) -> Tuple[List, ChironCFG]:
        """Execute out-of-SSA transformation pipeline."""
        self.find_all_preds_list()
        self.split_all_critical_edges()
        self.replace_phi_with_copies()
        self.handle_preds_of_end()
        self.instructions_in_original_order()
        self.update_jump_offsets()  # Renamed from Update_Jump_Offsets
        return self.ir, self.cfg


def out_of_ssa(ir, cfg: ChironCFG, sscp_results: Dict[str, LatticeValue]) -> Tuple[List, ChironCFG]:
    """Interface to perform out-of-SSA transformation."""
    transformer = OutOfSSATransformer(ir, cfg, sscp_results)
    transformer.transform()
    dumpCFG(cfg, "cfg4_old_out_of_ssa")
    new_cfg = buildCFG(ir, 'out_of_ssa')
    dumpCFG(new_cfg, 'cfg5_new_out_of_ssa')
    return ir, new_cfg