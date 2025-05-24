
class Type:
    def __init__(self, name: str):
        self.name = name

    def typename(self) -> str:
        return self.name