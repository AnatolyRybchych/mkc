
class Type:
    def __init__(self):
        self.typedefs = []

    def type_name(self) -> str:
        raise Exception(f'{type(self)}.type_name() is not defined')

    def feild_declaration(self, name: str) -> str:
        raise Exception(f'{type(self)}.feild_declaration({name}) is not defined')

def field_decl(target: tuple[Type, str] | Type) -> str:
    if type(target) is Type:
        return target.type_name()
    else:
        return target[0].feild_declaration(target[1])
