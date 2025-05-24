
class Expr:
    def __init__(self):
        pass

    def assign(self, expr):
        from mkc.expr.assign import Assign

        if isinstance(expr, Expr):
            return Assign(self, expr)
        else:
            from mkc.expr.literal import Literal
            return Assign(self, Literal(expr))

    def __getitem__(self, key):
        from mkc.expr.subscript import Subscript

        if isinstance(key, Expr):
            return Subscript(self, key)
        else:
            from mkc.expr.literal import Literal
            return Subscript(self, Literal(key))

    def gen(self) -> str:
        raise Exception(f'{type(self)}.gen() is not implemented')