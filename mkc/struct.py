
from mkc.type import Type
from mkc.depends import Depends

class Struct(Type, Depends):
    def __init__(self, name: str):
        Type.__init__(self, f'struct {name}')
        Depends.__init__(self)
        self.fields: list[tuple[Type, str]] = []

    def add_field(self, type: Type, name: str):
        is_duplicate = any(typename == name for typename, _ in self.fields)
        assert not is_duplicate

        self.depend_on(type)
        self.fields.append((type, name))

    def __str__(self) -> str:
        return f'struct {self.typename}''{' + ';'.join(f'{type.typename} {name}' for type, name in self.fields) + '}'
