from ChironAST import ChironAST
from cfg import ChironCFG
import networkx as nx
import re

# rename_map = {}

def extract_variables_assign(stmt):
    # Remove whitespace and split the statement into LHS and RHS
    stmt = stmt.strip()
    if "=" not in stmt:
        raise ValueError(f"Invalid assignment statement: {stmt}")
    
    lhs_expr, rhs_expr = stmt.split("=", 1)
    lhs_expr = lhs_expr.strip()
    rhs_expr = rhs_expr.strip()

    # Extract variables from LHS and RHS using regex
    lhs_vars = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', lhs_expr)
    rhs_vars = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', rhs_expr)

    return rhs_vars, rhs_expr, lhs_vars, lhs_expr

def extract_variables_others(stmt):
    variables = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', stmt)
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
        if stmt[1] == 'invariant':
            invariant = stmt[0]
            invariant_vars = extract_variables_others(invariant)
            stmt = (stmt[0], "invariant_in")
            
        if stmt[1] == "assign" or stmt[1] == "loop-end" or stmt[1] == "ite" or stmt[1] == "loop-init":
            vars = extract_variables_assign(stmt[0])
            rhs_vars = vars[0]
            rexpr = vars[1]
            lhs_vars = vars[2]
            lexpr = vars[3]
        else:
            vars = extract_variables_others(stmt[0])
            rhs_vars = vars
            rexpr = stmt[0]
            lhs_vars = []
            lexpr = ""
        
        # print(rhs_vars, rexpr, lhs_vars, lexpr)
        for var in rhs_vars:
            if var == "REPCOUNTER":
                rexpr = re.sub(rf'{var}\b', '__rep_counter_1', rexpr)
                var = "__rep_counter_1"
            if var not in rename_map:
                rename_map[var] = 0
                # raise ValueError(f"Variable '{var}' not initialised before first use!")
            rexpr = re.sub(rf':{var}\b', f'{var}_{rename_map[var]}', rexpr)

        for var in lhs_vars:
            if var == "REPCOUNTER":
                print("Warning: ':REPCOUNTER' is a reserved variable name for loop counter.")
                lexpr = re.sub(rf'{var}\b', '__rep_counter_1', lexpr)
                var = "__rep_counter_1"
            if var not in rename_map:
                rename_map[var] = 0
            else:
                rename_map[var] = rename_map[var] + 1
            lexpr = re.sub(rf'{var}\b', f'{var}_{rename_map[var]}', lexpr)

        if lexpr != "":
            lexpr += '='
            updated_ir.append([lexpr+rexpr, stmt[1]])
        else:
            updated_ir.append([rexpr, stmt[1]])
        
        if stmt[1]=='loop-end':
            invariant_out = invariant
            for var in invariant_vars:
                if var == "REPCOUNTER":
                    invariant_out = re.sub(rf'{var}\b', '__rep_counter_1', invariant_out)
                    var = "__rep_counter_1"
                if var not in rename_map:
                    rename_map[var] = 0
                    # raise ValueError(f"Variable '{var}' not initialised before first use!")
                invariant_out = re.sub(rf'{var}\b', f'{var}_{rename_map[var]}', invariant_out)
            updated_ir.append((invariant_out, "invariant_out"))
    # print(updated_ir)
    return rename_map, updated_ir

def process_bb(node:ChironCFG.BasicBlock):
    curr_instrlist = node.instrlist
    new_instrlist = []
    block_id = node.irID

    for entry in node.instrlist:
        stmt = str(entry[0])
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
            stmt = re.sub(rf':{var}\b', f'{var}_{block_id}', stmt)
        # vars.update(stmt_vars)
        new_instrlist.append([stmt, type])
    
    rename_map, new_instrlist = rename_vars(new_instrlist)
    print(f"Block ID: {block_id}")
    print(f"New Instruction List: {new_instrlist}")
        
    return new_instrlist
                     

def Traverse(cfg: ChironCFG.ChironCFG):
    for node in cfg.nxgraph.nodes:
        if(node.name == "START" or node.name == "END"):
            continue
        process_bb(node)
    