
from mkc.type import Type, field_decl

class FuncType(Type):
    def __init__(self, ret_type: Type, *args: tuple[Type, str] | Type):
        super().__init__()
        self.ret_type = ret_type
        self.args: list[tuple[Type, str] | Type] = list(args)

    def type_name(self):
        return f'{self.ret_type.type_name()}({','.join(f'{field_decl(arg)}' for arg in self.args)})'

    def feild_declaration(self, name):
        return f'{self.ret_type.type_name()} {name}({','.join(f'{field_decl(arg)}' for arg in self.args)})'
