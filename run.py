#!/bin/python3

import mkc as c

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

point = c.Struct('Point')
point.add_field(c.int, 'x')
point.add_field(c.int, 'y')
point_t = c.Typedef(point, 'Point')

main.declare(point)
main.declare(point_t)

mkpoint = c.Func(point_t, 'make_point', (c.int, 'x'), (c.int, 'y'))
main.declare(mkpoint)
main.declare(mkpoint.func_decl())

mkpoint.body.add_line(c.Ret(c.Initializer(point_t, {
    'x': mkpoint['x'],
    'y': mkpoint['y']
})))

print(main)
