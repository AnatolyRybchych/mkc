from mkc.type import Type, field_decl
from mkc.func_type import FuncType

class FuncDecl:
    def __init__(self, ret: Type, name, *args: tuple[Type, str]):
        super().__init__()
        self.func_type = FuncType(ret, *args)
        self.name: str = name

    def __str__(self):
        return self.func_type.feild_declaration(self.name)

