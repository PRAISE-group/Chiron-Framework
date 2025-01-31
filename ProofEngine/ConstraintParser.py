import re

def Constraint_Parser(filepath: str):
    data = ""
    with open(filepath, 'r') as file:
        data = file.read()
    
    expr_dict = {}
    literal_groups = []
    
    sections = data.split("\n\n")
    
    expression_lines = sections[0].strip().split("\n")
    for line in expression_lines:
        match = re.match(r"([a-zA-Z0-9_]+):\s*(.*)", line.strip())
        if match:
            literal = match.group(1)
            expression = match.group(2)
            expr_dict[literal] = expression
    
    literal_lines = sections[1].strip().split("\n")
    for line in literal_lines:
        literals = line.strip().split(",")
        literal_groups.append([literal.strip() for literal in literals])
    
    return expr_dict, literal_groups