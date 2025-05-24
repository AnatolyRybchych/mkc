from mkc.expr import Expr

class GetField(Expr):
    def __init__(self, lhs: Expr, field: str):
        super().__init__()
        self.lhs = lhs
        self.field = field

    def gen(self):
        return f'({self.lhs.gen()}).{self.field}'
