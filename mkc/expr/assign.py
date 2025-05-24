from mkc.expr import Expr

class Assign(Expr):
    def __init__(self, lhs: Expr, rhs: Expr):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs

    def gen(self) -> str:
        return f'({self.lhs.gen()}) = ({self.rhs.gen()})'
