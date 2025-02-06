import sys
from ConstraintParser import Constraint_Parser
from PrefixConvertor import Infix_To_Prefix
from SMTLIBConvertor import CNF_To_SMTLIB

if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <filepath>")
        sys.exit(1)

filepath = sys.argv[1]

expr_dict, literal_groups = Constraint_Parser(filepath)

for key, expr in expr_dict.items():
    # print(f"key = {key}")
    # print(f"expr = {expr}")
    expr_dict[key] = Infix_To_Prefix(expr)

statement = CNF_To_SMTLIB(literal_groups, expr_dict)

print(f"Literal Map : {expr_dict}")
print(f"CNF groups : {literal_groups}")
print(f"SMTLIB Statement : {statement}")
