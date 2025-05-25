#!/bin/python3

import mkc as c

print('test', '=', c.Add(c.Add(c.Literal(1), c.Literal(2)), c.Add(c.Literal(3), c.Literal(4))), ';')
print('test', '=', c.Mul(c.Add(c.Literal(1), c.Literal(2)), c.Add(c.Literal(3), c.Literal(4))), ';')

# codebase = c.Codebase()
# main = codebase.add_new_file('main.c')

# days = main.enum('Days', 'MONDAY', 'TUESDAY')

# point = main.struct('Point', x = c.int, y = c.int).typedef()
# main.declare(point)

# mkpoint = main.func(point, 'make_point', (c.int, 'x'), (c.int, 'y'))
# main.declare(mkpoint.func_decl())

# mkpoint.body.add_line(c.Ret(c.Initializer(point, {
#     'x': mkpoint['x'],
#     'y': mkpoint['y']
# })))

# print(main)
