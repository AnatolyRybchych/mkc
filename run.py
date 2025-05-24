#!/bin/python3

import mkc as c

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

point = c.Struct('Point')
point.add_field(c.Array(c.int, 2), 'coords')

point_t = c.Typedef(point, 'Point')

main.declare(point)
main.declare(c.Typedef(c.Ptr(point_t), 'PointPtr'))
main.declare(c.FuncDecl(point_t, 'make_point', (c.int, 'x'), (c.int, 'y')))

print(main)
