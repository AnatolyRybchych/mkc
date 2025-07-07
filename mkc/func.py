from mkc.func_type import FuncType
from mkc.func_decl import FuncDecl
from mkc.type import Type
from mkc.consturction.block import Block
from mkc.consturction.decl_var import DeclVar
from mkc.operations import Var

class Func:
    def __init__(self, scope, ret: Type, name, *args: tuple[Type, str]):
        from mkc.file import File

        self.func_type = FuncType(ret, *args)
        self.body = Block(scope)
        self.name: str = name
        self.scope: File = scope
        self.decl_var: DeclVar = DeclVar(self.func_type, self.name)

        for arg_type, arg_name in args:
            self.body.scope_set_var(DeclVar(arg_type, arg_name))

    def __call__(self, *args):
        from mkc.operations import Call, Fn
        return Fn(self.name)(*args)

    def func_decl(self) -> FuncDecl:
        return FuncDecl(self.func_type, self.name)

    def __str__(self):
        return f'{self.func_type.feild_declaration(self.name)} {self.body}'
