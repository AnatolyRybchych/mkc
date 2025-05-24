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

res = mkpoint.body.declare(point_t, 'res')
mkpoint.body.add_line(res.var()['x'].assign(0))
mkpoint.body.add_line(res.var()['y'].assign(1))
mkpoint.body.add_line(c.Ret(res.var()))

print(main)
