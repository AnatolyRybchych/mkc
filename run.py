#!/bin/python3

import mkc as c

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

days = main.enum('Days', 'MONDAY', 'TUESDAY')

point = main.struct('Point', x = c.int, y = c.int).typedef()
main.declare(point)

mkpoint = main.func(point, 'make_point', (c.int, 'x'), (c.int, 'y'))
main.declare(mkpoint.func_decl())

mkpoint.body.add_line(c.Ret(c.Initializer(point, {
    'x': mkpoint['x'],
    'y': mkpoint['y']
})))

print(main)
