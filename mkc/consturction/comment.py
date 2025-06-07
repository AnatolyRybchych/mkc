
from mkc.consturction import Construction
from mkc.expr import Expr
from mkc.operations import Nop

class Comment(Construction):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return f'// {self.text}\n'
