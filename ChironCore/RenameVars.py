import re
# sys.path.insert(0, "../ChironCore/ChironAST/")
from ChironAST import ChironAST

def extract_variables(stmt):
    # Remove leading/trailing whitespace
    stmt = stmt.strip()

    # Extract all variables that start with ':'
    all_vars = set(re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', stmt))

    assigned = set()
    used = set()

    # Handle assignment only if it's a single '=' (not '==')
    # Use regex to find assignment outside of '==' comparison
    assignment_match = re.search(r'([^=!<>]=[^=])', stmt)

    if assignment_match:
        # Find the actual position of the '=' used for assignment
        eq_index = assignment_match.start(1) + assignment_match.group(1).index('=')
        lhs_exp = stmt[:eq_index]
        rhs_exp = stmt[eq_index + 1:]

        assigned = set(re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', lhs_exp))
        used = set(re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', rhs_exp))
        return [used, rhs_exp,  assigned, lhs_exp]
    else:
        used = all_vars
        return [used, stmt]


def rename_vars(ir):
    rename_map = {}
    updated_ir = []
    for stmt in ir:
        print(stmt[0])
        rhs_vars = ""
        lhs_vars = ""
        lexpr = ""
        rexpr = ""
        vars = extract_variables(str(stmt[0]))
        rhs_vars = vars[0]
        rexpr = vars[1]
        for var in rhs_vars:
            if var not in rename_map:
                raise ValueError(f"Variable '{var}' not initialised before first use!")
            rexpr = re.sub(rf':{var}\b', f'{var}_{rename_map[var]}', rexpr)
        if(type(stmt[0])==ChironAST.AssignmentCommand):
            lhs_vars = vars[2]
            lexpr = vars[3]
            for var in lhs_vars:
                if var not in rename_map:
                    rename_map[var] = 0
                else:
                    rename_map[var] = rename_map[var] + 1
                lexpr = re.sub(rf':{var}\b', f'{var}_{rename_map[var]}', lexpr)
            lexpr += '='
        # print("Renamed:", lexpr+rexpr)
        # print(type(lexpr))
        # print(type(rexpr))
        updated_ir.append((lexpr+rexpr,stmt[1])) 
    print(updated_ir)
    return updated_ir
                   
