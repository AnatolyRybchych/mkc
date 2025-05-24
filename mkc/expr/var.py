from mkc.expr import Expr
from mkc.consturction.decl_var import DeclVar

class Var(Expr):
    def __init__(self, decl: DeclVar):
        super().__init__()
        self.decl = decl

    def gen(self):
        return f'{self.decl.name}'