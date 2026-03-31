"""
Aggressive Dead Code Elimination (ADCE) for Kachua IR.

Starts from essential (side-effecting) instructions and works backward
through SSA def-use chains and control dependence to find all live code.
Everything not marked live is dead.
"""

import sys
sys.path.insert(0, "../ChironCore/")

import ChironAST.ChironAST as AST
from ssa import vars_used_in, get_block_instr


# ---------------------------------------------------------------------------
# Essential instruction classification
# ---------------------------------------------------------------------------

def is_essential(instr):
    """An instruction is essential if it has observable side effects."""
    return isinstance(instr, (
        AST.MoveCommand,
        AST.PenCommand,
        AST.GotoCommand,
        AST.PauseCommand,
    ))


# ---------------------------------------------------------------------------
# Post-dominator computation
# ---------------------------------------------------------------------------

def compute_post_dominators(cfg, rpo):
    """Compute post-dominators using iterative algorithm on reverse CFG."""
    # Find END block
    end_block = None
    for b in cfg.nodes():
        if b.name == "END":
            end_block = b
            break

    if end_block is None:
        return {}, {}

    # Only consider reachable blocks
    all_blocks = set(rpo)
    # Also include END if not in RPO (it might not be)
    all_blocks.add(end_block)

    pdom = {b: set(all_blocks) for b in all_blocks}
    pdom[end_block] = {end_block}

    # Reverse post-order on reverse CFG = post-order on forward CFG
    # Use reversed RPO as approximation (iterate until stable anyway)
    order = list(reversed(rpo))
    if end_block not in order:
        order.insert(0, end_block)

    changed = True
    while changed:
        changed = False
        for b in order:
            if b == end_block:
                continue
            succs = [s for s in cfg.successors(b) if s in all_blocks]
            if not succs:
                continue
            new_pdom = set.intersection(*(pdom[s] for s in succs))
            new_pdom = new_pdom | {b}
            if new_pdom != pdom[b]:
                pdom[b] = new_pdom
                changed = True

    # Extract immediate post-dominators
    # Use RPO index on reverse graph for ordering
    rev_rpo_index = {b: i for i, b in enumerate(order)}

    ipdom = {}
    pdom_children = {b: [] for b in all_blocks}
    for b in all_blocks:
        if b == end_block:
            continue
        candidates = pdom[b] - {b}
        if not candidates:
            continue
        # ipdom is the candidate with the largest index in reverse RPO
        # (closest post-dominator)
        ipdom[b] = max(candidates, key=lambda c: rev_rpo_index.get(c, -1))
        pdom_children[ipdom[b]].append(b)

    return ipdom, pdom_children


def compute_control_dependence(cfg, rpo, ipdom):
    """Compute control dependence using post-dominance frontiers.

    Block B is control-dependent on block A if:
    - A has a successor S such that B post-dominates S
    - B does NOT strictly post-dominate A
    This is equivalent to the post-dominance frontier.
    """
    all_blocks = set(rpo)
    # Include END block
    for b in cfg.nodes():
        if b.name == "END":
            all_blocks.add(b)
            break

    pdf = {b: set() for b in all_blocks}

    for b in all_blocks:
        preds = [p for p in cfg.predecessors(b) if p in all_blocks]
        if len(preds) < 2:
            continue
        for p in preds:
            runner = p
            while runner is not None and runner != ipdom.get(b):
                pdf[runner].add(b)
                runner = ipdom.get(runner)

    # Invert: for each block b, which blocks is b control-dependent on?
    ctrl_dep = {b: set() for b in all_blocks}
    for a, frontier in pdf.items():
        for b in frontier:
            ctrl_dep[b].add(a)

    return ctrl_dep


# ---------------------------------------------------------------------------
# ADCE
# ---------------------------------------------------------------------------

def run_adce(cfg, ssa_info, executable_blocks):
    """Run Aggressive Dead Code Elimination.

    Returns set of live blocks (blocks whose instructions should be kept).
    """
    live_blocks = set()
    worklist = []

    def mark_live(b):
        if b not in live_blocks and b in executable_blocks:
            live_blocks.add(b)
            worklist.append(b)

    # Compute post-dominators and control dependence
    ipdom, _ = compute_post_dominators(cfg, ssa_info.rpo)
    ctrl_dep = compute_control_dependence(cfg, ssa_info.rpo, ipdom)

    # Step 1: Seed with essential instructions
    for block in executable_blocks:
        instr = get_block_instr(block)
        if instr is not None and is_essential(instr):
            mark_live(block)

    # Step 2: Propagate liveness backward
    visited_phis = set()  # avoid infinite loops in phi tracing

    def trace_phi_operands(var, ver):
        """Recursively trace phi operands back to their definitions."""
        key = (var, ver)
        if key in visited_phis:
            return
        visited_phis.add(key)

        def_block = ssa_info.def_site.get(key)
        if def_block is None:
            return
        if var in ssa_info.phi_nodes.get(def_block, {}):
            # This version is defined by a phi — trace operands
            mark_live(def_block)
            for pred_block, pred_ver in ssa_info.phi_nodes[def_block][var].items():
                if pred_ver >= 0:
                    pred_def = ssa_info.def_site.get((var, pred_ver))
                    if pred_def is not None:
                        mark_live(pred_def)
                    trace_phi_operands(var, pred_ver)

    while worklist:
        block = worklist.pop()
        instr = get_block_instr(block)

        # Data dependence: mark definitions of used variables as live
        if instr is not None:
            for var in vars_used_in(instr):
                ver = ssa_info.var_version_use.get((var, block))
                if ver is not None and ver >= 0:
                    def_block = ssa_info.def_site.get((var, ver))
                    if def_block is not None:
                        mark_live(def_block)
                    # If defined by phi, trace operands
                    trace_phi_operands(var, ver)

        # Also trace phi operands if this block has phis that are live
        for var in ssa_info.phi_nodes.get(block, {}):
            phi_ver = ssa_info.var_version_def.get((var, block))
            if phi_ver is not None:
                for pred_block, pred_ver in ssa_info.phi_nodes[block][var].items():
                    if pred_ver >= 0:
                        pred_def = ssa_info.def_site.get((var, pred_ver))
                        if pred_def is not None:
                            mark_live(pred_def)
                        trace_phi_operands(var, pred_ver)

        # Control dependence: mark branches that control this block
        for cd_block in ctrl_dep.get(block, set()):
            mark_live(cd_block)

    return live_blocks


def dump_adce(live_blocks, executable_blocks, ssa_info):
    """Print ADCE results for debugging."""
    print("\n===== ADCE RESULTS =====")
    for block in ssa_info.rpo:
        if block.name in ("START", "END"):
            continue
        instr = get_block_instr(block)
        if instr is None:
            continue
        status = "LIVE" if block in live_blocks else "DEAD"
        reachable = "reachable" if block in executable_blocks else "unreachable"
        print(f"  [{block.name}] {instr} — {status} ({reachable})")
    print("========================\n")
