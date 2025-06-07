
from mkc.consturction import Construction
from mkc.expr import Expr
from mkc.operations import Nop

class Ret(Construction):
    def __init__(self, expr: Expr = Nop()):
        super().__init__()
        self.expr = expr

    def __str__(self) -> str:
        return f'return {self.expr};'