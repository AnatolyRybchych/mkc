
from mkc.consturction import Construction
from mkc.expr import Expr
from mkc.expr.nop import Nop

class Ret(Construction):
    def __init__(self, expr: Expr = Nop()):
        super().__init__()
        self.expr = expr

    def gen(self) -> str:
        return f'return {self.expr.gen()}'