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
    pre_condition = []
    
    sections = data.split("\n\n")
    
    if(len(sections)!=2 and len(sections)!=4):
        raise ValueError("Either 2 (without loop) or 4 (with loop) sections expected in constraint file")
    
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
        pre_condition.append([literal.strip() for literal in literals])
        
    post_condition = []
    invariant = []
    if(len(sections)==4):
        literal_lines = sections[2].strip().split("\n")
        for line in literal_lines:
            literals = line.strip().split(",")
            post_condition.append([literal.strip() for literal in literals])
            
        literal_lines = sections[3].strip().split("\n")
        for line in literal_lines:
            literals = line.strip().split(",")
            invariant.append([literal.strip() for literal in literals])
        
    return expr_dict, pre_condition, post_condition, invariant