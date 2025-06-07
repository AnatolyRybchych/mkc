
from mkc.translation_unit import TranslationUnit
from mkc.objfile import ObjFile
from mkc.file import File
from mkc.struct import Struct
from mkc.union import Union
from mkc.base_type import *
from mkc.typedef import Typedef
from mkc.ptr import Ptr
from mkc.func_decl import FuncDecl
from mkc.array import Array
from mkc.func import Func
from mkc.expr import Expr
from mkc.operations import Assign, BinOp, GetField, Initializer, Literal, Subscript, Var, Fn
from mkc.operations import Add, Sub, Mul, Div, Mod, Shl, Shr
from mkc.operations import LessThan, GreaterThen, LessOrEqual, GreaterOrEquals
from mkc.consturction.ret import Ret
from mkc.consturction.if_statement import If
from mkc.scope import Scope
from mkc.func_type import FuncType

import os

class Codebase(Scope):
    def __init__(self):
        Scope.__init__(self, Scope.LEVEL_TOP, None)

        self.object_files: list[ObjFile] = []
        self.include_paths: list[str] = []
    
    def add_include_path(self, path: str):
        path = os.path.abspath(path)

        if path not in self.include_paths:
            self.include_paths.append(path)

    def add_new_obj(self) -> ObjFile:
        object_file = ObjFile(self)
        self.object_files.append(object_file)
        return object_file

    def add_new_file(self, filename):
        return self.add_new_obj().add_new_file(filename)

    def find_file(self, filename: str) -> File | None:
        for obj in self.object_files:
            if filename in obj.link_files:
                return obj.link_files[filename]

        return None

    def generate(self):
        for obj in self.object_files:
            for path, source in obj.link_files.items():
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as file:
                    file.write(f'{source}')

