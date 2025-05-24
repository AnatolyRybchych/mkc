from mkc.consturction import Construction
from mkc.consturction.decl_var import DeclVar
from mkc.consturction.line import Line
from mkc.expr import Expr
from mkc.expr.nop import Nop
from mkc.type import Type

class Block(Construction):
    def __init__(self):
        super().__init__()
        self.lines: list[Construction] = []

    def add_line(self, line: Expr | Construction) -> Construction:
        if isinstance(line, Expr):
            line = Line(line)
            self.lines.append(line)
        elif isinstance(line, Construction):
            self.lines.append(line)
        else:
            raise Exception(f'{type(line)} is neither a construction or expression')

        return line

    def declare(self, type: Type, name: str, expr: Expr = Nop()) -> DeclVar:
        var = DeclVar(type, name, expr)
        self.add_line(var)
        return var

    def gen(self) -> str:
        return '{' + ''.join(f'{line.gen()}' for line in self.lines) + '}'
