from mkc.expr import Expr
from mkc.expr.literal import Literal
from mkc.type import Type
from mkc.struct import Struct

class Initializer(Expr):
    def __init__(self, type: Type, initializer = None):
        super().__init__()
        self.type = type
        self.initializer = initializer

    def gen(self):
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
                    initializers += [f'.{field} = {Initializer(t.get_field_type(field), expr).gen()},']
                else:
                    initializers += [f'.{field} = {expr.gen()},']

            return f'({t.type_name()})' + '{' + ''.join(initializers) + '}'

        raise Exception(f'Could not have an initializer for {self.type.type_name()}')


