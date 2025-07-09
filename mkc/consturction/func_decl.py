from mkc.type import Type, field_decl, FuncType
from mkc.consturction.decl_var import DeclVar
from mkc.operations import Nop

class FuncDecl(DeclVar):
    def __init__(self, type, name):
        super().__init__(type, name, Nop())

    def __call__(self, *args):
        from mkc.operations import Call, Fn
        return Fn(self.name)(*args)

