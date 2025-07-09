from mkc.type import Type

class Enum(Type):
    def __init__(self, name: str, file = None, *fields: tuple[str, int] | str):
        from mkc.file import File
        super().__init__()
        self.name: str = name
        self.file: File | None = file
        self.fields: list[tuple[str, int|None]] = []
        self.annonymous = True
        self.prefix: str = ''

        for field in fields:
            if type(field) is str:
                self.add_field(field)
            else:
                self.add_field(field[0], field[1])

    def set_prefix(self, prefix: str):
        self.prefix = prefix

    def keys(self) -> list[str]:
        return [name for name, value in self.fields]

    def __getitem__(self, key: str):
        from mkc.consturction.decl_var import DeclVar
        import mkc as c

        assert key in self.keys() or f'{self.prefix}{key}' in self.keys()

        return c.Var(DeclVar(c.int, f'{self.prefix}{key}'))

    def full_field_declaration(self, name):
        return f'{self} {name}'

    def add_field(self, name: str, value: int|None = None):
        assert not any(existing_name == name for existing_name, _ in self.fields)

        if value is not None:
            existing_values = filter(lambda v: v is not None, [v for _, v in self.fields])
            assert value not in existing_values

        self.fields.append((name, value))

    def __str__(self):
        fields = [f'{name}{value and f'= {value}' or ''}' for name, value in self.fields]
        return f'enum {self.name}' + '{' + ','.join(f'{self.prefix}{field}' for field in fields) + '}'
