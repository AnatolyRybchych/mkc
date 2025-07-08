from mkc.expr import Expr
from mkc.type import Type

class UnOp(Expr):
    def __init__(self, expr: Expr, operation_fmt: str, precedence: int):
        super().__init__(tuple(([expr])))
        self.precedence = precedence
        self.operation_fmt = operation_fmt

    def __str__(self):
        res = f'({self.childs[0]})' if self.childs[0].precedence > self.precedence else f'{self.childs[0]}'
        return self.operation_fmt.format(res)

class BinOp(Expr):
    def __init__(self, lhs: Expr, rhs:Expr, operation_sign: str, precedence: int):
        super().__init__((lhs, rhs))
        self.precedence = precedence
        self.operation_sign = operation_sign

    def __str__(self):
        res = f'({self.childs[0]})' if self.childs[0].precedence > self.precedence else f'{self.childs[0]}'
        res += f'{self.operation_sign}'
        res += f'({self.childs[1]})' if self.childs[1].precedence > self.precedence else f'{self.childs[1]}'
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

class Equals(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '==', 6)

class And(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '&&', 11)

class Not(UnOp):
    def __init__(self, expr):
        super().__init__(expr, '!{}', 2)

class SizeOf(UnOp):
    def __init__(self, expr):
        super().__init__(expr, 'sizeof {}', 2)

class Or(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '||', 12)

class NotEquals(BinOp):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs, '!=', 6)

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
        super().__init__((lhs))
        self.field = field
        self.precedence = 1

    def __str__(self):
        if self.childs[0].precedence > self.precedence:
            return f'({self.childs[0]}).{self.field}'
        else:
            return f'{self.childs[0]}.{self.field}'

class Call(Expr):
    def __init__(self, callable: Expr, *args: Expr):
        super().__init__((callable, *args))
        self.precedence = 1

    def __str__(self):
        if self.childs[0].precedence > self.precedence:
            res = f'({self.childs[0]})'
        else:
            res = f'{self.childs[0]}'

        return f'{res}({','.join(f'{c}' for c in self.childs[1:])})'

class Ref(Expr):
    def __init__(self, expr: Expr):
        super().__init__((callable, *expr))
        self.precedence = 2
        self.expr = expr

    def __str__(self):
        if self.expr.precedence > self.precedence:
            return f'&({self.expr})'
        else:
            return f'&{self.expr}'

class Deref(Expr):
    def __init__(self, expr: Expr):
        super().__init__((expr))
        self.precedence = 2
        self.expr = expr

    def __str__(self):
        if self.expr.precedence > self.precedence:
            return f'*({self.expr})'
        else:
            return f'*{self.expr}'

class Nop(Expr):
    def __init__(self):
        super().__init__(())
    
    def __str__(self):
        return ''

class Subscript(Expr):
    def __init__(self, expr: Expr, field: Expr):
        super().__init__(tuple([expr]))
        self.field = field
        self.precedence = 1

    def __str__(self) -> str:
        return f'({self.childs[0]})[{self.field}]'

class Literal(Expr):
    def __init__(self, value: int | str, flavour = 'default'):
        super().__init__(())
        self.value = value
        self.precedence = 1
        self.flavour = flavour

    def is_literal(target):
        if type(target) in [int, str]:
            return True

        return False

    def expr_or_literal(target) -> Expr:
        if Literal.is_literal(target):
            return Literal(target)
        elif isinstance(target, Expr):
            return target
        else:
            raise Exception(f'The {type(target)} is neither a literal or expresson')

    def escape_string(text: str) -> str:
        ESC = {
            '\\': '\\\\',
            '\n': '\\n',
            '\t': '\\t',
            '\'': '\\\'',
            '\"': '\\\"',
        }

        res = ''
        for ch in text:
            if ch in ESC:
                res += ESC[ch]
            elif ch.isprintable():
                res += ch
            else:
                b = bytes(ch, 'utf-8')
                assert len(b) == 1
                res += f'\\x{hex(b[0])[2:]}'
        
        return res

    def __str__(self):
        if self.flavour == 'char':
            if type(self.value) is int:
                if self.value < 128:
                    value = f'{Literal.escape_string(str(bytes([self.value]), encoding='ascii'))}'
                else:
                    value = f'\\x{hex(self.value)[2:]}'
            else:
                value = self.value

            return f"'{value}'"

        if type(self.value) is str:
            return f'"{Literal.escape_string(self.value)}"'

        return f'{self.value}'

class Initializer(Expr):
    def __init__(self, init_type: Type, initializer = None):
        def initializer_expressions(initializer) -> tuple:
            if isinstance(initializer, Expr):
                return (initializer)
            elif type(initializer) is list:
                return tuple([i if isinstance(i, Expr) else Initializer(i) for i in initializer])
            elif type(initializer) is dict:
                return tuple([i if isinstance(i, Expr) else Initializer(i) for i in initializer.values()])
            else:
                raise Exception(f'Unexpected initializer type {type(initializer)}')

        super().__init__(initializer_expressions(initializer))

        self.type = init_type
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
        super().__init__(())

        assert isinstance(decl, DeclVar)

        self.decl: DeclVar = decl
        self.precedence = 1

    def __str__(self):
        return f'{self.decl.name}'

class Fn(Expr):
    def __init__(self, name: str):
        super().__init__(())
        self.name = name
        self.precedence = 1

    def __str__(self):
        return f'{self.name}'

