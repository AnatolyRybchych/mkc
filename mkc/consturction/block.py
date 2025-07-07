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

    def add_block(self):
        from mkc.consturction.block import Block

        block = Block(self)
        self.add_line(block)
        return block

    def add_if(self, condition: Expr, then = None, otherwice = None):
        from mkc.consturction.if_statement import If

        if_statement = If(self, condition, then, otherwice)
        self.add_line(if_statement)
        return if_statement

    def add_for(self, init: Construction | Expr | None, condition: Expr, increment: Expr):
        from mkc.consturction.for_loop import For

        while_loop = For(self, init, condition, increment)
        self.add_line(while_loop)
        return while_loop

    def add_while(self, condition: Expr):
        from mkc.consturction.while_loop import While

        for_loop = While(self, condition)
        self.add_line(for_loop)
        return for_loop

    def add_switch(self, target: Expr, cases: list[tuple[Expr, Construction | Expr]] = []):
        from mkc.consturction.switch import Switch
        switch =  Switch(self, target, cases)
        self.add_line(switch)
        return switch

    def add_comment(self, text: str):
        from mkc.consturction.comment import Comment

        comment = Comment(text)
        self.add_line(comment)
        return comment

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
