from mkc.func_type import FuncType
from mkc.func_decl import FuncDecl
from mkc.type import Type
from mkc.consturction.block import Block
from mkc.consturction.decl_var import DeclVar
from mkc.operations import Var

class Func:
    def __init__(self, file, ret: Type, name, *args: tuple[Type, str]):
        from mkc.file import File

        self.func_type = FuncType(ret, *args)
        self.body = Block()
        self.name: str = name
        self.file: File = file

        for arg_type, arg_name in args:
            self.body.scope_set_var(DeclVar(arg_type, arg_name))

    def func_decl(self) -> FuncDecl:
        return FuncDecl(self.func_type, self.name)

    def __str__(self):
        return f'{self.func_type.feild_declaration(self.name)} {self.body}'
