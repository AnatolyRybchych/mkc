
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
        from mkc.expr.get_field import GetField
        from mkc.expr.literal import Literal

        if isinstance(key, Expr):
            return Subscript(self, key)
        elif type(key) is int:
            return Subscript(self, Literal(key))
        elif type(key) is str:
            return GetField(self, key)
        else:
            raise Exception(f'{type(key)} is not a propper selector')

    def gen(self) -> str:
        raise Exception(f'{type(self)}.gen() is not implemented')