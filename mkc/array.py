from mkc.type import Type
from mkc.func_type import FuncType
from mkc.ptr import Ptr

class Array(Type):
    def __init__(self, type: Type, cnt: int = 0):
        super().__init__()
        self.type: Type = type
        self.cnt = cnt

    def is_flexible_array(self) -> bool:
        return self.cnt == 0

    def feild_declaration(self, name):
        return self.type.feild_declaration(f'{name}[{self.cnt or ''}]')
