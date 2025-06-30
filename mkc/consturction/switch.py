
from mkc.consturction import Construction, as_construction
from mkc.expr import Expr
from mkc.operations import Nop

class Switch(Construction):
    def __init__(self, parent_block, target: Expr, cases: list[tuple[Expr, Construction | Expr]] = []):
        from mkc.operations import Literal
        super().__init__()

        self.parent_block = parent_block
        self.target: Expr = target
        self.cases: list[tuple[Expr, Construction]] = [\
            (Literal.expr_or_literal(expr), as_construction(construction))
            for expr, construction in cases]

    def add_case(self, condition: Expr, construction: Construction | Expr):
        from mkc.operations import Literal

        self.cases.append((Literal.expr_or_literal(condition), as_construction(construction)))

    def __str__(self) -> str:
        from mkc.consturction.block import Block
        from mkc.consturction.line import Line
        from mkc.consturction.ret import Ret

        if len(self.cases) == 0:
            return ''

        result = f'switch ({self.target})' + '{\n'

        for condition, then in self.cases:
            result += f'case {condition}: {then}'
            if type(then) is Ret:
                pass
            elif type(then) is Block and len(then.lines) != 0 and type(then.lines[-1]) is Ret:
                pass
            else:
                result += f'break;'

        result += '}\n'
        return result
