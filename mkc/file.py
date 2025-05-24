
from mkc.struct import Struct
from mkc.typedef import Typedef
from mkc.func_decl import FuncDecl
from mkc.func import Func
from mkc.type import Type

class File:
    def __init__(self, path: str, translation_unit):
        from mkc.translation_unit import TranslationUnit

        self.path = path
        self.typedefs: list[Typedef] = []
        self.structs: list[Struct] = []
        self.func_decls: list[FuncDecl] = []
        self.funcs: list[Func] = []
        self.translation_unit: TranslationUnit = translation_unit

    def struct(self, name: str) -> Struct:
        new_struct = Struct(name, self)
        self.declare(new_struct)
        return new_struct

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
        else:
            raise Exception(f'the costruction of type {type(target)} is not ment to be declared')

    def __str__(self):
        # TODO: reorder accrding to dependencies
        res = []

        for typedef in self.typedefs:
            res += [f'{typedef};']

        for struct in self.structs:
            res += ['', f'{struct};']

        if self.structs and self.func_decls:
            res += ['']

        for func_decl in self.func_decls:
            res += [f'{func_decl};']

        for func in self.funcs:
            res += ['', f'{func}']

        return '\n'.join(res)