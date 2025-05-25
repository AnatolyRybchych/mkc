
from mkc.struct import Struct
from mkc.typedef import Typedef
from mkc.func_decl import FuncDecl
from mkc.func import Func
from mkc.type import Type
from mkc.enum import Enum

class File:
    def __init__(self, path: str, translation_unit):
        from mkc.translation_unit import TranslationUnit

        self.path = path
        self.typedefs: list[Typedef] = []
        self.structs: list[Struct] = []
        self.func_decls: list[FuncDecl] = []
        self.funcs: list[Func] = []
        self.enums: list[Enum] = []
        self.translation_unit: TranslationUnit = translation_unit

    def struct(self, name: str, **fields: Type) -> Struct:
        new_struct = Struct(name, self)
        for name, type in fields.items():
            new_struct.add_field(type, name)

        self.declare(new_struct)
        return new_struct
    
    def enum(self, name: str, *fields: tuple[str, int] | str) -> Typedef:
        new_enum = Enum('', self, *fields).typedef(name)
        self.declare(new_enum)
        return new_enum

    def func(self, ret: Type, name: str, *args: tuple[Type, str]) -> Func:
        new_func = Func(self, ret, name, *args)
        self.declare(new_func)
        return new_func

    def declare(self, target):
        # TODO: check duplicate declarations

        if type(target) is Struct:
            self.structs.append(target)
        elif type(target) is Typedef:
            self.typedefs.append(target)
        elif type(target) is FuncDecl:
            self.func_decls.append(target)
        elif type(target) is Func:
            self.funcs.append(target)
        elif type(target) is Enum:
            self.enums.append(target)
        else:
            raise Exception(f'the costruction of type {type(target)} is not ment to be declared')

        return target

    def __str__(self):
        # TODO: reorder accrding to dependencies
        res = []

        def cat(var):
            nonlocal res
            res += [var]
            if '{' in var:
                res += ['']

        for typedef in self.typedefs:
            cat(f'{typedef};')

        for enum in self.enums:
            cat(f'{enum};')

        for struct in self.structs:
            cat(f'{struct};')

        for func_decl in self.func_decls:
            cat(f'{func_decl};')

        if self.func_decls and self.funcs:
            cat('')

        for func in self.funcs:
            cat(f'{func}')

        return '\n'.join(res)