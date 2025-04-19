import ast
import re 

"""
This module provides functionality to convert infix expressions into prefix (SMT-LIB) format.
It uses Python's `ast` module to parse expressions and a custom visitor class to traverse
the abstract syntax tree (AST) and generate the corresponding prefix notation.
"""

class PrefixNotationConverter(ast.NodeVisitor):
    """
    A custom AST visitor class to convert infix expressions into prefix notation.
    """

    def visit_BinOp(self, node):
        """
        Handles binary operations (e.g., +, -, *, /).
        Converts them into prefix notation (e.g., (+ left right)).
        """
        op = self.get_operator(node.op)
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({op} {left} {right})"

    def visit_Compare(self, node):
        """
        Handles comparison operations (e.g., ==, !=, >, <, >=, <=).
        Converts them into prefix notation.
        Special handling for "!=" to represent it as (not (= left right)).
        """
        op = self.get_operator(node.ops[0])
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if op == '!=':  # Handle "!=" as (not (= expr1 expr2))
            return f"(not (= {left} {right}))"
        else:
            return f"({op} {left} {right})"

    def visit_BoolOp(self, node):
        """
        Handles boolean operations (e.g., and, or).
        Converts them into prefix notation (e.g., (and expr1 expr2 ...)).
        """
        op = self.get_operator(node.op)
        values = " ".join(self.visit(value) for value in node.values)
        return f"({op} {values})"

    def visit_UnaryOp(self, node):
        """
        Handles unary operations (e.g., not, -).
        Converts them into prefix notation (e.g., (not operand)).
        """
        op = self.get_operator(node.op)
        operand = self.visit(node.operand)
        return f"({op} {operand})"

    def visit_Name(self, node):
        """
        Handles variable names.
        Returns the variable name as is.
        """
        return node.id

    def visit_Constant(self, node):
        """
        Handles constant values (e.g., numbers, strings).
        Returns the constant value as a string.
        """
        return str(node.value)

    def get_operator(self, op):
        """
        Maps Python AST operators to their corresponding SMT-LIB operators.
        """
        operators = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: 'div',
            ast.Gt: '>',
            ast.Lt: '<',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.Eq: '=',
            ast.NotEq: '!=',
            ast.Mod: 'mod',
            ast.And: 'and',
            ast.Or: 'or',
            ast.Not: '~',
            ast.Assign: '=',
            ast.USub: '-',  # Unary subtraction
        }
        return operators[type(op)]

def preprocess_expression(expr: str, replace_eq):
    """
    Preprocesses the input expression to make it compatible with Python's `ast` module.
    - Replaces variable prefixes (e.g., ":var" -> "var").
    - Removes spaces.
    - Optionally replaces single "=" with "==" for equality checks.

    Args:
        expr (str): The input infix expression.
        replace_eq (bool): Whether to replace "=" with "==" for equality.

    Returns:
        str: The preprocessed expression.
    """
    expr = re.sub(r":(\w+)", r"\1", expr)  # Remove ":" prefix from variables
    expr = expr.replace(" ", "")  # Remove spaces
    if replace_eq:
        expr = re.sub(r"(?<![<>=!])=(?!=)", "==", expr)  # Replace "=" with "==" for equality
    return expr

def Construct_AST(expr: str, replace_eq):
    """
    Constructs an abstract syntax tree (AST) from the given infix expression.

    Args:
        expr (str): The input infix expression.
        replace_eq (bool): Whether to preprocess the expression to replace "=" with "==".

    Returns:
        ast.AST: The constructed AST.

    Raises:
        Exception: If there is a syntax error in the input expression.
    """
    expr = preprocess_expression(expr, replace_eq)
    # print(expr)  # Debugging print for the preprocessed expression
    try:
        tree = ast.parse(expr, mode='eval')  # Parse the expression in evaluation mode
        return tree
    except SyntaxError as e:
        print(expr)  # Debugging print for the expression causing the error
        raise Exception(f"Syntax Error: {e}")

def Infix_To_Prefix(expr: str, replace_eq=False):
    """
    Converts an infix expression into prefix notation.

    Args:
        expr (str): The input infix expression.
        replace_eq (bool): Whether to preprocess the expression to replace "=" with "==".

    Returns:
        str: The prefix notation of the expression, or None if the input is empty.
    """
    if expr:
        tree = Construct_AST(expr, replace_eq)
        if tree:
            converter = PrefixNotationConverter()
            expr = converter.visit(tree.body)  # Visit the root of the AST
            return expr
        else:
            return None
    else:
        return None

