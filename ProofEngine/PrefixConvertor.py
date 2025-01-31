import ast

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
            ast.Div: '/',
            ast.Gt: '>',
            ast.Lt: '<',
            ast.GtE: '>=',
            ast.LtE: '<=',
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Mod: '%',
            ast.And: 'and',
            ast.Or: 'or',
            ast.Not: '~',
        }
        return operators[type(op)]

def Construct_AST(expr: str):
    try:
        tree = ast.parse(expr, mode='eval')
        return tree
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return None

def Infix_To_Prefix(expr: str):
    if expr:
        tree = Construct_AST(expr)
        if tree:
            converter = PrefixNotationConverter()
            expr = converter.visit(tree.body)
            return expr
        else:
            return None
    else:
        return None
        
