
from mkc.consturction import Construction, as_construction
from mkc.consturction.block import Block
from mkc.expr import Expr
from mkc.operations import Nop

class For(Construction):
    def __init__(self, parent_block: Block, init: Construction | Expr | None, condition: Expr, increment: Expr):
        super().__init__()

        self.parent_block = parent_block
        self.init: Construction = as_construction(init)
        self.condition: Expr = condition
        self.increment: Expr = increment
        self.body: Block = Block(parent_block)

    def __str__(self) -> str:
        return f'for ({self.init} {self.condition};{self.increment}){self.body}'
