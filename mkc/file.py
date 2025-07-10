
from mkc.type import Struct, Typedef, Enum
from mkc.construction import DeclVar
from mkc.func import Func
from mkc.type import Type, FuncType
from mkc.scope import Scope
from mkc.include import Include

import os 

class File:
    def __init__(self, path: str, translation_unit):
        from mkc.translation_unit import TranslationUnit

        self.include_guard = None
        self.translation_unit:TranslationUnit = translation_unit
        self.path: str = path
        self.typedefs: list[Typedef] = []
        self.structs: list[Struct] = []
        self.func_decls: list[DeclVar] = []
        self.var_decls: list[DeclVar] = []
        self.funcs: list[Func] = []
        self.enums: list[Enum] = []

        self.includes: list[Include] = []

    def include_file(self, file):
        if type(file) is File:
            self.translation_unit.scope_link(file.translation_unit)
            self.includes.append(Include(file.path))
        elif type(file) is str:
            self.includes.append(Include(file))
        else:
            raise Exception(f'file of type {type(file)} is incompatible with {type(self)}.include_file()')

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
        new_func = self.translation_unit.func(ret, name, *args)
        self.declare(new_func)
        return new_func

    def enum_str_func(self, name: str, enum_type: Type, argname: str | None = None) -> Func:
        from mkc.construction import Ret
        from mkc.expr import Literal
        from mkc.base_types import char

        assert isinstance(enum_type, Typedef)
        enum = enum_type.get_origin(['typedef'])
        assert isinstance(enum, Enum)

        argname = argname or f'enum_val'
        enum_str_func = self.func(char.const().ptr(), name, (enum_type, argname))

        switch = enum_str_func.body.add_switch(enum_str_func.body[argname])
        for k in enum.keys():
            switch.add_case(enum[k], Ret(Literal(k)))
        switch.set_default(Ret(Literal(0)))

        return enum_str_func

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
        elif type(target) is DeclVar:
            if type(target.type) is FuncType:
                self.func_decls.append(target)
            else:
                self.var_decls.append(target)
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
            cat(f'{include}')

        for typedef in self.typedefs:
            cat(f'{typedef};')

        for enum in self.enums:
            cat(f'{enum};')

        for struct in self.structs:
            cat(f'{struct};')

        for func_decl in self.func_decls:
            cat(f'{func_decl}')

        if self.func_decls and self.funcs:
            cat('')

        for func in self.funcs:
            cat(f'{func}')

        if self.include_guard:
            cat(f'')
            cat(f'#endif // {self.include_guard}')

        return '\n'.join(res)