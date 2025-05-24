
from mkc.func_type import FuncType
from mkc.func_decl import FuncDecl
from mkc.type import Type
from mkc.block import Block

class Func:
    def __init__(self, ret: Type, name, *args: tuple[Type, str]):
        super().__init__()
        self.func_type = FuncType(ret, *args)
        self.name: str = name
        self.body = Block()

    def func_decl(self) -> FuncDecl:
        return FuncDecl(self.func_type, self.name)

    def __str__(self):
        return f'{self.func_type.feild_declaration(self.name)} {self.body}'
