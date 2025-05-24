from mkc.construction import Construction

class Block(Construction):
    def __init__(self):
        super().__init__()
        self.lines = []

    def __str__(self):
        return '{' + ''.join(f'{line};' for line in self.lines) + '}'
