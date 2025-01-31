import re

def parse_expressions_and_literals(data):
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


def read_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

file_path = "C1.txt"
data = read_input_from_file(file_path)
expr_dict, literal_groups = parse_expressions_and_literals(data)

print("Expression Dictionary:")
print(expr_dict)
print("\nTwo-Dimensional List of Literals:")
print(literal_groups)
