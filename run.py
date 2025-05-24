#!/bin/python3

import mkc as c

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

point = c.Struct('Point')
point.add_field(c.Array(c.int, 2).ptr_type(), 'coords')

point_t = c.Typedef(point, 'Point')

main.declare(point)
main.declare(point_t)

mkpoint = c.Func(point_t, 'make_point', (c.int, 'x'), (c.int, 'y'))
main.declare(mkpoint)
main.declare(mkpoint.func_decl())

print(main)
