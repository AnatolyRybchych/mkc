
class Include:
    def __init__(self, filename: str):
        self.filename = filename
        self.local = False

    def __str__(self):
        path = self.local and f'"{self.filename}"' or f'<{self.filename}>'
        return f'#include {path}'