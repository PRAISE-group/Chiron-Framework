import re

def extract_variables(expression: str):
    # Match variable-like words that are not numbers and are not part of function calls
    tokens = re.findall(r'[a-zA-Z_]\w*', expression)
    
    keywords = {"ite", "and", "or", "not", "assert", "div"}
    variables = {token for token in tokens if token not in keywords and not token.isdigit()}
    return sorted(variables)  # Sorted for consistency

def CheckOutput(constraint_statement, smtlib_code):
    if "None" in constraint_statement:
        raise Exception("Syntax Error: Invalid Syntax in constraint file!")
    for line in smtlib_code:
        if "None" in line:
            raise Exception("Syntax Error: Invalid Syntax in code!")
    
    constraint_vars = extract_variables(constraint_statement)
    code_vars = {var for line in smtlib_code for var in extract_variables(line)}

    unknown_vars = set(constraint_vars) - code_vars  # Get all missing variables
    if unknown_vars:
        raise Exception(f"Syntax Error: Unknown variables in constraint file - {unknown_vars}")
    return sorted(code_vars)
    