#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Dominance Frontiers Computation for ChironLang CFG"""

from typing import Dict, Set, List, Tuple
import networkx as nx
from cfg.cfgBuilder import dumpCFG, buildCFG
from cfg.ChironCFG import BasicBlock, ChironCFG

# Function to compute dominators set for every basic block
def compute_dominators(cfg: ChironCFG) -> Dict[BasicBlock, Set[BasicBlock]]:
    dominators = {}
    entry = cfg.entry
    all_nodes = set(cfg.nodes())
    
    # Initialize dominance sets
    for node in cfg.nodes():
        dominators[node] = all_nodes if node != entry else {entry}
    
    changed = True
    while changed:
        changed = False
        for node in cfg.nodes():
            if node == entry:
                continue   
            preds = list(cfg.predecessors(node))
            if preds:
                # Compute intersection of all predecessors' dominators
                predecessor_doms = [dominators[p] for p in preds]
                new_dom = set.intersection(*predecessor_doms)
            else:
                new_dom = set()

            new_dom.add(node)  # Node always dominates itself
            
            if new_dom != dominators[node]:
                dominators[node] = new_dom
                changed = True
                
    return dominators

# Function to computer dominator tree using the CFG and immediate dominator
def compute_dominator_tree(dominators: Dict) -> Dict[BasicBlock, List[BasicBlock]]:
    dom_tree = {n: [] for n in dominators}

    for node in dominators:
        candidates = dominators[node] - {node}
        if not candidates:
            continue

        # Find the immediate dominator (IDOM)
        idom = None
        for candidate in candidates:
            # Check if this candidate dominates all other candidates
            if all(other in dominators[candidate] for other in candidates if other != candidate):
                idom = candidate
                break

        # Fallback: pick the first candidate (shouldn't happen in valid CFGs)
        if not idom and candidates:
            idom = next(iter(candidates))

        if idom:
            dom_tree[idom].append(node)

    return dom_tree


# Function to compute dominance frontiers
def compute_dominance_frontiers( cfg: ChironCFG, dominators: Dict[BasicBlock, Set[BasicBlock]]) -> Dict[BasicBlock, Set[BasicBlock]]:
    
    frontiers = {n: set() for n in cfg.nodes()}
    dom_tree = compute_dominator_tree(dominators)

    for node in cfg.nodes():
        predecessors = list(cfg.predecessors(node))
        if len(predecessors) >= 2:  # Merge point
            for p in predecessors:
                runner = p
                idom = next((d for d, children in dom_tree.items() if node in children), None)
                while runner != idom and runner is not None:
                    frontiers[runner].add(node)
                    runner = next((d for d, children in dom_tree.items() if runner in children), None) # Move to runner's immediate dominator
    return frontiers