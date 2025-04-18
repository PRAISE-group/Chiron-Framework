from ChironAST import ChironAST
from cfg import ChironCFG
import networkx as nx
import re
import cfg.cfgBuilder as cfgB

"""
This module provides functionality to traverse and process the control flow graph (CFG).
It includes methods for extracting variables, renaming variables, processing basic blocks, and verifying the CFG format for programs with or without loops.
"""

def extract_variables_assign(stmt):
    """
    Extracts variables from an assignment statement.

    Args:
        stmt (str): The assignment statement in the form "lhs = rhs".

    Returns:
        tuple: A tuple containing:
            - rhs_vars (list): Variables found in the right-hand side (RHS) of the statement.
            - rhs_expr (str): The RHS expression as a string.
            - lhs_vars (list): Variables found in the left-hand side (LHS) of the statement.
            - lhs_expr (str): The LHS expression as a string.

    Raises:
        ValueError: If the input statement does not contain an "=" sign, indicating it is not a valid assignment.
    """
    # Remove leading and trailing whitespace from the statement
    stmt = stmt.strip()

    # Check if the statement contains an "=" sign; raise an error if not
    if "=" not in stmt:
        raise ValueError(f"Invalid assignment statement: {stmt}")
    
    # Split the statement into LHS (left-hand side) and RHS (right-hand side) at the "=" sign
    lhs_expr, rhs_expr = stmt.split("=", 1)

    # Remove leading and trailing whitespace from both LHS and RHS
    lhs_expr = lhs_expr.strip()
    rhs_expr = rhs_expr.strip()

    # Use regex to extract variables from the LHS and RHS
    # Variables are identified by the pattern ":<identifier>"
    lhs_vars = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*)', lhs_expr)
    rhs_vars = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*)', rhs_expr)

    # Return the extracted variables and expressions as a tuple
    return rhs_vars, rhs_expr, lhs_vars, lhs_expr

def extract_variables_others(stmt):
    """
    Extracts variables from non-assignment statements.

    Args:
        stmt (str): The statement from which variables need to be extracted.

    Returns:
        list: A list of variables found in the statement.

    Explanation:
        - This function uses a regular expression to identify variables in the statement.
        - Variables are expected to follow the pattern ":<identifier>", where <identifier>
          starts with a letter or underscore and can be followed by alphanumeric characters or underscores.
    """
    # Use regex to find all variables in the statement
    variables = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*)', stmt)
    return variables


def rename_vars(ir):
    """
    Renames variables in the intermediate representation (IR) to ensure uniqueness.

    Args:
        ir (list): The intermediate representation (IR) as a list of statements.
                   Each statement is a tuple where the first element is the statement string
                   and the second element is the type of the statement (e.g., "assign").

    Returns:
        tuple: A tuple containing:
            - rename_map (dict): A mapping of variables to their renamed versions.
            - updated_ir (list): The updated IR with renamed variables.

    Explanation:
        - This function processes each statement in the IR to rename variables for uniqueness.
        - Variables in the right-hand side (RHS) and left-hand side (LHS) are renamed using a counter.
        - The renaming ensures that variables are uniquely identified across the IR.

    Steps:
        1. Extract variables from the RHS and LHS of each statement.
        2. Rename RHS variables using the `rename_map` dictionary.
        3. Rename LHS variables and increment their counters in `rename_map`.
        4. Combine the renamed LHS and RHS into a new statement and add it to the updated IR.
    """
    updated_ir = []  # List to store the updated IR with renamed variables
    rename_map = {}  # Dictionary to map variables to their renamed versions

    for stmt in ir:
        lexpr = ""  # Left-hand side expression
        rexpr = ""  # Right-hand side expression
        rhs_vars = []  # Variables in the RHS
        lhs_vars = []  # Variables in the LHS

        # print(stmt)  # Debugging print for the current statement

        # Process assignment statements
        if stmt[1] == "assign":
            vars = extract_variables_assign(stmt[0])  # Extract variables from the assignment
            rhs_vars = vars[0]  # Variables in the RHS
            rexpr = vars[1]  # RHS expression
            lhs_vars = vars[2]  # Variables in the LHS
            lexpr = vars[3]  # LHS expression
        else:
            # Process non-assignment statements
            vars = extract_variables_others(stmt[0])  # Extract variables from the statement
            # print(vars)  # Debugging print for extracted variables
            rhs_vars = vars  # Variables in the RHS
            rexpr = stmt[0]  # RHS expression
            lhs_vars = []  # No LHS for non-assignment statements
            lexpr = ""  # No LHS expression

        # print(rhs_vars, rexpr, lhs_vars, lexpr)  # Debugging print for extracted variables and expressions

        # Rename RHS variables
        for var in rhs_vars:
            if var not in rename_map:
                rename_map[var] = 0  # Initialize the variable in the rename map
                # raise ValueError(f"Variable '{var}' not initialised before first use!")  # Uncomment for strict checks
            # Replace the variable in the RHS with its renamed version
            rexpr = re.sub(rf'{var}\b', f'{var}_{rename_map[var]}', rexpr)

        # Rename LHS variables
        for var in lhs_vars:
            if var not in rename_map:
                rename_map[var] = 1  # Initialize the variable in the rename map
            else:
                rename_map[var] += 1  # Increment the counter for the variable
            # Replace the variable in the LHS with its renamed version
            lexpr = re.sub(rf'{var}\b', f'{var}_{rename_map[var]}', lexpr)

        # Combine the renamed LHS and RHS into a single statement
        if lexpr != "":
            lexpr += '='  # Add the "=" sign to the LHS
            updated_ir.append([lexpr + rexpr, stmt[1]])  # Add the renamed statement to the updated IR
        else:
            updated_ir.append([rexpr, stmt[1]])  # Add the renamed RHS-only statement to the updated IR

    # print(updated_ir)  # Debugging print for the updated IR
    return rename_map, updated_ir


def process_bb1(node: ChironCFG.BasicBlock):
    """
    Processes a basic block to extract and classify instructions.

    Args:
        node (ChironCFG.BasicBlock): The basic block to process.

    Returns:
        None

    Explanation:
        - This function processes the instructions in a basic block and classifies them into types such as "assign", 
          "condition", "assert", "assume", or "invariant".
        - It also renames special variables (e.g., TURTLEX, TURTLEY) to their internal representations (e.g., __turtleX, __turtleY).
        - Variables are further renamed to include the block ID for uniqueness.
        - The processed instructions are stored back in the `instrlist` of the node.

    Steps:
        1. Iterate through the instructions in the basic block.
        2. Classify each instruction based on its type (e.g., assignment, condition, analysis commands).
        3. Replace special variables with their internal representations.
        4. Append the processed instruction to the new instruction list.
        5. Update the node's `instrlist` with the processed instructions.
    """
    new_instrlist = []  # List to store the processed instructions
    block_id = node.irID  # Block ID for variable renaming

    for entry in node.instrlist:
        stmt = str(entry[0])  # Convert the instruction to a string
        if stmt == "False" or stmt == "True":
            continue  # Skip boolean literals

        type = None  # Initialize the type of the instruction

        # Classify the instruction based on its type
        if isinstance(entry[0], ChironAST.AssignmentCommand):
            type = "assign"
        elif isinstance(entry[0], ChironAST.ConditionCommand):
            type = "condition"
        elif isinstance(entry[0], ChironAST.AnalysisCommand):
            if entry[0].stmt == "assert":
                stmt = stmt.split("assert")[-1].strip()  # Extract the assertion statement
                type = "assert"
            elif entry[0].stmt == "assume":
                stmt = stmt.split("assume")[-1].strip()  # Extract the assumption statement
                type = "assume"
            elif entry[0].stmt == "invariant":
                stmt = stmt.split("invariant")[-1].strip()  # Extract the invariant statement
                type = "invariant"
            else:
                raise ValueError(f"Unknown type of AnalysisCommand: {entry[0].stmt}")
        # else:
        #     raise ValueError(f"Unknown type of instruction: {entry[0]}")

        # Extract variables from the statement
        stmt_vars = re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', stmt)

        # Replace special variables with their internal representations
        for var in stmt_vars:
            if var == "TURTLEX":
                stmt = re.sub(rf':{var}\b', f':__turtleX', stmt)
                var = f"__turtleX"
            if var == "TURTLEY":
                stmt = re.sub(rf':{var}\b', f':__turtleY', stmt)
                var = f"__turtleY"
            if var == "TURTLEANGLE":
                stmt = re.sub(rf':{var}\b', f':__turtleW', stmt)
                var = f"__turtleW"
            if var == "TURTLEPEN":
                stmt = re.sub(rf':{var}\b', f':__turtleZ', stmt)
                var = f"__turtleZ"
            if var == "REPCOUNTER":
                stmt = re.sub(rf':{var}\b', f':__rep_counter_1', stmt)
                var = f"__rep_counter_1"

            # Append the block ID to the variable for uniqueness
            stmt = re.sub(rf':{var}\b', f':{var}_{block_id}', stmt)

        # Append the processed instruction to the new instruction list
        new_instrlist.append([stmt, type])

    # print(f"Block ID: {block_id}")  # Debugging print for the block ID
    # print(f"New Instruction List: {new_instrlist}")  # Debugging print for the new instruction list

    # Update the node's instruction list with the processed instructions
    node.instrlist = new_instrlist
    return

def process_bb2(node, successors):
    """
    Processes a basic block to handle variable renaming across its successors.

    Args:
        node (ChironCFG.BasicBlock): The current basic block being processed.
        successors (list): A list of successor nodes of the current basic block.

    Returns:
        None

    Explanation:
        - This function ensures that variables used in successor nodes are properly renamed
          to maintain consistency and uniqueness across the control flow graph (CFG).
        - It uses the `rename_map` of the current node to determine the latest version of each variable.
        - For each successor node, it identifies variables used without assignment and generates
          new assignment statements to propagate the correct variable values.

    Steps:
        1. Retrieve the `rename_map` of the current node to track variable versions.
        2. Iterate through each successor node.
        3. For each successor, identify variables used without assignment.
        4. Generate new assignment statements to propagate the correct variable values.
        5. Append the new assignment statements to the instruction list of the current node.
        6. Update the `instrlist` of the current node with the modified instruction list.
    """
    new_instrlist = node.instrlist  # Get the instruction list of the current node
    block_id = node.irID  # Get the block ID of the current node

    # Retrieve the rename map for the current node
    rename_map = node_to_rename_map[node]
    primary_var_to_id = {}  # Map to store the latest version of each primary variable

    # Populate the primary variable to ID map from the rename map
    for var, id in rename_map.items():
        primary_var = "_".join(var.split("_")[0:-1])  # Extract the primary variable name
        primary_var_to_id[primary_var] = id

    # Iterate through each successor node
    for succ in successors:
        if succ.irID <= block_id:
            continue  # Skip successors with a lower or equal block ID

        # Process each instruction in the successor's instruction list
        for entry in succ.instrlist:
            stmt = str(entry[0])  # Convert the instruction to a string

            # If the instruction is an assignment, extract variables from the RHS
            if entry[1] == "assign":
                vars = extract_variables_assign(stmt)
                stmt = vars[1]  # Use the RHS expression for further processing

            # Find all variables used in the statement without assignment
            stmt_vars = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*_0)', stmt)
            for var in stmt_vars:
                primary_var = "_".join(var.split("_")[0:-2])  # Extract the primary variable name

                # Generate a new assignment statement to propagate the correct variable value
                if primary_var in primary_var_to_id:
                    new_stmt = f"{primary_var}_{succ.irID}_0 = {primary_var}_{block_id}_{primary_var_to_id[primary_var]}"
                else:
                    new_stmt = f"{primary_var}_{succ.irID}_0 = {primary_var}_{block_id}_0"

                # Create a new entry for the assignment statement
                new_entry = [new_stmt, "assign"]

                # Append the new entry to the instruction list if it doesn't already exist
                if new_entry not in new_instrlist:
                    new_instrlist.append([new_stmt, "assign"])

    # Update the instruction list of the current node
    node.instrlist = new_instrlist
    return

def process_bb3(node):
    """
    Processes a basic block to extract assignment statements and the condition.

    Args:
        node (ChironCFG.BasicBlock): The basic block to process.

    Returns:
        tuple: A tuple containing:
            - new_instrlist (list): A list of assignment statements extracted from the block.
            - condition (str or None): The condition statement if present, otherwise None.

    Explanation:
        - This function iterates through the instructions in the basic block.
        - It separates assignment statements and identifies the condition statement, if any.
        - The extracted assignments are stored in `new_instrlist`, and the condition is stored in `condition`.
    """
    new_instrlist = []  # List to store assignment statements
    condition = None  # Variable to store the condition statement

    # Iterate through the instructions in the block
    for entry in node.instrlist:
        if entry[1] == "assign":
            # Add assignment statements to the list
            new_instrlist.append(entry[0])
        elif entry[1] == "condition":
            # Set the condition statement
            condition = entry[0]

    # Return the extracted assignments and condition
    return new_instrlist, condition

"""
A dictionary that maps block types (e.g., "assume", "assert", "invariant", "loop condition") 
to their corresponding nodes in the control flow graph (CFG).
This is used to identify and access specific blocks in the CFG based on their type.
"""
block_type_to_node = {}

"""
A dictionary that maps nodes in the CFG to their variable rename maps.
Each node's rename map tracks the latest version of variables within that node.
"""
node_to_rename_map = {}

def check_cfg_format_with_loop(cfg: ChironCFG.ChironCFG):
    """
    Verifies the format and structure of a control flow graph (CFG) for programs with loops.

    Args:
        cfg (ChironCFG.ChironCFG): The control flow graph to check.

    Returns:
        None

    Explanation:
        - This function ensures that the CFG contains all required blocks: assume, assert, invariant, and loop condition.
        - It validates the presence of these blocks and ensures their positions and relationships in the CFG are correct.
        - It also checks for duplicate blocks of the same type and raises errors if the CFG format is invalid.

    Steps:
        1. Iterate through all nodes in the CFG to identify and classify blocks (assume, assert, invariant, loop condition).
        2. Ensure that there is exactly one block of each required type.
        3. Validate the positions and relationships of the blocks in the CFG.
        4. Check for unexpected or invalid statements in the blocks.
        5. Ensure that the loop condition and loop end are correctly defined and connected.

    Raises:
        ValueError: If the CFG is missing required blocks, contains duplicate blocks, or has invalid relationships or statements.
    """
    nodes_list = list(cfg.nxgraph.nodes)  # Get the list of nodes in the CFG

    """
    Check if all required blocks are present: assume, assert, invariant, loop condition
    """
    for node in nodes_list:
        instrList = node.instrlist  # Get the instruction list for the current node

        # Classify blocks based on their type
        for entry in instrList:
            if entry[1] == "assume":
                if "assume" in block_type_to_node.keys():
                    raise ValueError(f"More than one assume statement is not allowed")
                else:
                    block_type_to_node["assume"] = node

            elif entry[1] == "assert":
                if "assert" in block_type_to_node.keys():
                    raise ValueError(f"More than one assert statement is not allowed")
                else:
                    block_type_to_node["assert"] = node

            elif entry[1] == "invariant":
                if "invariant" in block_type_to_node.keys():
                    raise ValueError(f"More than one invariant statement is not allowed")
                else:
                    block_type_to_node["invariant"] = node

        # Identify the loop condition block based on its predecessors and successors
        predecessors = list(cfg.predecessors(node))
        successors = list(cfg.successors(node))

        if len(predecessors) == 2 and len(successors) == 2:
            if predecessors[0].irID > node.irID or predecessors[1].irID > node.irID:
                if "loop condition" in block_type_to_node.keys():
                    raise ValueError(f"More than one loop is not allowed")
                else:
                    block_type_to_node["loop condition"] = node

    # Ensure all required blocks are present
    if "assume" not in block_type_to_node.keys():
        raise ValueError("Assume statement is missing")
    if "assert" not in block_type_to_node.keys():
        raise ValueError("Assert statement is missing")
    if "invariant" not in block_type_to_node.keys():
        raise ValueError("Invariant statement is missing")
    if "loop condition" not in block_type_to_node.keys():
        raise ValueError("Loop condition is missing")

    """
    Check if the positions of blocks in the CFG and the format of individual blocks are correct
    """
    assume_node = block_type_to_node["assume"]
    assert_node = block_type_to_node["assert"]
    invariant_node = block_type_to_node["invariant"]
    loop_condition_node = block_type_to_node["loop condition"]

    # Validate the assume block
    if assume_node.irID != 0 or assume_node.instrlist[0][1] != "assume":
        raise ValueError("Assume statement should be the first statement")
    if len(assume_node.instrlist) > 2:
        raise ValueError("Unexpected statement(s) after assume")
    if assume_node not in cfg.predecessors(loop_condition_node):
        raise ValueError("Loop condition should have assume as predecessor")
    if loop_condition_node not in cfg.successors(assume_node):
        raise ValueError("Assume should have loop condition as successor")

    # Validate the invariant block
    if invariant_node not in cfg.successors(loop_condition_node) or invariant_node.instrlist[0][1] != "invariant":
        raise ValueError("Loop body should start with invariant")

    # Validate the assert block
    if assert_node not in cfg.successors(loop_condition_node):
        raise ValueError("Assert should be after the loop body ends")
    if len(assert_node.instrlist) > 1:
        raise ValueError("Unexpected statement(s) after assert")

    # Validate the loop condition block
    if len(loop_condition_node.instrlist) > 1:
        raise ValueError("Unexpected statement(s) after loop condition")
    if "__rep_counter_1_1 > 0" not in loop_condition_node.instrlist[0][0]:
        raise ValueError(f"Invalid Loop condition: {loop_condition_node.instrlist[0][0]}")

    # Identify the loop end block
    for pred in cfg.predecessors(loop_condition_node):
        if pred.irID != 0:
            for entry in pred.instrlist:
                if (f"__rep_counter_1_{pred.irID}" in entry[0]) and (entry[1] == "assign"):
                    block_type_to_node["loop end"] = pred
                    break

    # Ensure the loop end block is present
    if "loop end" not in block_type_to_node.keys():
        raise ValueError("Could not find loop end statement")

    return

def check_cfg_format_without_loop(cfg: ChironCFG.ChironCFG):
    """
    Verifies the format and structure of a control flow graph (CFG) for programs without loops.

    Args:
        cfg (ChironCFG.ChironCFG): The control flow graph to check.

    Returns:
        None

    Explanation:
        - This function ensures that the CFG contains the required blocks: assume and assert.
        - It validates the presence of these blocks and ensures their positions and relationships in the CFG are correct.
        - It also checks for duplicate blocks of the same type and raises errors if the CFG format is invalid.

    Steps:
        1. Iterate through all nodes in the CFG to identify and classify blocks (assume, assert).
        2. Ensure that there is exactly one block of each required type.
        3. Validate the positions and relationships of the blocks in the CFG.
        4. Check for unexpected or invalid statements in the blocks.

    Raises:
        ValueError: If the CFG is missing required blocks, contains duplicate blocks, or has invalid relationships or statements.
    """
    nodes_list = list(cfg.nxgraph.nodes)  # Get the list of nodes in the CFG

    """
    Check if all required blocks are present: assume, assert
    """
    for node in nodes_list:
        instrList = node.instrlist  # Get the instruction list for the current node

        # Classify blocks based on their type
        for entry in instrList:
            if entry[1] == "assume":
                if "assume" in block_type_to_node.keys():
                    raise ValueError(f"More than one assume statement is not allowed")
                else:
                    block_type_to_node["assume"] = node

            elif entry[1] == "assert":
                if "assert" in block_type_to_node.keys():
                    raise ValueError(f"More than one assert statement is not allowed")
                else:
                    block_type_to_node["assert"] = node

    # Ensure all required blocks are present
    if "assume" not in block_type_to_node.keys():
        raise ValueError("Assume statement is missing")
    if "assert" not in block_type_to_node.keys():
        raise ValueError("Assert statement is missing")

    """
    Check if the positions of blocks in the CFG and the format of individual blocks are correct
    """
    assume_node = block_type_to_node["assume"]
    assert_node = block_type_to_node["assert"]

    # Validate the assume block
    if assume_node.irID != 0 or assume_node.instrlist[0][1] != "assume":
        raise ValueError("Assume statement should be the first statement")

    # Validate the assert block
    for succ in cfg.successors(assert_node):
        if succ.irID != float('inf'):
            raise ValueError("Assert should be the last statement")
    if assert_node.instrlist[-1][1] != "assert":
        raise ValueError("Assert statement should be the last statement")

    return

def process_and_rename_nodes(sorted_nodes):
    """
    Processes and renames variables in the instruction lists of nodes in the control flow graph (CFG).

    Args:
        sorted_nodes (list): A list of nodes in the CFG, sorted by their `irID`.

    Returns:
        None

    Explanation:
        - This function iterates through the sorted nodes of the CFG and renames variables in their instruction lists.
        - It skips the "END" node as it does not require processing.
        - For each node, the `rename_vars` function is called to rename variables in the instruction list.
        - The renamed instruction list is then updated in the node, and the rename map for the node is stored in `node_to_rename_map`.
    """
    for node in sorted_nodes:
        if node.name == "END":
            continue  # Skip END node as it does not require processing

        # Rename variables in the instruction list of the current node
        node_to_rename_map[node], new_instrlist = rename_vars(node.instrlist)

        # Update the node's instruction list with the renamed instructions
        node.instrlist = new_instrlist

def extract_and_replace_variables(stmt, block_type, target_block_type):
    """
    Extracts variables from a statement and replaces their block-specific suffixes.

    Args:
        stmt (str): The statement to process.
        block_type (str): The source block type (e.g., "invariant", "loop condition").
        target_block_type (str): The target block type (e.g., "assert").

    Returns:
        str: The updated statement with replaced variables.
    """
    stmt_vars = extract_variables_others(stmt)
    for var in stmt_vars:
        primary_var = "_".join(var.split("_")[0:-1])
        stmt = re.sub(rf'{primary_var}_{block_type_to_node[block_type].irID}\b', 
                      f'{primary_var}_{block_type_to_node[target_block_type].irID}', stmt)
    return stmt

def TraverseCFG(cfg: ChironCFG.ChironCFG, has_loop: bool = True):
    """
    Traverses and processes the control flow graph (CFG) to extract preconditions, postconditions,
    and other relevant information for programs with or without loops.

    Args:
        cfg (ChironCFG.ChironCFG): The control flow graph to process.
        has_loop (bool): Indicates whether the CFG contains a loop.

    Returns:
        tuple: Extracted preconditions, postconditions, and other relevant information.

    Explanation:
        - This function processes the CFG by assigning special IDs to nodes, sorting them, and processing them.
        - For CFGs with loops, it validates the CFG format, extracts loop-related information, and processes nodes.
        - For CFGs without loops, it validates the CFG format and extracts preconditions, postconditions, and code body.
    """
    # Assign special irID values for START and END nodes
    for node in cfg.nxgraph.nodes:
        if node.name == "START":
            node.irID = 0  # Assign 0 to the START node
        elif node.name == "END":
            node.irID = float('inf')  # Assign infinity to the END node

    # Sort nodes by irID in ascending order
    sorted_nodes = sorted(cfg.nxgraph.nodes, key=lambda node: node.irID)

    # Process nodes in sorted order
    for node in sorted_nodes:
        if node.name == "END":
            continue  # Skip processing for the END node
        process_bb1(node)  # Process the basic block

    if has_loop:
        # Check CFG format for loops
        check_cfg_format_with_loop(cfg)

        # Extract and replace variables for invariant and loop condition
        stmt1 = block_type_to_node["invariant"].instrlist[0][0]
        stmt1 = extract_and_replace_variables(stmt1, "invariant", "assert")

        stmt2 = block_type_to_node["loop condition"].instrlist[0][0]
        stmt2 = extract_and_replace_variables(stmt2, "loop condition", "assert")
        stmt2 = stmt2.replace(">", "==")  # Replace ">" with "==" for loop false condition

        # Add extra statements to the assert block
        extra_stmts = [[stmt1, "invariant_out"], [stmt2, "loop_false_condition"]]
        block_type_to_node["assert"].instrlist = extra_stmts + block_type_to_node["assert"].instrlist

        stmt = block_type_to_node["loop condition"].instrlist[0][0]
        stmt = extract_and_replace_variables(stmt, "loop condition", "invariant")
        block_type_to_node["loop condition"].instrlist[0][0] = stmt  # Update the loop condition statement

        # Rename variables in nodes
        process_and_rename_nodes(sorted_nodes)

        # Process nodes for further renaming and linking
        for node in sorted_nodes[::-1]:
            if (node.irID > block_type_to_node["loop end"].irID) or \
               (node.irID <= block_type_to_node["loop condition"].irID):
                continue  # Skip nodes outside the loop range
            successors = list(cfg.nxgraph.successors(node))
            if node == block_type_to_node["loop end"]:
                successors.append(block_type_to_node["assert"])  # Add assert block as a successor
            process_bb2(node, successors)

        # Process the assume block with its successors
        process_bb2(
            block_type_to_node["assume"],
            [block_type_to_node["invariant"], block_type_to_node["loop condition"]],
        )

        # Extract preconditions, postconditions, and loop-related information
        pre_condition = []
        post_condition = []
        loop_condition = []
        invariant_in = []
        invariant_out = []
        loop_body = []
        loop_false_condition = []

        # Extract preconditions from the assume block
        for stmt in block_type_to_node["assume"].instrlist:
            pre_condition.append(stmt[0])

        # Extract postconditions from the assert block
        for stmt in block_type_to_node["assert"].instrlist:
            if stmt[1] == "assert":
                post_condition.append(stmt[0])

        # Extract loop condition statements
        for stmt in block_type_to_node["loop condition"].instrlist:
            loop_condition.append(stmt[0])

        # Extract invariant input
        invariant_in.append(block_type_to_node["invariant"].instrlist[0][0])

        # Extract invariant output and loop false condition
        for stmt in block_type_to_node["assert"].instrlist:
            if stmt[1] == "invariant_out":
                invariant_out.append(stmt[0])
            if stmt[1] == "loop_false_condition":
                loop_false_condition.append(stmt[0])

        # Process nodes to extract loop body
        node_to_stmt_list = {}
        for node in sorted_nodes:
            if (node.irID > block_type_to_node["loop end"].irID) or \
               (node.irID <= block_type_to_node["loop condition"].irID):
                continue  # Skip nodes outside the loop range
            new_instrlist, condition = process_bb3(node)
            node_to_stmt_list[node] = [new_instrlist, condition]

        # Build the loop body
        visited = set()
        for node in sorted_nodes:
            if (node.irID > block_type_to_node["loop end"].irID) or \
               (node.irID <= block_type_to_node["loop condition"].irID) or \
               (node in visited):
                continue  # Skip nodes outside the loop range or already visited
            instrList, condition = node_to_stmt_list[node]
            loop_body.append(["assign", instrList])  # Add assignments to the loop body
            visited.add(node)
            if condition is not None:
                # Process if-else conditions in the loop body
                successors = sorted(list(cfg.nxgraph.successors(node)), key=lambda x: x.irID)
                instrList1 = node_to_stmt_list[successors[0]][0]
                instrList2 = node_to_stmt_list[successors[1]][0]
                loop_body.append(["if-else", condition, instrList1, instrList2])
                visited.add(successors[0])
                visited.add(successors[1])

        # Return extracted information for loops
        return pre_condition, post_condition, loop_condition, invariant_in, invariant_out, loop_body, loop_false_condition

    else:
        # Check CFG format for programs without loops
        check_cfg_format_without_loop(cfg)

        # Rename variables in nodes
        process_and_rename_nodes(sorted_nodes)

        # Process nodes for further renaming and linking
        for node in sorted_nodes[::-1]:
            if node.name == "END":
                continue  # Skip the END node
            successors = list(cfg.nxgraph.successors(node))
            process_bb2(node, successors)

        # Extract preconditions, postconditions, and code body
        pre_condition = []
        post_condition = []
        code_body = []

        # Process nodes to extract statements and conditions
        node_to_stmt_list = {}
        for node in sorted_nodes:
            if node.name == "END":
                continue  # Skip the END node
            new_instrlist, condition = process_bb3(node)
            node_to_stmt_list[node] = [new_instrlist, condition]

        # Extract preconditions from the assume block
        for stmt in block_type_to_node["assume"].instrlist:
            if stmt[1] == "assume":
                pre_condition.append(stmt[0])

        # Extract postconditions from the assert block
        for stmt in block_type_to_node["assert"].instrlist:
            if stmt[1] == "assert":
                post_condition.append(stmt[0])

        # Build the code body
        visited = set()
        for node in sorted_nodes:
            if node.name == "END" or (node in visited):
                continue  # Skip the END node or already visited nodes
            instrList, condition = node_to_stmt_list[node]
            code_body.append(["assign", instrList])  # Add assignments to the code body
            visited.add(node)
            if condition is not None:
                # Process if-else conditions in the code body
                successors = sorted(list(cfg.nxgraph.successors(node)), key=lambda x: x.irID)
                instrList1 = node_to_stmt_list[successors[0]][0]
                instrList2 = node_to_stmt_list[successors[1]][0]
                code_body.append(["if-else", condition, instrList1, instrList2])
                visited.add(successors[0])
                visited.add(successors[1])

        # Return extracted information for programs without loops
        return pre_condition, post_condition, code_body

