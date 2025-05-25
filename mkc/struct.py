
from mkc.type import Type
from mkc.depends import Depends
from mkc.scope import Scope

class Struct(Type, Scope, Depends):
    def __init__(self, name: str, parent):
        Type.__init__(self)
        Scope.__init__(self, Scope.LEVEL_BLOCK, parent)
        Depends.__init__(self)

        self.name = name
        self.fields: list[tuple[Type, str]] = []
        self.annonymous = not name

    def add_field(self, type: Type, name: str):
        is_duplicate = any(field_name == name for _, field_name in self.fields)
        assert not is_duplicate

        self.depend_on(type)
        self.fields.append((type, name))

    def type_name(self):
        if not self.name:
            raise Exception(f'The type of unnamed struct is not accessible')
        else:
            return f'struct {self.name}'
    
    def feild_declaration(self, name):
        if not self.name:
            raise Exception(f'The type of unnamed struct is not accessible')
        else:
            return f'struct {self.name} {name}'

    def full_field_declaration(self, name):
        return f'{self} {name}'

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
        return f'struct {self.name}' + '{' + ''.join(f'{type.full_field_declaration(name)};' for type, name in self.fields) + '}'
