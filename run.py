#!/bin/python3

import mkc as c
import json

# one, two, three, four = [c.Literal(num) for num in [1, 2, 3, 4]]

# print('test', '=', one + two + three + four, ';')
# print('test', '=', (one + two) % (three + four), ';')

# print('test', '=', (one + two)(three + four), ';')
# print('test', '=', c.Fn('add') (one + two, three + four), ';')

codebase = c.Codebase()
main = codebase.add_new_file('main.c')

TokenType = main.enum('TokenType', 'END_OF_FILE', 'NAME', 'SPACE',
    'OPEN_PARENTHESIS', 'CLOSE_PARENTHESIS', 'OPEN_CURLY', 'CLOSE_CURLY',
    'SEMICOLON')

point = main.struct('',
    type = TokenType,
    begin = c.char.const().ptr(),
    end = c.char.const().ptr()).typedef('Token')

main.declare(point)
main.include_guard = 'TEST_H'

# print(main)

codebase.generate()
