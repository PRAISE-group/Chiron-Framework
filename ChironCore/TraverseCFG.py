from ChironAST import ChironAST
from cfg import ChironCFG
import networkx as nx
import re
import cfg.cfgBuilder as cfgB


def extract_variables_assign(stmt):
    # Remove whitespace and split the statement into LHS and RHS
    stmt = stmt.strip()
    if "=" not in stmt:
        raise ValueError(f"Invalid assignment statement: {stmt}")
    
    lhs_expr, rhs_expr = stmt.split("=", 1)
    lhs_expr = lhs_expr.strip()
    rhs_expr = rhs_expr.strip()

    # Extract variables from LHS and RHS using regex
    lhs_vars = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*)', lhs_expr)
    rhs_vars = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*)', rhs_expr)

    return rhs_vars, rhs_expr, lhs_vars, lhs_expr

def extract_variables_others(stmt):
    variables = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*)', stmt)
    return variables

def rename_vars(ir):
    updated_ir = []
    invariant = ""
    invariant_vars = []
    rename_map = {}
    for stmt in ir:
        lexpr = ""
        rexpr = ""
        rhs_vars = []
        lhs_vars = []
        # print(stmt)
        if stmt[1] == "assign":
            vars = extract_variables_assign(stmt[0])
            rhs_vars = vars[0]
            rexpr = vars[1]
            lhs_vars = vars[2]
            lexpr = vars[3]
        else:
            vars = extract_variables_others(stmt[0])
            # print(vars)
            rhs_vars = vars
            rexpr = stmt[0]
            lhs_vars = []
            lexpr = ""
        
        # print(rhs_vars, rexpr, lhs_vars, lexpr)
        for var in rhs_vars:
            if var not in rename_map:
                rename_map[var] = 0
                # raise ValueError(f"Variable '{var}' not initialised before first use!")
            rexpr = re.sub(rf'{var}\b', f'{var}_{rename_map[var]}', rexpr)

        for var in lhs_vars:
            if var not in rename_map:
                rename_map[var] = 1
            else:
                rename_map[var] = rename_map[var] + 1
            lexpr = re.sub(rf'{var}\b', f'{var}_{rename_map[var]}', lexpr)

        if lexpr != "":
            lexpr += '='
            updated_ir.append([lexpr+rexpr, stmt[1]])
        else:
            updated_ir.append([rexpr, stmt[1]])
        
    # print(updated_ir)
    return rename_map, updated_ir


def process_bb1(node:ChironCFG.BasicBlock):
    new_instrlist = []
    block_id = node.irID
    for entry in node.instrlist:
        stmt = str(entry[0])
        if(stmt == "False" or stmt == "True"):
            continue
        type = None
        if isinstance(entry[0], ChironAST.AssignmentCommand):
            type = "assign"
        elif isinstance(entry[0], ChironAST.ConditionCommand):
            type = "condition"
        elif isinstance(entry[0], ChironAST.AnalysisCommand):
            if(entry[0].stmt == "assert"):
                stmt = stmt.split("assert")[-1].strip()
                type = "assert"
            elif(entry[0].stmt == "assume"):
                stmt = stmt.split("assume")[-1].strip()
                type = "assume"
            elif(entry[0].stmt == "invariant"):
                stmt = stmt.split("invariant")[-1].strip()
                type = "invariant"
            else:
                raise ValueError(f"Unknown type of AnalysisCommand: {entry[0].stmt}")
        # else:
        #     raise ValueError(f"Unknown type of instruction: {entry[0]}")
        stmt_vars = re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', stmt)
        for var in stmt_vars:
            if var == "REPCOUNTER":
                stmt = re.sub(rf':{var}\b', f':__rep_counter_1', stmt)
                var = f"__rep_counter_1"
            stmt = re.sub(rf':{var}\b', f':{var}_{block_id}', stmt)
        # vars.update(stmt_vars)
        new_instrlist.append([stmt, type])
    
    # print(f"Block ID: {block_id}")
    # print(f"New Instruction List: {new_instrlist}") 
    node.instrlist = new_instrlist
    return

def process_bb2(node, successors):
    new_instrlist = node.instrlist
    block_id = node.irID
    # print(new_instrlist)
    rename_map = node_to_rename_map[node] 
    primary_var_to_id = {}
    for var, id in rename_map.items():
        primary_var = "_".join(var.split("_")[0:-1])
        primary_var_to_id[primary_var] = id  
    # print(rename_map)
    # print()

    for succ in successors:
        if(succ.irID <= block_id):
            continue
        for entry in succ.instrlist:
            # Find all variables used in entry without assignment
            stmt = str(entry[0])
            if entry[1] == "assign":
                vars = extract_variables_assign(stmt)
                stmt = vars[1]
            stmt_vars = re.findall(r'(:[a-zA-Z_][a-zA-Z0-9_]*_0)', stmt)
            for var in stmt_vars:
                primary_var = "_".join(var.split("_")[0:-2])
                if primary_var in primary_var_to_id:
                    new_stmt = f"{primary_var}_{succ.irID}_0 = {primary_var}_{block_id}_{primary_var_to_id[primary_var]}"
                else:
                    new_stmt = f"{primary_var}_{succ.irID}_0 = {primary_var}_{block_id}_0"
                new_entry = [new_stmt, "assign"]
                if new_entry not in new_instrlist:
                    new_instrlist.append([new_stmt, "assign"])
    # rename_map, new_instrlist = rename_vars(new_instrlist)
    node.instrlist = new_instrlist
    return

def process_bb3(node):
    new_instrlist = []
    condition = None
    for entry in node.instrlist:
        if entry[1] == "assign":
            new_instrlist.append(entry[0])
        elif entry[1] == "condition":
            condition = entry[0]
    return new_instrlist, condition    

block_type_to_node = {}
node_to_block_type = {}
node_to_rename_map = {}

def check_cfg_format_with_loop(cfg: ChironCFG.ChironCFG):
    nodes_list = list(cfg.nxgraph.nodes)
    """
    Check if all are present - assume, assert, invariant, loop condition
    """
    for node in nodes_list:
        instrList = node.instrlist
        
        for entry in instrList:
            if entry[1] == "assume":
                if "assume" in block_type_to_node.keys():
                    raise ValueError(f"More than one assume statement is not allowed")
                else:
                    block_type_to_node["assume"] = node
                    node_to_block_type[node] = "assume"
                    
            elif entry[1] == "assert":
                if "assert" in block_type_to_node.keys():
                    raise ValueError(f"More than one assert statement is not allowed")
                else:
                    block_type_to_node["assert"] = node
                    node_to_block_type[node] = "assert"
                    
            elif entry[1] == "invariant":
                if "invariant" in block_type_to_node.keys():
                    raise ValueError(f"More than one invariant statement is not allowed")
                else:
                    block_type_to_node["invariant"] = node
                    node_to_block_type[node] = "invariant"

        predecessors = list(cfg.predecessors(node))
        successors = list(cfg.successors(node))
        if len(predecessors) == 2 and len(successors) == 2:
            if predecessors[0].irID > node.irID or predecessors[1].irID > node.irID:
                if "loop condition" in block_type_to_node.keys():
                    raise ValueError(f"More than one loop is not allowed")
                else:
                    block_type_to_node["loop condition"] = node
                    node_to_block_type[node] = "loop condition"
    
    if "assume" not in block_type_to_node.keys():
        raise ValueError("Assume statement is missing")
    if "assert" not in block_type_to_node.keys():
        raise ValueError("Assert statement is missing")
    if "invariant" not in block_type_to_node.keys():
        raise ValueError("Invariant statement is missing")
    if "loop condition" not in block_type_to_node.keys():
        raise ValueError("Loop condition is missing")
    
    
    """
    Check if position of blocks in CFG  and format of individual blocks is correct
    """
    assume_node = block_type_to_node["assume"]
    assert_node = block_type_to_node["assert"]
    invariant_node = block_type_to_node["invariant"]
    loop_condition_node = block_type_to_node["loop condition"]
    
    if assume_node.irID != 0 or assume_node.instrlist[0][1] != "assume":
        raise ValueError("Assume statement should be first statement")
    
    if len(assume_node.instrlist) > 2:
        raise ValueError("Unexpected statement(s) after assume")
    
    if assume_node not in cfg.predecessors(loop_condition_node):
        raise ValueError("Loop condition should have assume as predecessor")
    
    if loop_condition_node not in cfg.successors(assume_node):
        raise ValueError("Assume should have loop condition as successor")
    
    if invariant_node not in cfg.successors(loop_condition_node) or invariant_node.instrlist[0][1] != "invariant":
        raise ValueError("Loop body should start with invariant")
    
    if assert_node not in cfg.successors(loop_condition_node):
        raise ValueError("Assert should be after of loop body ends")
    
    if len(loop_condition_node.instrlist) > 1:
        raise ValueError("Unexpected statement(s) after loop condition")
    
    if "__rep_counter_1_1 > 0" not in loop_condition_node.instrlist[0][0]:
        raise ValueError(f"Invalid Loop condition: {loop_condition_node.instrlist[0][0]}")

    if len(assert_node.instrlist) > 1:
        raise ValueError("Unexpected statement(s) after assert")
          
    for pred in cfg.predecessors(loop_condition_node):
        if pred.irID != 0:
            for entry in pred.instrlist:
                if (f"__rep_counter_1_{pred.irID}" in entry[0]) and (entry[1] == "assign"):
                    block_type_to_node["loop end"] = pred
                    break
    
    if "loop end" not in block_type_to_node.keys():
        raise ValueError("Could not find loop end statement")
    
    return

def check_cfg_format_without_loop(cfg: ChironCFG.ChironCFG):
    nodes_list = list(cfg.nxgraph.nodes)
    """
    Check if all are present - assume, assert
    """
    for node in nodes_list:
        instrList = node.instrlist
        
        for entry in instrList:
            if entry[1] == "assume":
                if "assume" in block_type_to_node.keys():
                    raise ValueError(f"More than one assume statement is not allowed")
                else:
                    block_type_to_node["assume"] = node
                    node_to_block_type[node] = "assume"
                    
            elif entry[1] == "assert":
                if "assert" in block_type_to_node.keys():
                    raise ValueError(f"More than one assert statement is not allowed")
                else:
                    block_type_to_node["assert"] = node
                    node_to_block_type[node] = "assert"
    
    if "assume" not in block_type_to_node.keys():
        raise ValueError("Assume statement is missing")
    if "assert" not in block_type_to_node.keys():
        raise ValueError("Assert statement is missing")
    
    
    """
    Check if position of blocks in CFG  and format of individual blocks is correct
    """
    assume_node = block_type_to_node["assume"]
    assert_node = block_type_to_node["assert"]
    
    if assume_node.irID != 0 or assume_node.instrlist[0][1] != "assume":
        raise ValueError("Assume statement should be first statement")
    
    for succ in cfg.successors(assert_node):
        if succ.irID != float('inf'):
            raise ValueError("Assert should be last statement")
    
    if assert_node.instrlist[-1][1] != "assert":
        raise ValueError("Assert statement should be last statement")
    
    return
    


def process_and_rename_nodes(sorted_nodes):
    for node in sorted_nodes:
        if node.name == "END":
            continue  # Skip END node
        node_to_rename_map[node], new_instrlist = rename_vars(node.instrlist)
        node.instrlist = new_instrlist

def Traverse(cfg: ChironCFG.ChironCFG, has_loop:bool = True):
    # Assign special irID values for START and END nodes
    for node in cfg.nxgraph.nodes:
        if node.name == "START":
            node.irID = 0
        elif node.name == "END":
            node.irID = float('inf')  # Treat END as infinite

    # Sort nodes by irID in ascending order
    sorted_nodes = sorted(cfg.nxgraph.nodes, key=lambda node: node.irID)

    # Process nodes in sorted order
    for node in sorted_nodes:
        if node.name == "END":
            continue  # Skip END node
        process_bb1(node)
    
    if(has_loop):
        # Check CFG format
        check_cfg_format_with_loop(cfg)

        stmt1 = block_type_to_node["invariant"].instrlist[0][0]
        stmt_vars = extract_variables_others(stmt1)
        for var in stmt_vars:
            primary_var = "_".join(var.split("_")[0:-1])
            stmt1 = re.sub(rf'{primary_var}_{block_type_to_node["invariant"].irID}\b', f'{primary_var}_{block_type_to_node["assert"].irID}', stmt1)

        stmt2 = block_type_to_node["loop condition"].instrlist[0][0]
        stmt_vars = extract_variables_others(stmt2)
        for var in stmt_vars:
            primary_var = "_".join(var.split("_")[0:-1])
            stmt2 = re.sub(rf'{primary_var}_{block_type_to_node["loop condition"].irID}\b', f'{primary_var}_{block_type_to_node["assert"].irID}', stmt2)
        stmt2 = stmt2.replace(">", "==")
        
        extra_stmts = [ [stmt1, "invariant_out"], [stmt2, "loop_false_condition"] ]
        block_type_to_node["assert"].instrlist =  extra_stmts + block_type_to_node["assert"].instrlist
    
    

        process_and_rename_nodes(sorted_nodes)

        # # Process nodes again in sorted order for further processing
        for node in sorted_nodes[::-1]:
            if (node.irID > block_type_to_node["loop end"].irID) or \
                (node.irID <= block_type_to_node["loop condition"].irID):
                continue  
            successors = list(cfg.nxgraph.successors(node))
            if(node == block_type_to_node["loop end"]):
                successors.append(block_type_to_node["assert"])
            process_bb2(node, successors)
            
        process_bb2(block_type_to_node["assume"], [block_type_to_node["invariant"], block_type_to_node["loop condition"]])

        # # Print the final CFG
        # for node in sorted_nodes:
        #     print(f"{node.irID}:")
        #     for entry in node.instrlist:
        #         print(f"\t{entry[0]}: {entry[1]}")

        pre_condition = []
        post_condition = []
        loop_condition = []
        invariant_in = []
        invariant_out = []
        loop_body = []
        loop_false_condition = []
        
        for stmt in block_type_to_node["assume"].instrlist:
            pre_condition.append(stmt[0])
        for stmt in block_type_to_node["assert"].instrlist:
            if(stmt[1] == "assert"):
                post_condition.append(stmt[0])
        for stmt in block_type_to_node["loop condition"].instrlist:
            loop_condition.append(stmt[0])
            
        invariant_in.append(block_type_to_node["invariant"].instrlist[0][0])

        for stmt in block_type_to_node["assert"].instrlist:
            if stmt[1] == "invariant_out":
                invariant_out.append(stmt[0])
            if stmt[1] == "loop_false_condition":
                loop_false_condition.append(stmt[0])

        node_to_stmt_list = {}
        for node in sorted_nodes:
            if (node.irID > block_type_to_node["loop end"].irID) or \
                (node.irID <= block_type_to_node["loop condition"].irID):
                continue  
            new_instrlist, condition= process_bb3(node)
            node_to_stmt_list[node] = [new_instrlist, condition]
        
        # print("Node to Statement List:")
        # for node, (stmt_list, condition) in node_to_stmt_list.items():
        #     print(f"Node {node.irID}:")
        #     print(f"Statements: {stmt_list}")
        #     print(f"Condition: {condition}")
        
        visited = set()
        for node in sorted_nodes:
            if (node.irID > block_type_to_node["loop end"].irID) or \
                (node.irID <= block_type_to_node["loop condition"].irID) or \
                (node in visited):
                continue
            instrList, condition = node_to_stmt_list[node]
            loop_body.append(["assign", instrList])
            visited.add(node)
            if(condition != None):
                successors = sorted(list(cfg.nxgraph.successors(node)), key=lambda x: x.irID)
                instrList1 = node_to_stmt_list[successors[0]][0]
                instrList2 = node_to_stmt_list[successors[1]][0]
                loop_body.append(["if-else", condition, instrList1, instrList2])
                visited.add(successors[0])
                visited.add(successors[1])
                
                
        return pre_condition, post_condition, loop_condition, invariant_in, invariant_out, loop_body, loop_false_condition
    
    else:
        # Check CFG format
        check_cfg_format_without_loop(cfg)

        process_and_rename_nodes(sorted_nodes)

        # print(node_to_rename_map)


        for node in sorted_nodes[::-1]:
            if node.name == "END":
                continue
            successors = list(cfg.nxgraph.successors(node))
            process_bb2(node, successors)

        pre_condition = []
        post_condition = []
        code_body = []

        node_to_stmt_list = {}
        for node in sorted_nodes:
            if node.name == "END":
                continue
            new_instrlist, condition= process_bb3(node)
            node_to_stmt_list[node] = [new_instrlist, condition]

        for stmt in block_type_to_node["assume"].instrlist:
            if(stmt[1] == "assume"):
                pre_condition.append(stmt[0])
        for stmt in block_type_to_node["assert"].instrlist:
            if(stmt[1] == "assert"):
                post_condition.append(stmt[0])
        
        visited = set()
        for node in sorted_nodes:
            if node.name == "END" or (node in visited):
                continue
            instrList, condition = node_to_stmt_list[node]
            code_body.append(["assign", instrList])
            visited.add(node)
            if(condition != None):
                successors = sorted(list(cfg.nxgraph.successors(node)), key=lambda x: x.irID)
                instrList1 = node_to_stmt_list[successors[0]][0]
                instrList2 = node_to_stmt_list[successors[1]][0]
                code_body.append(["if-else", condition, instrList1, instrList2])
                visited.add(successors[0])
                visited.add(successors[1])

        # print(pre_condition)
        # print(post_condition)
        # print(code_body)
        return pre_condition, post_condition, code_body

