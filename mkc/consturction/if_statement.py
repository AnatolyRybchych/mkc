
from mkc.consturction import Construction, as_construction
from mkc.expr import Expr
from mkc.operations import Nop

class If(Construction):
    def __init__(self, parent_block, condition: Expr, then: Construction| Expr | None = None, otherwice: Construction | Expr | None = None):
        super().__init__()

        self.parent_block = parent_block
        self.condition: Expr = condition
        self.then: Construction = as_construction(then)

        self.otherwice: Construction | None = None

        if otherwice is not None:
            self.otherwice = as_construction(otherwice)

    def __str__(self) -> str:
        from mkc.consturction.block import Block
        from mkc.consturction.line import Line

        then = self.then
        if not isinstance(then, Block):
            then = Block(self.parent_block)
            then.add_line(self.then)

        result = f'if ({self.condition}) {then}'
        if self.otherwice:
            result += f'else {self.otherwice}'

        return result