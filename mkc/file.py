
from mkc.struct import Struct
from mkc.typedef import Typedef

class File:
    def __init__(self, path: str):
        self.path = path
        self.typedefs = []
        self.structs = []

    def declare(self, target):
        # TODO: check duplicate declarations

        if type(target) is Struct:
            self.structs.append(target)
        elif type(target) is Typedef:
            self.typedefs.append(target)
        else:
            raise Exception(f'the costruction of type {type(target)} is not ment to be declared')

    def __str__(self):
        # TODO: reorder accrding to dependencies
        res = []

        for typedef in self.typedefs:
            res += [f'{typedef};']

        for struct in self.structs:
            res += [f'{struct};']

        return '\n'.join(res)