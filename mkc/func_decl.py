from mkc.type import Type, field_decl
from mkc.func_type import FuncType

class FuncDecl:
    def __init__(self, type: FuncType, name):
        super().__init__()
        self.func_type = type
        self.name: str = name

    def __str__(self):
        return self.func_type.feild_declaration(self.name)

