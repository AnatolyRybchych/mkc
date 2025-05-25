from mkc.type import Type
from mkc.depends import Depends

class Typedef(Type, Depends):
    def __init__(self, type: Type, name: str):
        Type.__init__(self)
        Depends.__init__(self)
        self.name = name
        self.type = type
        self.depend_on(type)
        type.typedefs.append(self)
        if not type.first_definition:
            type.first_definition = self

    def type_name(self):
        return f'{self.name}'

    def feild_declaration(self, name):
        return f'{self.name} {name}'

    def __str__(self):
        if self.typedefs and self.type.first_definition is not self or self.type.annonymous:
            return f'typedef {self.type.full_field_declaration(self.type_name())}'
        else:
            return f'typedef {self.type.feild_declaration(self.type_name())}'