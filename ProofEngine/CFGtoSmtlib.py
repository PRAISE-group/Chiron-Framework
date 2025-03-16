# import sys
# import re
# sys.path.insert(0, "../ChironCore/cfg/")
# sys.path.insert(0, "../ProofEngine/")
# sys.path.insert(0, "../ChironCore/ChironAST/")
# from cfgBuilder import buildCFG
# from IrToSmtlib import IrToSmtlib
# from PrefixConvertor import Infix_To_Prefix
# from ChironAST import ChironAST

# import networkx as nx

# def validate_cfg_format(cfg):
#     """
#     Validates the CFG:
#     - No loops (graph must be a DAG)
#     - Only if-else branching (each decision node has exactly 2 successors)
#     - Both branches of if-else must converge at the same node
#     """

#     # 1. Check for cycles (loops)
#     if not nx.is_directed_acyclic_graph(cfg.nxgraph):
#         raise ValueError("Invalid CFG: The graph contains a loop (not a DAG).")

#     # 2. Check branching rules
#     for node in cfg:
#         successors = list(cfg.successors(node))

#         # Allow linear flow (0 or 1 successor)
#         if len(successors) <= 1:
#             continue

#         # If branching, it must have exactly 2 successors
#         if len(successors) != 2:
#             raise ValueError(f"Invalid CFG format: Node {node.name} has {len(successors)} successors, expected 2.")

#         true_branch, false_branch = successors
#         true_path, false_path = set(), set()
#         convergence_point = None

#         # Explore True branch
#         stack = [true_branch]
#         while stack:
#             n = stack.pop()
#             if n in false_path:  # Convergence detected
#                 convergence_point = n
#                 break
#             if n not in true_path:
#                 true_path.add(n)
#                 stack.extend(cfg.successors(n))

#         # Explore False branch
#         stack = [false_branch]
#         while stack:
#             n = stack.pop()
#             if n in true_path:  # Convergence detected
#                 convergence_point = n
#                 break
#             if n not in false_path:
#                 false_path.add(n)
#                 stack.extend(cfg.successors(n))

#         # If no convergence found, raise an error
#         if convergence_point is None:
#             raise ValueError(f"Invalid CFG: No convergence found for branching at node {node.name}.")

#     print("CFG format is valid.")  # If no errors, CFG is valid

# def find_if_else_blocks(cfg, start_node):
#     visited = set()
#     if_else_blocks = []  # Stores (start_node, convergence_point, condition_expr, if_statements, else_statements)

#     def get_statements_between(start, end):
#         """ Collect all statements between start and end nodes. """
#         collected_statements = []
#         stack = [start]
#         visited_nodes = set()

#         while stack:
#             node = stack.pop()
#             if node == end or node in visited_nodes:
#                 continue
#             visited_nodes.add(node)

#             # Collect statements from this node
#             collected_statements.extend([instr[0] for instr in node.instrlist])

#             # Add successors to explore
#             stack.extend(cfg.successors(node))

#         return collected_statements

#     def dfs(node):
#         if node in visited:
#             return
#         visited.add(node)

#         # Check if this node is a branching point (has exactly two successors)
#         successors = list(cfg.successors(node))
#         if len(successors) == 2:
#             true_branch, false_branch = successors
#             true_path = set()
#             false_path = set()
#             convergence_point = None

#             # Extract condition expression
#             condition_expr = None
#             if node.instrlist:
#                 last_instr = node.instrlist[-1][0]  # Last instruction should be the condition
#                 condition_expr = str(last_instr)  # Convert it to string for printing

#             # Explore True branch
#             stack = [true_branch]
#             while stack:
#                 n = stack.pop()
#                 if n in false_path:  # Found convergence point
#                     convergence_point = n
#                     break
#                 if n not in true_path:
#                     true_path.add(n)
#                     stack.extend(cfg.successors(n))

#             # Explore False branch
#             stack = [false_branch]
#             while stack:
#                 n = stack.pop()
#                 if n in true_path:  # Found convergence point
#                     convergence_point = n
#                     break
#                 if n not in false_path:
#                     false_path.add(n)
#                     stack.extend(cfg.successors(n))

#             if convergence_point:
#                 # Get statements separately for if (true) and else (false) paths
#                 if_statements = get_statements_between(true_branch, convergence_point)
#                 else_statements = get_statements_between(false_branch, convergence_point)
                
#                 if_else_blocks.append((node, convergence_point, condition_expr, if_statements, else_statements))

#         # Continue DFS traversal
#         for successor in successors:
#             dfs(successor)

#     dfs(start_node)
#     return if_else_blocks

# def extract_variable(statement):
#     match = re.match(r"\s*([:\w]+)\s*=\s*(.+)", statement)
#     return (match.group(1).lstrip(':'), match.group(2)) if match else (None, None)


# def if_else_smtlib(condition, if_stat, else_stat):
#     # print(f"{type(condition)}, {type(if_stat)}, {type(else_stat)}")
#     # print(f"{len(if_stat)}, {len(else_stat)}")

#     if(len(if_stat) != 2):
#         print("Only 1 statement must be there in the if path")

#     if(len(else_stat) != 1):
#         print("Only 1 statement must be there in the else path")

#     if_var, if_value = extract_variable(if_stat[0].__str__())
#     else_var, else_value = extract_variable(else_stat[0].__str__())

#     # Ensure both paths assign to the same variable
#     if if_var and else_var and if_var != else_var:
#         raise ValueError(f"Mismatch: IF assigns to {if_var}, ELSE assigns to {else_var}. Expected same variable.")

#     cond = Infix_To_Prefix(condition)
#     if_value = Infix_To_Prefix(if_value)
#     else_value = Infix_To_Prefix(else_value)
#     smtlib_statement = f"(assert (= {if_var} (ite {cond} {if_value} {else_value})))"
#     print(smtlib_statement)

# def CFGtoSmtlib(cfg):
#     # Validate CFG
#     validate_cfg_format(cfg)

#     # Find the START node in the CFG
#     start_node = None
#     for node in cfg:
#         if node.name == "START":
#             start_node = node
#             break

#     if start_node is None:
#         raise ValueError("START node not found in the CFG")

#     # Run the function
#     if_else_results = find_if_else_blocks(cfg, start_node)

#     # Print results
#     print("If-Else Blocks (Start, Convergence, Condition, If Statements, Else Statements):")
#     for start, converge, condition, if_statements, else_statements in if_else_results:
#         print(f"Start: {start.name}, Converge: {converge.name}")
#         print(f"Condition: {condition}")  # Printing the condition expression
#         print("If Path Statements:")
#         for stmt in if_statements:
#             print(f"  - {stmt}")
#         print("Else Path Statements:")
#         for stmt in else_statements:
#             print(f"  - {stmt}")
#         print("-" * 40)
#         if_else_smtlib(condition, if_statements, else_statements)
    

import sys
import re
import networkx as nx

sys.path.insert(0, "../ChironCore/cfg/")
sys.path.insert(0, "../ProofEngine/")
sys.path.insert(0, "../ChironCore/ChironAST/")

from cfgBuilder import buildCFG
from IrToSmtlib import IrToSmtlib
from PrefixConvertor import Infix_To_Prefix
from ChironAST import ChironAST

def validate_cfg_format(cfg):
    """
    Validates the CFG:
    - No loops (graph must be a DAG)
    - Only if-else branching (each decision node has exactly 2 successors)
    - Both branches of if-else must converge at the same node
    """

    # 1. Check for cycles (loops)
    if not nx.is_directed_acyclic_graph(cfg.nxgraph):
        raise ValueError("Invalid CFG: The graph contains a loop (not a DAG).")

    # 2. Check branching rules
    for node in cfg:
        successors = list(cfg.successors(node))

        # Allow linear flow (0 or 1 successor)
        if len(successors) <= 1:
            continue

        # If branching, it must have exactly 2 successors
        if len(successors) != 2:
            raise ValueError(f"Invalid CFG format: Node {node.name} has {len(successors)} successors, expected 2.")

        true_branch, false_branch = successors
        true_path, false_path = set(), set()
        convergence_point = None

        # Explore True branch
        stack = [true_branch]
        while stack:
            n = stack.pop()
            if n in false_path:  # Convergence detected
                convergence_point = n
                break
            if n not in true_path:
                true_path.add(n)
                stack.extend(cfg.successors(n))

        # Explore False branch
        stack = [false_branch]
        while stack:
            n = stack.pop()
            if n in true_path:  # Convergence detected
                convergence_point = n
                break
            if n not in false_path:
                false_path.add(n)
                stack.extend(cfg.successors(n))

        # If no convergence found, raise an error
        if convergence_point is None:
            raise ValueError(f"Invalid CFG: No convergence found for branching at node {node.name}.")

    print("CFG format is valid.")  # If no errors, CFG is valid

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
    return f"(assert (= {if_var} (ite {cond} {if_value} {else_value})))"

def extract_execution_order(cfg, start_node):
    """Extracts all assignments and if-else blocks while preserving execution order."""
    execution_order = []
    visited = set()

    def dfs(node):
        if node in visited:
            return
        visited.add(node)

        successors = list(cfg.successors(node))

        if len(successors) == 2:  # If-Else branching
            true_branch, false_branch = successors
            convergence_point = None
            condition_expr = str(node.instrlist[-1][0]) if node.instrlist else None

            true_path, false_path = set(), set()

            # Explore True branch
            stack = [true_branch]
            while stack:
                n = stack.pop()
                if n in false_path:
                    convergence_point = n
                    break
                if n not in true_path:
                    true_path.add(n)
                    stack.extend(cfg.successors(n))

            # Explore False branch
            stack = [false_branch]
            while stack:
                n = stack.pop()
                if n in true_path:
                    convergence_point = n
                    break
                if n not in false_path:
                    false_path.add(n)
                    stack.extend(cfg.successors(n))

            if convergence_point:
                if_statements = [str(instr[0]) for instr in true_branch.instrlist]
                else_statements = [str(instr[0]) for instr in false_branch.instrlist]
                execution_order.append(("if-else", condition_expr, if_statements, else_statements))

        elif len(successors) <= 1:  # Simple assignment statements
            for instr in node.instrlist:
                execution_order.append(("assign", str(instr[0])))

        for successor in successors:
            dfs(successor)

    dfs(start_node)
    return execution_order

def CFGtoSmtlib(cfg):
    """Generates SMT-LIB from a valid CFG while maintaining execution order."""
    validate_cfg_format(cfg)

    # Find the START node in the CFG
    start_node = next((node for node in cfg if node.name == "START"), None)
    if not start_node:
        raise ValueError("START node not found in the CFG")

    # Get execution order
    execution_list = extract_execution_order(cfg, start_node)

    # Convert to SMT-LIB in order
    smtlib_code = []
    for entry in execution_list:
        if entry[0] == "assign":
            _, statement = entry
            smtlib_code.append(IrToSmtlib([statement]))  # Direct assignment
        elif entry[0] == "if-else":
            _, condition, if_statements, else_statements = entry
            smtlib_code.append(if_else_smtlib(condition, if_statements, else_statements))

    # Print the generated SMT-LIB code
    for line in smtlib_code:
        print(line)
