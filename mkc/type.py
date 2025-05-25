
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

    def get_struct(self):
        from mkc.struct import Struct
        from mkc.typedef import Typedef

        if isinstance(self, Struct):
            return self
        elif isinstance(self, Typedef):
            return self.type.get_struct()

        return None

def field_decl(target: tuple[Type, str] | Type) -> str:
    if type(target) is Type:
        return target.type_name()
    else:
        return target[0].feild_declaration(target[1])
