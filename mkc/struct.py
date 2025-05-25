
from mkc.type import Type
from mkc.depends import Depends

class Struct(Type, Depends):
    def __init__(self, name: str, file = None):
        from mkc.file import File

        Type.__init__(self)
        Depends.__init__(self)
        self.name = name
        self.fields: list[tuple[Type, str]] = []
        self.file: File | None = file

    def add_field(self, type: Type, name: str):
        is_duplicate = any(field_name == name for _, field_name in self.fields)
        assert not is_duplicate

        self.depend_on(type)
        self.fields.append((type, name))

    def type_name(self):
        return f'struct {self.name}'
    
    def feild_declaration(self, name):
        return f'struct {self.name} {name}'

    def get_fields(self) -> list[str]:
        return [name for type, name in self.fields]

    def typedef(self, name: str | None = None):
        from mkc.typedef import Typedef
        return Typedef(self, name or self.name)

    def get_field_type(self, field: str) -> Type:
        for type, name in self.fields:
            if name == field:
                return type
        
        raise Exception(f'{self.type_name()} does not have a field "{field}"')

    def __str__(self) -> str:
        return f'{self.type_name()}''{' + ''.join(f'{type.feild_declaration(name)};' for type, name in self.fields) + '}'
