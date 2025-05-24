
from mkc.type import Type
from mkc.depends import Depends

class Struct(Type, Depends):
    def __init__(self, name: str):
        Type.__init__(self)
        Depends.__init__(self)
        self.name = name
        self.fields: list[tuple[Type, str]] = []

    def add_field(self, type: Type, name: str):
        is_duplicate = any(field_name == name for _, field_name in self.fields)
        assert not is_duplicate

        self.depend_on(type)
        self.fields.append((type, name))

    def type_name(self):
        return f'struct {self.name}'
    
    def feild_declaration(self, name):
        return f'struct {self.name} {name}'

    def __str__(self) -> str:
        return f'struct {self.type_name()}''{' + ''.join(f'{type.feild_declaration(name)};' for type, name in self.fields) + '}'
