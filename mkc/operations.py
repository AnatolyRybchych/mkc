from mkc.expr import Expr
from mkc.type import Type

class BinOp(Expr):
    def __init__(self, lhs: Expr, rhs:Expr, operation_sign: str, precedence: int):
        super().__init__()
        self.precedence = precedence
        self.operation_sign = operation_sign
        self.lhs = lhs
        self.rhs = rhs

    def get_childs(self):
        return [self.lhs, self.rhs]

    def __str__(self):
        res = f'({self.lhs})' if self.lhs.precedence > self.precedence else f'{self.lhs}'
        res += f'{self.operation_sign}'
        res += f'({self.rhs})' if self.rhs.precedence > self.precedence else f'{self.rhs}'
        return res

class Assign(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '=', 14)

class LessThan(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '<', 6)

class GreaterThen(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '>', 6)

class LessOrEqual(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '<=', 6)

class GreaterOrEquals(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '>=', 6)

class Shl(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '<<', 5)

class Shr(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '>>', 5)

class Add(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '+', 4)

class Sub(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '-', 4)

class Mul(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '*', 3)

class Div(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '/', 3)

class Mod(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '%', 3)

class GetField(Expr):
    def __init__(self, lhs: Expr, field: str):
        super().__init__()
        self.lhs = lhs
        self.field = field
        self.precedence = 1

    def __str__(self):
        return f'({self.lhs}).{self.field}'

class Nop(Expr):
    def __init__(self):
        super().__init__()

class Subscript(Expr):
    def __init__(self, expr: Expr, field: Expr):
        super().__init__()
        self.expr = expr
        self.field = field
        self.precedence = 1

    def __str__(self) -> str:
        return f'({self.expr})[{self.field}]'

class Literal(Expr):
    def __init__(self, value: tuple[int]):
        super().__init__()
        assert type(value) in [int]
        self.value = value
        self.precedence = 1

    def __str__(self):
        return f'{self.value}'

class Initializer(Expr):
    def __init__(self, type: Type, initializer = None):
        super().__init__()
        self.type = type
        self.initializer = initializer
        self.precedence = 2

    def __str__(self):
        if not self.initializer:
            return f'({self.type.type_name()})' '{0}'

        if self.type.get_struct():
            t = self.type.get_struct()
            fields = t.get_fields()
            assert type(self.initializer) is dict

            initializers = []
            for field, expr in self.initializer.items():
                if type(expr) is int:
                    expr = Literal(expr)

                if field not in fields:
                    raise Exception(f'{t.type_name()} does not have a field "{field}"')

                if type(expr) is dict:
                    initializers += [f'.{field} = {Initializer(t.get_field_type(field), expr)},']
                else:
                    initializers += [f'.{field} = {expr},']

            return f'({t.type_name()})' + '{' + ''.join(initializers) + '}'

        raise Exception(f'Could not have an initializer for {self.type.type_name()}')

class Var(Expr):
    def __init__(self, decl):
        from mkc.consturction.decl_var import DeclVar
        super().__init__()
        self.decl: DeclVar = decl
        self.precedence = 1

    def __str__(self):
        return f'{self.decl.name}'