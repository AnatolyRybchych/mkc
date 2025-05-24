
from mkc.type import Type

class Ptr(Type):
    def __init__(self, type: Type):
        super().__init__()
        self.type = type

    def type_name(self):
        return f'{self.type.type_name()}*'

    def feild_declaration(self, name):
        return f'{self.type.type_name()} *{name}'

