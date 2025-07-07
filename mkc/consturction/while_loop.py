
from mkc.consturction import Construction, as_construction
from mkc.consturction.block import Block
from mkc.expr import Expr
from mkc.operations import Nop

class While(Construction):
    def __init__(self, parent_block: Block, condition: Expr):
        super().__init__()

        self.parent_block = parent_block
        self.condition: Expr = condition
        self.body: Block = Block(parent_block)

    def __str__(self) -> str:
        return f'while ({self.condition}){self.body}'
