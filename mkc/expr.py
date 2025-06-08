
import math

class Expr:
    def __init__(self, childs: tuple):
        self.precedence = math.inf
        self.childs = childs

    def get_childs(self) -> list:
        raise Exception(f'{type(self)}.get_childs() -> list[Expr] is not implemented')

    def assign(self, expr):
        from mkc.operations import Assign

        if isinstance(expr, Expr):
            return Assign(self, expr)
        else:
            from mkc.operations import Literal
            return Assign(self, Literal(expr))

    def ref(self):
        from mkc.operations import Ref
        return Ref(self)

    def deref(self):
        from mkc.operations import Deref
        return Deref(self)

    def __add__(self, rhs):
        from mkc.operations import Add
        from mkc.operations import Literal
        return Add(self, Literal.expr_or_literal(rhs))

    def __sub__(self, rhs):
        from mkc.operations import Sub
        from mkc.operations import Literal
        return Sub(self, Literal.expr_or_literal(rhs))

    def __mul__(self, rhs):
        from mkc.operations import Mul
        from mkc.operations import Literal
        return Mul(self, Literal.expr_or_literal(rhs))

    def __div__(self, rhs):
        from mkc.operations import Div
        from mkc.operations import Literal
        return Div(self, Literal.expr_or_literal(rhs))

    def __mod__(self, rhs):
        from mkc.operations import Mod
        from mkc.operations import Literal
        return Mod(self, Literal.expr_or_literal(rhs))

    def __call__(self, *args):
        from mkc.operations import Call
        from mkc.operations import Literal
        return Call(self, *(Literal.expr_or_literal(arg) for arg in args))

    def __gt__(self, rhs):
        from mkc.operations import Literal, GreaterThen
        return GreaterThen(self, Literal.expr_or_literal(rhs))

    def __lt__(self, rhs):
        from mkc.operations import Literal, LessThan
        return LessThan(self, Literal.expr_or_literal(rhs))

    def __eq__(self, rhs):
        from mkc.operations import Literal, Equals
        return Equals(self, Literal.expr_or_literal(rhs))

    def __ne__(self, rhs):
        from mkc.operations import Literal, NotEquals
        return NotEquals(self, Literal.expr_or_literal(rhs))

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
