from mkc.type import Type, field_decl
from mkc.func_type import FuncType

class FuncDecl:
    def __init__(self, ret: Type, name, *args: tuple[Type, str]):
        super().__init__()
        self.func_type = FuncType(ret, *args)
        self.name: str = name

    def __str__(self):
        return f'{self.func_type.ret_type.type_name()} {self.name}({','.join(f'{field_decl(arg)}' for arg in self.func_type.args)})'
