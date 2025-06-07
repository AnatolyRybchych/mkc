
class Construction:
    def __init__(self):
        pass

    def __str__(self) -> str:
        raise Exception(f'{type(self)} is not implemented')

def as_construction(param):
    from mkc.expr import Expr
    from mkc.operations import Nop
    from mkc.consturction import Construction
    from mkc.consturction.line import Line

    if param is None:
        param = Nop()

    if isinstance(param, Construction):
        return param

    if isinstance(param, Expr):
        return Line(param)

    raise Exception(f'The parameter of type {type(param)} cannot represent construction')
