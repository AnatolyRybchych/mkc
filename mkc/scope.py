
class Scope:
    LEVEL_TOP: str = 'top'
    LEVEL_TRANSLATION: str = 'trans'
    LEVEL_FILE: str = 'file'
    LEVEL_BLOCK: str = 'block'

    def __init__(self, scope_level: str, parent = None):
        from mkc.consturction.decl_var import DeclVar

        self.scope_level: str = scope_level
        self.parent_scope: Scope | None = parent

        self.scope_variables:dict[str, DeclVar] = {}

    def __getitem__(self, name: str):
        return self.find_var(name)

    def find_var(self, name: str):
        if name in self.scope_variables:
            return self.scope_variables[name].var()
        elif self.parent_scope is not None:
            return self.parent_scope.find_var(name)
    
    def scope_set_var(self, decl):
        from mkc.consturction.decl_var import DeclVar

        assert isinstance(decl, DeclVar)
        if decl.name in self.scope_variables:
            raise Exception(f'The variable {decl} is aready in the {self.scope_level} scope')

        self.scope_variables[decl.name] = decl