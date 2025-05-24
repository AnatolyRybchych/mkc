
from mkc.type import Type
from mkc.func_type import FuncType

class Ptr(Type):
    def __init__(self, type: Type):
        super().__init__()
        self.type = type

    def func_ptr_depth(self) -> int:
        if type(self.type) is FuncType:
            return 1
        elif type(self.type) is Ptr:
            return self.type.func_ptr_depth() + 1
        else:
            return 0

    def type_name(self):
        func_ptr_depth = self.func_ptr_depth()
        if func_ptr_depth:
            return self.type.feild_declaration(f'({'*' * func_ptr_depth})')
        else:
            return f'{self.type.type_name()}*'

    def feild_declaration(self, name):
        func_ptr_depth = self.func_ptr_depth()
        if func_ptr_depth:
            return self.type.feild_declaration(f'({'*' * func_ptr_depth}{name})')
        else:
            return f'{self.type.type_name()} *{name}'

