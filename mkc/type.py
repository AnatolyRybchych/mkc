from mkc.scope import Scope

import copy

class Depends:
    def __init__(self):
        self.dependencies: dict[int] = {}

    def get_recursive_dependencies(self) -> list[list]:
        def step(dependency, visited: set) -> list[list]:
            visited = copy.deepcopy(visited)
            if id(dependency) in visited:
                return [[dependency]]

            visited.add(id(dependency))
            recursive = []
            if isinstance(dependency, Depends):
                for subsequesnt in dependency.dependencies.values():
                    recursive += step(subsequesnt, visited)

            for trace in recursive:
                trace.insert(0, dependency)

            return recursive

        return step(self, set())

    def depend_on(self, dependency):
        self.dependencies[id(dependency)] = dependency
        assert len(self.get_recursive_dependencies()) == 0


class Type:
    def __init__(self):
        self.typedefs = []
        self.first_definition = None
        self.annonymous = False

    def type_name(self) -> str:
        raise Exception(f'{type(self)}.type_name() is not defined')

    def feild_declaration(self, name: str) -> str:
        raise Exception(f'{type(self)}.feild_declaration({name}) is not defined')
    
    def full_field_declaration(self, name: str) -> str:
        return self.feild_declaration(name)

    def ptr(self):
        return Ptr(self)

    def typedef(self, name: str):
        return Typedef(self, name)
    
    def const(self):
        if isinstance(self, Const):
            return self
        else:
            return Const(self)

    def get_origin(self, discard = ['typedef', 'ptr', 'array', 'const']):
        if 'typedef' in discard and isinstance(self, Typedef):
            return self.type.get_origin(discard)

        if 'ptr' in discard and isinstance(self, Ptr):
            return self.type.get_origin(discard)

        if 'array' in discard and isinstance(self, Array):
            return self.type.get_origin(discard)

        if 'const' in discard and isinstance(self, Const):
            return self.type.get_origin(discard)

        return self

def field_decl(target: tuple[Type, str] | Type) -> str:
    if type(target) is Type:
        return target.type_name()
    else:
        return target[0].feild_declaration(target[1])

class BaseType(Type):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def type_name(self) -> str:
        return self.name
    
    def feild_declaration(self, name):
        return f'{self.name} {name}'

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

    def __getitem__(self, key):
        return self.type[key]

    def type_name(self):
        return f'{self.name}'

    def feild_declaration(self, name):
        return f'{self.name} {name}'

    def __str__(self):
        if self.typedefs and self.type.first_definition is not self or self.type.annonymous:
            return f'typedef {self.type.full_field_declaration(self.type_name())}'
        else:
            return f'typedef {self.type.feild_declaration(self.type_name())}'

class Union(Type, Depends):
    def __init__(self, name: str, file = None):
        from mkc.file import File

        Type.__init__(self)
        Depends.__init__(self)
        self.name = name
        self.fields: list[tuple[Type, str]] = []
        self.file: File | None = file
        self.annonymous = not name

    def add_field(self, type: Type, name: str = ''):
        is_duplicate = any(field_name == name for _, field_name in self.fields)
        assert not is_duplicate

        self.depend_on(type)
        self.fields.append((type, name))

    def type_name(self):
        if not self.name:
            raise Exception(f'The type of unnamed union is not accessible')
        else:
            return f'union {self.name}'
    
    def feild_declaration(self, name):
        if not self.name:
            raise Exception(f'The type of unnamed union is not accessible')
        else:
            return f'union {self.name} {name}'

    def full_field_declaration(self, name):
        return f'{self} {name}'

    def get_fields(self) -> list[str]:
        return [name for type, name in self.fields]

    def typedef(self, name: str | None = None):
        return Typedef(self, name or self.name)

    def get_field_type(self, field: str) -> Type:
        for type, name in self.fields:
            if name == field:
                return type
        
        raise Exception(f'{self.type_name()} does not have a field "{field}"')

    def __str__(self) -> str:
        return f'union {self.name}''{' + ''.join(f'{type.feild_declaration(name)};' for type, name in self.fields) + '}'

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
        return Typedef(self, name or self.name)

    def get_field_type(self, field: str) -> Type:
        for type, name in self.fields:
            if name == field:
                return type
        
        raise Exception(f'{self.type_name()} does not have a field "{field}"')

    def __str__(self) -> str:
        return f'struct {self.name}' + '{' + ''.join(f'{type.full_field_declaration(name)};' for type, name in self.fields) + '}'

class Ptr(Type):
    def __init__(self, type: Type):
        super().__init__()
        self.type = type

    def func_ptr_depth(self) -> int:
        if type(self.type) is FuncType:
            return 1
        elif type(self.type) is Ptr:
            return self.type.func_ptr_depth() + 1
        else:
            return 0

    def arr_ptr_depth(self) -> int:
        if type(self.type) is Array:
            return 1
        elif type(self.type) is Ptr:
            return self.type.arr_ptr_depth() + 1
        else:
            return 0

    def type_name(self):
        if self.func_ptr_depth():
            return self.type.feild_declaration(f'({'*' * (self.func_ptr_depth())})')
        elif self.arr_ptr_depth():
            return self.type.feild_declaration(f'({'*' * (self.arr_ptr_depth())})')
        else:
            return f'{self.type.type_name()}*'

    def feild_declaration(self, name):
        if self.func_ptr_depth():
            return self.type.feild_declaration(f'({'*' * self.func_ptr_depth()}{name})')
        elif self.arr_ptr_depth():
            return self.type.feild_declaration(f'({'*' * self.arr_ptr_depth()}{name})')
        else:
            return self.type.feild_declaration(f'*{name}')

class FuncType(Type):
    def __init__(self, ret_type: Type, *args: tuple[Type, str] | Type):
        super().__init__()
        self.ret_type = ret_type
        self.args: list[tuple[Type, str] | Type] = list(args)

    def feild_declaration(self, name):
        return f'{self.ret_type.type_name()} {name}({','.join(f'{field_decl(arg)}' for arg in self.args)})'

class Enum(Type):
    def __init__(self, name: str, file = None, *fields: tuple[str, int] | str):
        from mkc.file import File
        super().__init__()
        self.name: str = name
        self.file: File | None = file
        self.fields: list[tuple[str, int|None]] = []
        self.annonymous = True
        self.prefix: str = ''

        for field in fields:
            if type(field) is str:
                self.add_field(field)
            else:
                self.add_field(field[0], field[1])

    def set_prefix(self, prefix: str):
        self.prefix = prefix

    def keys(self) -> list[str]:
        return [name for name, _ in self.fields]

    def prefixed_keys(self) -> list[str]:
        return map(lambda k: f'{self.prefix}{k}', self.keys())

    def __getitem__(self, key: str):
        from mkc.construction import DeclVar
        import mkc as c

        assert key in self.keys() or f'{self.prefix}{key}' in self.keys()

        return c.Var(DeclVar(c.int, f'{self.prefix}{key}'))

    def full_field_declaration(self, name):
        return f'{self} {name}'

    def add_field(self, name: str, value: int|None = None):
        assert not any(existing_name == name for existing_name, _ in self.fields)

        if value is not None:
            existing_values = filter(lambda v: v is not None, [v for _, v in self.fields])
            assert value not in existing_values

        self.fields.append((name, value))

    def __str__(self):
        fields = [f'{name}{value and f'= {value}' or ''}' for name, value in self.fields]
        return f'enum {self.name}' + '{' + ','.join(f'{self.prefix}{field}' for field in fields) + '}'

class Const(Type):
    def __init__(self, type: Type):
        super().__init__()
        self.type = type

    def type_name(self):
        if isinstance(self.type, Ptr):
            return f'{self.type.type_name()} const'
        else:
            return f'const {self.type.type_name()}'

    def feild_declaration(self, name):
        if isinstance(self.type, Ptr):
            return f'{self.type.feild_declaration(f'const {name}')}'
        else:
            return f'const {self.type.feild_declaration(name)}'

class Array(Type):
    def __init__(self, type: Type, cnt: int = 0):
        super().__init__()
        self.type: Type = type
        self.cnt = cnt

    def is_flexible_array(self) -> bool:
        return self.cnt == 0

    def feild_declaration(self, name):
        return self.type.feild_declaration(f'{name}[{self.cnt or ''}]')

class ExternType(Type):
    def __init__(self, literal_name: str):
        super().__init__()
        self.literal_name = literal_name

    def type_name(self):
        return self.literal_name

    def feild_declaration(self, name):
        return f'{self.type_name()} {name}'
