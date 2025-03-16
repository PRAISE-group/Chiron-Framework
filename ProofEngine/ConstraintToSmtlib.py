import sys
from ConstraintParser import Constraint_Parser
from Infix_To_Prefix import Infix_To_Prefix
from SMTLIBConvertor import CNF_To_SMTLIB

def ConstraintToSmtlib(filepath):
    expr_dict, literal_groups = Constraint_Parser(filepath)

    for key, expr in expr_dict.items():
        expr_dict[key] = Infix_To_Prefix(expr, replace_eq=True)

    statement = CNF_To_SMTLIB(literal_groups, expr_dict)
    return statement
