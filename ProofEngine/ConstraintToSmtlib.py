import sys
from ConstraintParser import Constraint_Parser
from ChironCore.Infix_To_Prefix import Infix_To_Prefix
from CNF_To_SMTLIB import CNF_To_SMTLIB

def ConstraintToSmtlib(filepath):
    expr_dict, pre_condition, post_condition, invariant = Constraint_Parser(filepath)

    for key, expr in expr_dict.items():
        expr_dict[key] = Infix_To_Prefix(expr, replace_eq=True)
    
    def wrap_with_assert(s):
        return f"(assert {s})"
        
    if len(post_condition)>0 and len(invariant)>0:
        # loop
        pre_condition = CNF_To_SMTLIB(pre_condition, expr_dict)
        post_condition = CNF_To_SMTLIB(post_condition, expr_dict)
        invariant = CNF_To_SMTLIB(invariant, expr_dict)
    else:
        # normal
        pre_condition = CNF_To_SMTLIB(pre_condition, expr_dict)
        pre_condition = wrap_with_assert(pre_condition)
        post_condition = None
        invariant = None
        
    return pre_condition, post_condition, invariant
