
class Construction:
    def __init__(self):
        pass

    def gen(self) -> str:
        raise Exception(f'{type(self)}.gen() is not implemented')