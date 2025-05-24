from mkc.consturction import Construction
from mkc.expr import Expr

class Line(Construction):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

    def gen(self) -> str:
        return f'{self.expr.gen()};'