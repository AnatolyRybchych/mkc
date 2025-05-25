from mkc.consturction import Construction
from mkc.type import Type
from mkc.expr import Expr
from mkc.operations import Nop

class DeclVar(Construction):
    def __init__(self, type: Type, name: str, expr: Expr = Nop()):
        super().__init__()
        self.type = type
        self.name = name
        self.expr = expr

    def __str__(self) -> str:
        res = self.type.feild_declaration(self.name)
        if not isinstance(self.expr, Nop):
            res += f'={self.expr}'
        res += ';'

        return  res

    def var(self):
        from mkc.operations import Var
        return Var(self)

