from mkc.consturction import Construction
from mkc.consturction.decl_var import DeclVar
from mkc.consturction.line import Line
from mkc.expr import Expr
from mkc.operations import Nop, Var
from mkc.type import Type
from mkc.scope import Scope

class Block(Construction, Scope):
    def __init__(self, parent):
        Construction.__init__(self)
        Scope.__init__(self, Scope.LEVEL_BLOCK, parent)

        self.lines: list[Construction] = []

    def add_line(self, line: Expr | Construction) -> Construction:
        if isinstance(line, Expr):
            line = Line(line)
            self.lines.append(line)
        elif isinstance(line, Construction):
            if isinstance(line, DeclVar):
                self.scope_set_var(line)

            self.lines.append(line)
        else:
            raise Exception(f'{type(line)} is neither a construction or expression')

        return line

    def declare(self, type: Type, name: str, expr: Expr = Nop()) -> DeclVar:
        var = DeclVar(type, name, expr)
        self.add_line(var)
        return var

    def __str__(self) -> str:
        return '{' + ''.join(f'{line}' for line in self.lines) + '}'
