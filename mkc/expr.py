
import math

class Expr:
    def __init__(self):
        self.precedence = math.inf

    def get_childs(self) -> list:
        raise Exception(f'{type(self)}.get_childs() -> list[Expr] is not implemented')

    def assign(self, expr):
        from mkc.operations import Assign

        if isinstance(expr, Expr):
            return Assign(self, expr)
        else:
            from mkc.operations import Literal
            return Assign(self, Literal(expr))

    def __getitem__(self, key):
        from mkc.operations import Subscript
        from mkc.operations import GetField
        from mkc.operations import Literal

        if isinstance(key, Expr):
            return Subscript(self, key)
        elif type(key) is int:
            return Subscript(self, Literal(key))
        elif type(key) is str:
            return GetField(self, key)
        else:
            raise Exception(f'{type(key)} is not a propper selector')

    def __str__(self) -> str:
        raise Exception(f'{type(self)}.__str__() is not implemented')