from mkc.type import Type

class Const(Type):
    def __init__(self, type: Type):
        super().__init__()
        self.type = type

    def type_name(self):
        from mkc.ptr import Ptr
        if isinstance(self.type, Ptr):
            return f'{self.type.type_name()} const'
        else:
            return f'const {self.type.type_name()}'

    def feild_declaration(self, name):
        from mkc.ptr import Ptr
        if isinstance(self.type, Ptr):
            return f'{self.type.feild_declaration(f'const {name}')}'
        else:
            return f'const {self.type.feild_declaration(name)}'
