import re
import networkx as nx

from ChironCore.Infix_To_Prefix import Infix_To_Prefix

def validate_cfg_format(cfg):
    """
    Validates the CFG:
    - No loops (graph must be a DAG)
    - Only if-else branching (each decision node has exactly 2 successors)
    - Both branches of if-else must converge at the same node
    """

    # 1. Check for cycles (loops)
    if not nx.is_directed_acyclic_graph(cfg.nxgraph):
        raise ValueError("Invalid CFG: The graph contains a loop (not a DAG). Loops not supported.")

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

    # print("CFG format is valid.")  # If no errors, CFG is valid

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

def assign_smtlib(statement):
    return f"(assert {Infix_To_Prefix(statement, replace_eq=True)})"

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
                dfs(convergence_point)
                return

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
    # print(execution_list)
    
    # Convert to SMT-LIB in order
    smtlib_code = []
    for entry in execution_list:
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
        
    # for line in smtlib_code:
    #     print(line)
    return smtlib_code
