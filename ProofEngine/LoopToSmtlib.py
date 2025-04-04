import re
import networkx as nx

from ChironCore.Infix_To_Prefix import Infix_To_Prefix

def extract_variable(statement):
    """Extracts the assigned variable and its value from an assignment statement."""
    match = re.match(r"\s*([:\w]+)\s*=\s*(.+)", statement)
    return (match.group(1).lstrip(':'), match.group(2)) if match else (None, None)

def if_else_smtlib(condition, if_stat, else_stat):
    """Generates SMT-LIB for if-else blocks using the ite (if-then-else) construct."""
    if len(if_stat) != 1 or len(else_stat) != 1:
        raise ValueError("Invalid if-else block: Must have exactly 1 statement in each branch.")

    if_var, if_value = extract_variable(if_stat[0].__str__())
    else_var, else_value = extract_variable(else_stat[0].__str__())

    if if_var != else_var:
        raise ValueError(f"Mismatch: IF assigns to {if_var}, ELSE assigns to {else_var}. Expected same variable.")

    cond = Infix_To_Prefix(condition)
    if_value = Infix_To_Prefix(if_value)
    else_value = Infix_To_Prefix(else_value)
    return f"(= {if_var} (ite {cond} {if_value} {else_value}))"

def assign_smtlib(statement):
    return f"{Infix_To_Prefix(statement, replace_eq=True)}"

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
    return before_loop, loop_body, after_loop

import re

def get_vars(expression):
    """Extracts all variables (starting with ':') from an expression."""
    return set(re.findall(r":[\w_]+", expression))

def extract_lhs_rhs(statement):
    """Extracts the left-hand side (LHS) and right-hand side (RHS) from an assignment statement."""
    match = re.match(r"\s*([:\w_]+)\s*=\s*(.+)", statement)
    return (match.group(1), match.group(2)) if match else (None, None)

def classify_vars(statements):
    """Classifies variables into internal and external variables, including if-else conditions."""
    assigned_vars = set()  # Track variables that have been assigned
    external_vars = set()  # Variables used before assignment
    internal_vars = set()  # Variables assigned and used within the loop

    for entry in statements:
        if entry[0] == "assign":
            _, statement = entry
            lhs, rhs = extract_lhs_rhs(statement)

            if lhs:
                rhs_vars = get_vars(rhs)  # Extract variables from RHS
                
                # If a variable is used before assignment, mark it as external
                external_vars.update(rhs_vars - assigned_vars)
                
                # Mark the assigned variable
                assigned_vars.add(lhs)

        elif entry[0] == "if-else":
            _, condition, if_statements, else_statements = entry

            # Condition variables are always "used"
            external_vars.update(get_vars(condition) - assigned_vars)

            # Process if-block
            for statement in if_statements:
                lhs, rhs = extract_lhs_rhs(statement)
                if lhs:
                    rhs_vars = get_vars(rhs)
                    external_vars.update(rhs_vars - assigned_vars)  # RHS variables are used
                    assigned_vars.add(lhs)  # LHS variable is assigned

            # Process else-block
            for statement in else_statements:
                lhs, rhs = extract_lhs_rhs(statement)
                if lhs:
                    rhs_vars = get_vars(rhs)
                    external_vars.update(rhs_vars - assigned_vars)  # RHS variables are used
                    assigned_vars.add(lhs)  # LHS variable is assigned

    # Internal vars = assigned vars that were never external
    internal_vars = assigned_vars - external_vars

    return list(internal_vars), list(external_vars)


def rename_vars(statements, vars_to_modify):
    """Renames variables in the statements: used variables → _in, assigned variables → _out"""
    updated_statements = []

    for entry in statements:
        if entry[0] == "assign":
            _, statement = entry
            lhs, rhs = extract_lhs_rhs(statement)

            if lhs:
                # Modify assigned variable (LHS)
                if lhs in vars_to_modify:
                    lhs = f"{lhs}_out"

                # Modify used variables (RHS)
                for var in get_vars(rhs):
                    if var in vars_to_modify:
                        rhs = rhs.replace(var, f"{var}_in")

                updated_statements.append(('assign', f"{lhs} = {rhs}"))

        elif entry[0] == "if-else":
            _, condition, if_statements, else_statements = entry

            # Modify condition variables
            for var in get_vars(condition):
                if var in vars_to_modify:
                    condition = condition.replace(var, f"{var}_in")

            # Process if-block
            new_if_statements = []
            for statement in if_statements:
                lhs, rhs = extract_lhs_rhs(statement)
                if lhs:
                    if lhs in vars_to_modify:
                        lhs = f"{lhs}_out"
                    for var in get_vars(rhs):
                        if var in vars_to_modify:
                            rhs = rhs.replace(var, f"{var}_in")
                    new_if_statements.append(f"{lhs} = {rhs}")

            # Process else-block
            new_else_statements = []
            for statement in else_statements:
                lhs, rhs = extract_lhs_rhs(statement)
                if lhs:
                    if lhs in vars_to_modify:
                        lhs = f"{lhs}_out"
                    for var in get_vars(rhs):
                        if var in vars_to_modify:
                            rhs = rhs.replace(var, f"{var}_in")
                    new_else_statements.append(f"{lhs} = {rhs}")

            updated_statements.append(('if-else', condition, new_if_statements, new_else_statements))

    return updated_statements

def replace_smtlib_variables(smtlib_stmt: str, variables: list, s: str) -> str:
    """
    Replaces each instance of the given variables in the SMT-LIB statement with (variable+s).
    
    :param smtlib_stmt: The input SMT-LIB statement as a string.
    :param variables: A list of variable names to be replaced.
    :param s: The string to append to each variable.
    :return: The modified SMT-LIB statement.
    """
    
    def replacement(match):
        var_name = match.group(0)
        return f'{var_name}{s}'
    
    # Use regex word boundaries to ensure whole variable replacement
    pattern = r'\b(' + '|'.join(map(re.escape, variables)) + r')\b'
    modified_stmt = re.sub(pattern, replacement, smtlib_stmt)
    
    return modified_stmt

def LoopToSmtlib(cfg):
    back_edges = find_back_edges(cfg)
    if len(back_edges) == 0:
        return None

    # Find the START node in the CFG
    start_node = next((node for node in cfg if node.name == "START"), None)
    if not start_node:
        raise ValueError("START node not found in the CFG")
    before_loop, loop_body, after_loop = validate_and_partition_cfg(cfg, start_node)

    # **Process If-Else Blocks in Each Section**
    before_loop = process_if_else_blocks(before_loop, cfg)
    # loop_body_head = [loop_body[0]]
    # loop_body_head = [str(instr[0]) for instr in loop_body_head[0].instrlist]
    # loop_body_head = [('assign', loop_body_head[0])]
    loop_body_without_head = loop_body[1:-2]
    loop_body = process_if_else_blocks(loop_body_without_head, cfg)
    # loop_body = loop_body_head + loop_body_without_head
    after_loop = process_if_else_blocks(after_loop, cfg)

    vars = classify_vars(loop_body)[1]
    loop_body = rename_vars(loop_body, vars)
    
    # Convert to SMT-LIB in order
    def sectionTosmtlib(section):
        smtlib_code = []
        for entry in section:
            smt_statement = None
            if entry[0] == "assign":
                _, statement = entry
                smt_statement = assign_smtlib(statement)
            elif entry[0] == "if-else":
                _, condition, if_statements, else_statements = entry
                smt_statement = if_else_smtlib(condition, if_statements, else_statements)
            
            if(smt_statement):
                smtlib_code.append(smt_statement)
            else:
                print("Invalid Statement: Only assignment and if-else blocks are allowed")
                return
        # code = f"(and "
        code = ""
        for entry in smtlib_code:
            code += entry + " "
        code = code[:-1]
        # code += ")"
        return code
    
    loop_init = before_loop[-1]
    loop_init = rename_vars([loop_init], vars)[0]
    loop_var = re.match(r":([\w_]+)", loop_init[1]).group(1)
    loop_count = re.match(r".*=\s*(.+)", loop_init[1]).group(1)
    loop_count = Infix_To_Prefix(loop_count, True)
    loop_condition = f"(> {loop_var} 0) (<= {loop_var} {loop_count})"
    
    before_loop = before_loop[:-1]
    pre_condition = sectionTosmtlib(before_loop)
    post_condition = sectionTosmtlib(after_loop)
    loop_body_code = sectionTosmtlib(loop_body)

    return pre_condition, loop_body_code, post_condition, loop_condition, vars
    # print(loop_var)
    # print(pre_condition)
    # print(post_condition)
    # print(loop_condition)
    # print(loop_body_code)
    


    