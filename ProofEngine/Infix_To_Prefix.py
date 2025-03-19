import ast
import re 

class PrefixNotationConverter(ast.NodeVisitor):
    def visit_BinOp(self, node):
        op = self.get_operator(node.op)
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({op} {left} {right})"

    def visit_Compare(self, node):
        op = self.get_operator(node.ops[0])
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if op == '!=':  # Handle "!=" as (not (= expr1 expr2))
            return f"(not (= {left} {right}))"
        else:
            op = self.get_operator(node.ops[0])
            return f"({op} {left} {right})"

    def visit_BoolOp(self, node):
        op = self.get_operator(node.op)
        values = " ".join(self.visit(value) for value in node.values)
        return f"({op} {values})"

    def visit_UnaryOp(self, node):
        op = self.get_operator(node.op)
        operand = self.visit(node.operand)
        return f"({op} {operand})"

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        return str(node.value)

    def get_operator(self, op):
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
            # ast.Mod: 'mod',
            ast.And: 'and',
            ast.Or: 'or',
            ast.Not: '~',
            ast.Assign: '=',
            ast.USub: '-',
        }
        return operators[type(op)]

def preprocess_expression(expr: str, replace_eq):
    expr = re.sub(r":(\w+)", r"\1", expr) 
    expr = expr.replace(" ", "")
    if(replace_eq):
        expr = re.sub(r"(?<![<>=!])=(?!=)", "==", expr)
    return expr

def Construct_AST(expr: str, replace_eq):
    expr= preprocess_expression(expr, replace_eq)
    try:
        tree = ast.parse(expr, mode='eval')
        return tree
    except SyntaxError as e:
        raise Exception(f"Syntax Error: {e}")

def Infix_To_Prefix(expr: str, replace_eq = False):
    if expr:
        tree = Construct_AST(expr, replace_eq)
        if tree:
            converter = PrefixNotationConverter()
            expr = converter.visit(tree.body)
            return expr
        else:
            return None
    else:
        return None
        
