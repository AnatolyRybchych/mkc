#!/bin/python3

import mkc as c

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

point = main.struct('Point')
point.add_field(c.int, 'x')
point.add_field(c.int, 'y')
point_t = point.typedef()
main.declare(point_t)

mkpoint = main.func(point_t, 'make_point', (c.int, 'x'), (c.int, 'y'))
main.declare(mkpoint.func_decl())

mkpoint.body.add_line(c.Ret(c.Initializer(point_t, {
    'x': mkpoint['x'],
    'y': mkpoint['y']
})))

print(main)
