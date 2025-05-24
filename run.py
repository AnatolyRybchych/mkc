#!/bin/python3

import mkc as c

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

point = c.Struct('Point')
main.declare(point)

point.add_field(c.int, 'x')
point.add_field(c.int, 'y')

main.declare(c.Typedef(point, 'Point'))

print(main)
