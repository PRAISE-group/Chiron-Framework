import re
import networkx as nx

from Infix_To_Prefix import Infix_To_Prefix

def find_back_edges(cfg):
    """Identifies back edges in the CFG using depth-first search."""
    back_edges = []
    visited = set()

    def dfs(node, ancestors):
        visited.add(node)

        for succ in cfg.successors(node):  
            if succ in ancestors:  # Found a back edge
                back_edges.append((node, succ))
            elif succ not in visited:
                dfs(succ, ancestors | {succ})

    for node in cfg:
        if node not in visited:
            dfs(node, {node})

    return back_edges


def find_loop_nodes(cfg, head, tail):
    """
    Finds all nodes in a loop (from head to tail) and returns them in execution order.
    Ensures it does not include nodes from the exit path.
    """
    loop_nodes = []
    queue = [head]  # Start from loop header

    # Identify the loop exit branch
    successors = list(cfg.successors(head))
    if len(successors) != 2:
        raise ValueError("Loop header must have exactly two successors.")

    cond_true, cond_false = successors  # Assuming first branch is true (loop), second is false (exit)
    exit_path = cond_false  # Nodes in this path must be ignored

    while queue:
        node = queue.pop(0)  # FIFO for forward traversal

        if node not in loop_nodes:  # Avoid duplicates
            loop_nodes.append(node)

            for succ in cfg.successors(node):  
                # Ensure we do not add nodes from the exit path
                if succ not in loop_nodes and succ != head and succ != exit_path:
                    queue.append(succ)

    # Ensure tail is included at the end
    if tail not in loop_nodes:
        loop_nodes.append(tail)

    return loop_nodes

def process_if_else_blocks(section, cfg):
    """
    Identifies if-else blocks in a given section and groups them as single statements using DFS.
    Ensures execution order is preserved by using lists instead of sets.
    """
    processed_section = []
    visited = set()

    def dfs(node):
        if node in visited:
            return
        visited.add(node)

        successors = list(cfg.successors(node))
        if len(successors) <= 1:  # Simple statement
            if node in section:
                for instr in node.instrlist:
                    processed_section.append(("assign", str(instr[0])))
            for succ in successors:
                if succ in section:    
                    dfs(succ)
            return
            
        if len(successors) != 2:
            raise ValueError(f"Invalid CFG format: Node {node.name} has {len(successors)} successors, expected 2.")
        
        # Detect If-Else Blocks
        true_branch, false_branch = successors
        convergence = None
        if_branch_nodes, else_branch_nodes = [true_branch], [false_branch]
        if_branch = true_branch
        for i in range(2):
            succ = list(cfg.successors(if_branch))
            if len(succ) > 1:
                raise ValueError("Nested if-else not allowed 1.")
            if_branch = succ[0]
            if_branch_nodes.append(if_branch)
        else_branch = false_branch
        for i in range(1):
            succ = list(cfg.successors(else_branch))
            if len(succ) > 1:
                raise ValueError("Nested if-else not allowed 2.")
            else_branch = succ[0]
            else_branch_nodes.append(else_branch)
        

        if if_branch_nodes[-1] != else_branch_nodes[-1]:
            raise ValueError("Invalid if-else branch format. Convergence not found.")
        
        convergence = if_branch_nodes[-1]
        if_branch_nodes = if_branch_nodes[:-1]
        else_branch_nodes = else_branch_nodes[:-1]
        if_branch = [if_branch_nodes[0]]
        else_branch = [else_branch_nodes[0]]
        if_statements = [str(instr[0]) for instr in true_branch.instrlist]
        else_statements = [str(instr[0]) for instr in false_branch.instrlist]
        condition_expr = str(node.instrlist[-1][0]) if node.instrlist else None
        processed_section.append(("if-else", condition_expr, if_statements, else_statements))
        for nx in if_branch_nodes:
            visited.add(nx)
        for nx in else_branch_nodes:
            visited.add(nx)
        dfs(convergence)
        return

    # Start DFS traversal
    for node in section:
        if node not in visited:
            dfs(node)

    return processed_section


def validate_and_partition_cfg(cfg, start_node):
    """Validates that the CFG has at most one loop and partitions it into before-loop, in-loop, and after-loop sections."""
    back_edges = find_back_edges(cfg)

    # Check that there is at most one loop
    if len(back_edges) > 1:
        raise ValueError("More than one loop detected. Only one loop is allowed.")

    loop_header = None
    loop_body = []

    if back_edges:
        # Identify loop header and validate its structure
        loop_tail, loop_header = back_edges[0]  # Single loop detected
        if len(list(cfg.successors(loop_header))) != 2:
            raise ValueError("Loop header must have exactly two successors: one to enter the loop, one to exit.")

        # Find loop body while preserving execution order
        loop_body = find_loop_nodes(cfg, loop_header, loop_tail)

    before_loop = []
    after_loop = []
    visited = set()

    # Perform DFS to separate before-loop and after-loop regions
    def dfs(node, section_list):
        if node in visited or node in loop_body:
            return
        visited.add(node)
        section_list.append(node)  # Maintain execution order
        for successor in cfg.successors(node):
            dfs(successor, section_list)

    # Traverse from start to classify nodes before the loop
    if loop_header:
        dfs(start_node, before_loop)

        # Find the exit path (node outside the loop reachable from loop header)
        exit_nodes = [s for s in cfg.successors(loop_header) if s not in loop_body]
        if(len(exit_nodes) > 1):
            raise ValueError("Loop header must have exactly one exit node.")
        # Traverse from exit nodes to classify nodes after the loop
        for exit_node in exit_nodes:
            dfs(exit_node, after_loop)
    else:
        # No loop detected, treat everything as "before loop"
        dfs(start_node, before_loop)
    # for i in before_loop:
    #     print(i)
    # print(".....")
    # for i in loop_body:
    #     print(i)
    # print(".....")
    # for i in after_loop:
    #     print(i)
    return before_loop, loop_body, after_loop


def LoopToSmtlib(cfg):
    """Generates SMT-LIB from a valid CFG while maintaining execution order."""
    # loops = find_loops(cfg)
    # print(loops)
    # validate_cfg(cfg)

    # Find the START node in the CFG
    start_node = next((node for node in cfg if node.name == "START"), None)
    if not start_node:
        raise ValueError("START node not found in the CFG")
    before_loop, loop_body, after_loop = validate_and_partition_cfg(cfg, start_node)

    # **Process If-Else Blocks in Each Section**
    before_loop = process_if_else_blocks(before_loop, cfg)
    loop_body_head = [loop_body[0]]
    loop_body_head = [str(instr[0]) for instr in loop_body_head[0].instrlist]
    loop_body_without_head = loop_body[1:-1]
    loop_body_without_head = process_if_else_blocks(loop_body_without_head, cfg)
    loop_body = loop_body_head + loop_body_without_head
    after_loop = process_if_else_blocks(after_loop, cfg)

    # print(before_loop)
    # print("...")
    # print(loop_body)
    # print("...")
    # print(after_loop)
    return