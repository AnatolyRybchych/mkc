from mkc.type import Type

class FuncDecl(Type):
    def __init__(self, ret: Type, name, *args: tuple[Type, str]):
        super().__init__(f'{ret.typename}(*)({','.join(f'{t.typename} {n}' for t, n in args)})')
        self.name = name
        self.args = list(args)
        self.ret_type = ret

    def __str__(self):
        return f'{self.ret_type.typename} {self.name}({','.join(f'{t.typename} {n}' for t, n in self.args)})'