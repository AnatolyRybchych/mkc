
from mkc.scope import Scope
from mkc.expr import Expr
from mkc.operations import *

class Construction:
    def __init__(self):
        pass

    def __str__(self) -> str:
        raise Exception(f'{type(self)} is not implemented')

def as_construction(param):
    from mkc.expr import Expr
    from mkc.operations import Nop

    if param is None:
        param = Nop()

    if isinstance(param, Construction):
        return param

    if isinstance(param, Expr):
        return Line(param)

    raise Exception(f'The parameter of type {type(param)} cannot represent construction')

class DeclVar(Construction):
    def __init__(self, type: Type, name: str, expr: Expr = Nop()):
        super().__init__()
        self.type = type
        self.name = name
        self.expr = expr

    def __str__(self) -> str:
        res = self.type.feild_declaration(self.name)
        if not isinstance(self.expr, Nop):
            res += f'={self.expr}'
        res += ';'

        return  res

    def var(self):
        from mkc.operations import Var
        return Var(self)

class Block(Construction, Scope):
    def __init__(self, parent):
        Construction.__init__(self)
        Scope.__init__(self, Scope.LEVEL_BLOCK, parent)

        self.lines: list[Construction] = []
        self.logical = False

    def is_empty(self) -> bool:
        return all(type(line) is Block and line.is_empty() for line in self.lines)

    def add_block(self):
        block = Block(self)
        self.add_line(block)
        return block
    
    def add_logical_block(self):

        block = Block(self)
        block.logical = True
        self.add_line(block)
        return block

    def add_if(self, condition: Expr, then = None, otherwice = None):
        if_statement = If(self, condition, then, otherwice)
        self.add_line(if_statement)
        return if_statement

    def add_for(self, init: Construction | Expr | None, condition: Expr, increment: Expr):
        while_loop = For(self, init, condition, increment)
        self.add_line(while_loop)
        return while_loop

    def add_while(self, condition: Expr):
        for_loop = While(self, condition)
        self.add_line(for_loop)
        return for_loop

    def add_switch(self, target: Expr, cases: list[tuple[Expr, Construction | Expr]] = []):
        switch =  Switch(self, target, cases)
        self.add_line(switch)
        return switch

    def add_comment(self, text: str):
        comment = Comment(text)
        self.add_line(comment)
        return comment

    def add_line(self, line: Expr | Construction) -> Construction:
        if isinstance(line, Expr):
            line = Line(line)
            self.lines.append(line)
        elif isinstance(line, Construction):
            if isinstance(line, DeclVar):
                self.scope_set_var(line)

            self.lines.append(line)
        else:
            raise Exception(f'{type(line)} is neither a construction or expression')

        return line

    def declare(self, type: Type, name: str, expr: Expr = Nop()) -> DeclVar:
        var = DeclVar(type, name, expr)
        self.add_line(var)
        return var

    def __str__(self) -> str:
        lines = ''.join(f'{line}' for line in self.lines)
        if not self.logical:
            return '{' + lines + '}'
        else:
            return lines

class Comment(Construction):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return f'// {self.text}\n'

class For(Construction):
    def __init__(self, parent_block: Block, init: Construction | Expr | None, condition: Expr, increment: Expr):
        super().__init__()

        self.parent_block = parent_block
        self.init: Construction = as_construction(init)
        self.condition: Expr = condition
        self.increment: Expr = increment
        self.body: Block = Block(parent_block)

    def __str__(self) -> str:
        consruction = f'for ({self.init} {self.condition};{self.increment})'
        if self.body.is_empty():
            return f'{consruction};'
        else:
            return f'{consruction}{self.body}'

class FuncDecl(DeclVar):
    def __init__(self, type, name):
        super().__init__(type, name, Nop())

    def __call__(self, *args):
        from mkc.operations import Call, Fn
        return Fn(self.name)(*args)

class For(Construction):
    def __init__(self, parent_block: Block, init: Construction | Expr | None, condition: Expr, increment: Expr):
        super().__init__()

        self.parent_block = parent_block
        self.init: Construction = as_construction(init)
        self.condition: Expr = condition
        self.increment: Expr = increment
        self.body: Block = Block(parent_block)

    def __str__(self) -> str:
        consruction = f'for ({self.init} {self.condition};{self.increment})'
        if self.body.is_empty():
            return f'{consruction};'
        else:
            return f'{consruction}{self.body}'

class FuncDecl(DeclVar):
    def __init__(self, type, name):
        super().__init__(type, name, Nop())

    def __call__(self, *args):
        from mkc.operations import Call, Fn
        return Fn(self.name)(*args)

class If(Construction):
    def __init__(self, parent_block, condition: Expr, then: Construction| Expr | None = None, otherwice: Construction | Expr | None = None):
        super().__init__()

        self.parent_block = parent_block
        self.condition: Expr = condition
        self.then: Block = Block(parent_block)
        self.then.add_line(as_construction(then))

        self.otherwice: Block | None = None

        if otherwice is not None:
            self.otherwice = Block(parent_block)
            self.otherwice.add_line(as_construction(otherwice))

    def __str__(self) -> str:
        then = self.then
        if not isinstance(then, Block):
            then = Block(self.parent_block)
            then.add_line(self.then)

        result = f'if ({self.condition}) {then}\n'
        if self.otherwice:
            result += f'else {self.otherwice}\n'

        return result

class Line(Construction):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

    def __str__(self) -> str:
        return f'{self.expr};'

class Ret(Construction):
    def __init__(self, expr: Expr = Nop()):
        super().__init__()
        self.expr = expr

    def __str__(self) -> str:
        return f'return {self.expr};'

class Switch(Construction):
    def __init__(self, parent_block, target: Expr, cases: list[tuple[Expr, Construction | Expr]] = [], default: Construction | Expr | None = None):
        from mkc.operations import Literal
        super().__init__()

        self.parent_block = parent_block
        self.target: Expr = target
        self.cases: list[tuple[Expr, Construction]] = [\
            (Literal.expr_or_literal(expr), as_construction(construction))
            for expr, construction in cases]

        self.default: Construction = default and as_construction(default)

    def add_case(self, condition: Expr, construction: Construction | Expr):
        from mkc.operations import Literal

        self.cases.append((Literal.expr_or_literal(condition), as_construction(construction)))

    def set_default(self, default: Construction | Expr | None = None):
        self.default: Construction = default and as_construction(default)

    def __str__(self) -> str:
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
        if self.default:
            result += f'default:\n{self.default}'

        result += '}\n'

        return result

class While(Construction):
    def __init__(self, parent_block: Block, condition: Expr):
        super().__init__()

        self.parent_block = parent_block
        self.condition: Expr = condition
        self.body: Block = Block(parent_block)

    def __str__(self) -> str:
        return f'while ({self.condition}){self.body}'
