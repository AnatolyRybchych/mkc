

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
        from mkc.construction import DeclVar
        from mkc.type import Struct

        self.scope_level: str = scope_level
        self.parent_scope: Scope | None = parent
        self.scope_variables:dict[str, DeclVar] = {}
        self.scope_types:dict[str, Struct] = {}
        self.scope_shared_with: list[Scope] = []

    def get_scope_level(self) -> int:
        return self.SCOPE_LEVEL[self.scope_level]

    def scope_link(self, scope):
        assert isinstance(scope, Scope)
        assert scope.scope_level == self.scope_level

        self.scope_shared_with.append(scope)
        scope.scope_shared_with.append(self)

    def __getitem__(self, name: str):
        return self.find_var(name)

    def find_var(self, name: str):
        from mkc.operations import Var

        for scope_variables in self.all_in_all_scopes(lambda scope: scope.scope_variables):
            if name in scope_variables:
                return Var(scope_variables[name])

        if self.parent_scope is not None:
            return self.parent_scope.find_var(name)
        else:
            return None

    def scope_set_var(self, decl):
        from mkc.construction import DeclVar

        assert isinstance(decl, DeclVar)
        if decl.name in self.scope_variables:
            raise Exception(f'The variable {decl} is aready in the {self.scope_level} scope')

        self.scope_variables[decl.name] = decl

    def func(self, ret, name: str, *args):
        from mkc.func import Func
        from mkc.construction import DeclVar

        if name in self.scope_variables:
            raise Exception(f'The variable {name} is aready in the {self.scope_level} scope')

        new_func = Func(self, ret, name, *args)
        self.scope_variables[name] = new_func.decl_var
        return new_func

    def struct(self, name: str, **fields):
        from mkc.type import Struct

        if name and name in self.scope_types:
            raise Exception(f'type {name} is already defined in scope of this {self.scope_level}')

        new_struct = Struct(name, self)
        for struct_name, type in fields.items():
            new_struct.add_field(type, struct_name)

        if name:
            self.scope_types[name] = new_struct

        return new_struct

    def enum(self, name: str, *fields: tuple[str, int] | str):
        from mkc.type import Enum

        if name and name in self.scope_types:
            raise Exception(f'type {name} is already defined in scope of this {self.scope_level}')

        enum =  Enum('', self, *fields).typedef(name)
        self.scope_types[name] = enum

        return enum

    def all_in_all_scopes(self, select_field):
        yield select_field(self)

        visited = set()
        unresolved: list[Scope] = [self]
        while len(unresolved) != 0:
            scope = unresolved.pop()

            yield select_field(scope)

            for shared in scope.scope_shared_with:
                if id(shared) not in visited:
                    visited.add(id(shared))
                    unresolved.append(shared)

    def find_type(self, name: str):
        for scope_types in self.all_in_all_scopes(lambda scope: scope.scope_types):
            if name in scope_types:
                return scope_types[name]

        if self.parent_scope is not None:
            return self.parent_scope.find_type(name)
        else:
            return None
