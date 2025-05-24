from mkc.type import Type

class Typedef(Type):
    def __init__(self, type: Type, name: str):
        super().__init__(name)
        self.type = type
        type.typedefs.append(self)

    def __str__(self):
        return f'typedef {self.type.typename} {self.typename}'