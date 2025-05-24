from mkc.type import Type
from mkc.depends import Depends

class Typedef(Type, Depends):
    def __init__(self, type: Type, name: str):
        Type.__init__(self, name)
        Depends.__init__(self)
        self.type = type
        self.depend_on(type)
        type.typedefs.append(self)

    def __str__(self):
        return f'typedef {self.type.typename} {self.typename}'