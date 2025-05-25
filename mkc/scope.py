

class Scope:
    LEVEL_TOP: str = 'top'
    LEVEL_TRANS: str = 'trans'
    LEVEL_BLOCK: str = 'block'

    SCOPE_LEVEL: dict[str: int] = {
        LEVEL_BLOCK: 1,
        LEVEL_TRANS: 2,
        LEVEL_TOP: 3,
    }

    def __init__(self, scope_level: str, parent = None):
        from mkc.consturction.decl_var import DeclVar
        from mkc.struct import Struct

        self.scope_level: str = scope_level
        self.parent_scope: Scope | None = parent
        self.scope_variables:dict[str, DeclVar] = {}
        self.scope_types:dict[str, Struct] = {}

    def get_scope_level(self) -> int:
        return self.SCOPE_LEVEL[self.scope_level]

    def __getitem__(self, name: str):
        return self.find_var(name)

    def find_var(self, name: str):
        if name in self.scope_variables:
            return self.scope_variables[name].var()
        elif self.parent_scope is not None:
            return self.parent_scope.find_var(name)
        else:
            return None

    def scope_set_var(self, decl):
        from mkc.consturction.decl_var import DeclVar

        assert isinstance(decl, DeclVar)
        if decl.name in self.scope_variables:
            raise Exception(f'The variable {decl} is aready in the {self.scope_level} scope')

        self.scope_variables[decl.name] = decl

    def struct(self, name: str, **fields):
        from mkc.struct import Struct

        if name and name in self.scope_types:
            raise Exception(f'struct {name} is already defined in scope of this {self.scope_level}')

        new_struct = Struct(name, self)
        for name, type in fields.items():
            new_struct.add_field(type, name)

        if name:
            self.scope_types[name] = new_struct

        return new_struct

    def find_struct(self, name: str):
        if name in self.scope_types:
            return self.scope_types[name]
        elif self.parent_scope is not None:
            return self.parent_scope.find_struct(name)
        else:
            return None