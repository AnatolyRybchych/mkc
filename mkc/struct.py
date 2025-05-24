
from mkc.type import Type

class Struct(Type):
    def __init__(self, name: str):
        super().__init__(f'struct {name}')
        self.fields: list[tuple[Type, str]] = []

    def add_field(self, type: Type, name: str):
        is_duplicate = any(typename == name for typename, _ in self.fields)
        assert not is_duplicate

        self.fields.append((type, name))

    def __str__(self) -> str:
        return f'struct {self.typename}''{' + ';'.join(f'{type.typename} {name}' for type, name in self.fields) + '}'
