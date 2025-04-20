import sys
import re

"""
This module provides helper functions for generating SMT-LIB code, extracting variables,
and converting conditions and code bodies into SMT-LIB format. It also includes functionality
to parse the program, generate IR, and build the control flow graph (CFG).
"""

# Add necessary paths for importing modules
sys.path.insert(0, "../cfg/")
sys.path.insert(0, "../ChironAST/")
sys.path.insert(0, "../ProofEngine/")

from ChironAST.builder import astGenPassSMTLIB
from ProofEngine.TurtleCommandsCompiler import TurtleCommandsCompiler
from ProofEngine.Infix_To_Prefix import Infix_To_Prefix
from cfg import cfgBuilder as cfgB

def generate_cfg_and_ir(parseTree, irHandler):
    """
    Parses the program, generates IR, compiles it into a new IR list, and builds the CFG.

    Args:
        parseTree: The parse tree of the program.
        irHandler: The IRHandler instance to manage the IR.

    Returns:
        tuple: A tuple containing the CFG and the number of loops in the program.
    """
    # Parse the program and generate IR
    astgen = astGenPassSMTLIB()
    ir = astgen.visitStart(parseTree)
    num_loops = astgen.repeatInstrCount
    irHandler.setIR(ir)

    # Compile the IR into a new IR list
    new_irList = []
    turt_compiler = TurtleCommandsCompiler()
    for entry in irHandler.ir:
        new_stmt = turt_compiler.compile(entry[0])
        for stmt in new_stmt:
            new_irList.append((stmt, entry[1]))

    # Build the CFG
    cfg = cfgB.buildCFG(new_irList, "control_flow_graph", False)

    return cfg, num_loops

def list_to_smtlib_stmt(L):
    """
    Converts a list of statements into SMT-LIB format.

    Args:
        L (list): A list of infix expressions.

    Returns:
        str: The SMT-LIB formatted string representing the list of statements.
    """
    if len(L) == 1:
        return Infix_To_Prefix(L[0], True)
    smtlib_stmt = "(and "
    for stmt in L:
        stmt = Infix_To_Prefix(stmt, True)
        smtlib_stmt += f"{stmt} "
    smtlib_stmt += ")\n"
    return smtlib_stmt

def extract_variables(expression: str):
    """
    Extracts variables from a given expression.

    Args:
        expression (str): The input expression.

    Returns:
        list: A sorted list of variables found in the expression.
    """
    tokens = re.findall(r'[a-zA-Z_]\w*', expression)
    keywords = {"ite", "and", "or", "not", "assert", "div", "true", "false", "mod"}
    variables = {token for token in tokens if token not in keywords and not token.isdigit()}
    return sorted(variables)

def generate_smtlib_code(pre_condition, post_condition, loop_condition=None, invariant_in=None, invariant_out=None, loop_body=None, loop_false_condition=None):
    """
    Generates SMT-LIB code based on the given conditions and loop structure.

    Args:
        pre_condition (str): The pre-condition in SMT-LIB format.
        post_condition (str): The post-condition in SMT-LIB format.
        loop_condition (str, optional): The loop condition in SMT-LIB format.
        invariant_in (str, optional): The loop invariant before the loop body.
        invariant_out (str, optional): The loop invariant after the loop body.
        loop_body (str, optional): The loop body in SMT-LIB format.
        loop_false_condition (str, optional): The condition when the loop exits.

    Returns:
        str: The generated SMT-LIB code.
    """
    smtlib_code = ""
    all_vars = set()

    if loop_condition is None:  # No loop
        check = f"(=> (and {pre_condition} {loop_body}) {post_condition})"
        all_vars.update(extract_variables(check))
        smtlib_code += "".join([f"(declare-fun {var} () Int)\n" for var in all_vars])
        smtlib_code += f"(assert (not {check}))\n"
        smtlib_code += "(check-sat)\n(get-model)\n"
    else:  # With loop
        first_check = f"(=> {pre_condition} {invariant_in})"
        second_check = f"(=> (and {invariant_in} {loop_body} {loop_condition}) {invariant_out})"
        third_check = f"(=> (and {invariant_out} {loop_false_condition}) {post_condition})"

        all_vars.update(extract_variables(first_check))
        all_vars.update(extract_variables(second_check))
        all_vars.update(extract_variables(third_check))

        smtlib_code += "".join([f"(declare-fun {var} () Int)\n" for var in all_vars])
        smtlib_code += "(push 1)\n"
        smtlib_code += f"(assert (not {first_check}))\n"
        smtlib_code += "(check-sat)\n(get-model)\n(pop 1)\n"
        smtlib_code += "(push 1)\n"
        smtlib_code += f"(assert (not {second_check}))\n"
        smtlib_code += "(check-sat)\n(get-model)\n(pop 1)\n"
        smtlib_code += "(push 1)\n"
        smtlib_code += f"(assert (not {third_check}))\n"
        smtlib_code += "(check-sat)\n(get-model)\n(pop 1)\n"

    return smtlib_code

def generate_code_body(code_body_list):
    """
    Generates the SMT-LIB code body from the given code body list.

    Args:
        code_body_list (list): A list of code body entries, where each entry is a tuple
                               representing an assignment or an if-else block.

    Returns:
        str: The SMT-LIB formatted code body as a string.
    """
    code_body = "(and "
    for entry in code_body_list:
        if entry[0] == "assign":
            for stmt in entry[1]:
                code_body += Infix_To_Prefix(stmt, True)
        elif entry[0] == "if-else":
            condition = entry[1]
            then_part = entry[2]
            else_part = entry[3]
            then_stmt = list_to_smtlib_stmt(then_part)
            else_stmt = list_to_smtlib_stmt(else_part)
            cond_stmt = list_to_smtlib_stmt([condition])
            then_stmt = f"(and {cond_stmt} {then_stmt})"
            else_stmt = f"(and (not {cond_stmt}) {else_stmt})"
            code_body += f"(or {then_stmt} {else_stmt})"
    code_body += "true)\n"
    return code_body
