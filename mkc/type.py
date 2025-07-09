
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
        from mkc.ptr import Ptr
        return Ptr(self)

    def typedef(self, name: str):
        from mkc.typedef import Typedef
        return Typedef(self, name)
    
    def const(self):
        from mkc.const import Const
        if isinstance(self, Const):
            return self
        else:
            return Const(self)

    def get_origin(self, discard = ['typedef', 'ptr', 'array', 'const']):
        from mkc.struct import Struct
        from mkc.const import Const
        from mkc.ptr import Ptr
        from mkc.array import Array
        from mkc.typedef import Typedef

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
