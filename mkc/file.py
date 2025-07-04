
from mkc.struct import Struct
from mkc.typedef import Typedef
from mkc.func_decl import FuncDecl
from mkc.func import Func
from mkc.type import Type
from mkc.enum import Enum
from mkc.scope import Scope

import os 

class File:
    def __init__(self, path: str, translation_unit):
        from mkc.translation_unit import TranslationUnit


        self.include_guard = None
        self.translation_unit:TranslationUnit = translation_unit
        self.path: str = path
        self.typedefs: list[Typedef] = []
        self.structs: list[Struct] = []
        self.func_decls: list[FuncDecl] = []
        self.funcs: list[Func] = []
        self.enums: list[Enum] = []

        self.includes: list[File] = []

    def include_file(self, file):
        assert isinstance(file, File)

        self.translation_unit.scope_link(file.translation_unit)
        self.includes.append(file)

    def set_include_guard(self, include_guard: str|None = None):
        self.include_guard = include_guard

    def struct(self, name: str, **fields: Type) -> Struct:
        new_struct = self.translation_unit.struct(name, **fields)
        if not new_struct.annonymous:
            self.declare(new_struct)

        return new_struct

    def enum(self, name: str, *fields: tuple[str, int] | str) -> Typedef:
        new_enum = Scope.enum(self.translation_unit, name, *fields)
        self.declare(new_enum)
        return new_enum

    def func(self, ret: Type, name: str, *args: tuple[Type, str]) -> Func:
        new_func = Func(self.translation_unit, ret, name, *args)
        self.declare(new_func)
        return new_func
    
    def find_type(self, name: str) -> Struct | None:
        return self.translation_unit.find_type(name)

    def find_var(self, name: str):
        return self.translation_unit.find_var(name)

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

        if self.include_guard:
            cat(f'#ifndef {self.include_guard}')
            cat(f'#define {self.include_guard}')
            cat(f'')

        for include in self.includes:
            cat(f'#include <{os.path.basename(include.path)}>')

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

        if self.include_guard:
            cat(f'')
            cat(f'#endif // {self.include_guard}')

        return '\n'.join(res)