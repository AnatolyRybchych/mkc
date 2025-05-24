from mkc.expr import Expr

from mkc.type import Type

class Subscript(Expr):
    def __init__(self, expr: Expr, field: Expr):
        super().__init__()
        self.expr = expr
        self.field = field

    def gen(self) -> str:
        return f'({self.expr.gen()})[{self.field.gen()}]'
