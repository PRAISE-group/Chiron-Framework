import re
import sys

def Constraint_Parser(filepath: str):
    data = ""
    try:
        with open(filepath, "r") as file:
            data = file.read()

        # print("Constraints File Content:")
        # print(data)
    
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read the file - {e}")
        sys.exit(1)
    
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