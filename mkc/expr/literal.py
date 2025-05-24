from mkc.expr import Expr

class Literal(Expr):
    def __init__(self, value: tuple[int]):
        super().__init__()
        assert type(value) in [int]
        self.value = value

    def gen(self):
        return f'{self.value}'