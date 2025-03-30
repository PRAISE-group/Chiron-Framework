# import re

# def get_vars(s):
#     """Extracts all variables from a string. 
#     Variables start with a colon and contain only alphanumeric characters and underscores.
#     """
#     return re.findall(r":[\w_]+", s)

# # Example usage:
# test_str = ":var1 = :value_2 + :anotherVar_3 * :__rep_counter_1"
# print(get_vars(test_str))  

#  # vars = set()
#     # for entry in loop_body:
#     #     if entry[0] == "assign":
#     #         _, statement = entry
#     #         vars.update(get_vars(statement))

#     #     elif entry[0] == "if-else":
#     #         _, condition, if_statements, else_statements = entry
#     #         vars.update(get_vars(condition))

#     #         # Extract variables from all if-else statements
#     #         for stmt in if_statements:
#     #             vars.update(get_vars(stmt))
            
#     #         for stmt in else_statements:
#     #             vars.update(get_vars(stmt))
                
    
#     # for entry in loop_body:
#     #     smt_statement = None
#     #     if entry[0] == "assign":
#     #         _, statement = entry
#     #         smt_statement = Infix_To_Prefix(statement, True)
#     #     elif entry[0] == "if-else":
#     #         _, condition, if_statements, else_statements = entry
#     #         smt_statement = if_else_smtlib(condition, if_statements, else_statements)
        
#     #     if(smt_statement):
#     #         smtlib_code.append(smt_statement)
#     #     else:
#     #         print("Invalid Statement: Only assignment and if-else blocks are allowed")
#     #         return
#     # sectionTosmtlib(after_loop)
#     # print(after_loop)
#     # print(loop_body)
#     # print(vars)
#     # for line in smtlib_code:
#     #     print(line)

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

# # Example Usage:
# statements = [
#     ('assign', ':x = (:n - ((:n / 10) * 10))'),
#     ('assign', ':s1 = (:s + :x)'),
#     ('assign', ':n1 = (:n / 10)'),
#     ('assign', ':n = :n1'),
#     ('assign', ':s = :s1'),
#     ('if-else', '(:x > :s1)', [':z = :n'], [':z = :n1'])
# ]

# internal_vars, external_vars = classify_vars(statements)
# print("Internal Vars:", internal_vars)  # Assigned & used within the loop
# print("External Vars:", external_vars)  # Inputs from previous iterations

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

# Example Usage
statements = [
    ('assign', ':x = (:n - ((:n / 10) * 10))'),
    ('assign', ':s1 = (:s + :x)'),
    ('assign', ':n1 = (:n / 10)'),
    ('assign', ':n = :n1'),
    ('assign', ':s = :s1'),
    ('if-else', '(:x > :s1)', [':z = :n'], [':z = :n1'])
]

vars_to_modify = {':n', ':s'}  # Variables to be modified

updated_statements = rename_vars(statements, vars_to_modify)

for stmt in updated_statements:
    print(stmt)