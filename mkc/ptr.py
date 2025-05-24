
from mkc.type import Type

class Ptr(Type):
    def __init__(self, type: Type):
        super().__init__(f'{type.typename}*')
        self.type = type
