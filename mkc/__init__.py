
from mkc.translation_unit import TranslationUnit
from mkc.objfile import ObjFile
from mkc.file import File
from mkc.type import *
from mkc.base_types import *
from mkc.construction import Ret, If, For, DeclVar
from mkc.func import Func
from mkc.expr import Expr
from mkc.operations import Assign, BinOp, GetField, Initializer, Literal, Subscript, Var, Fn
from mkc.operations import Add, Sub, Mul, Div, Mod, Shl, Shr, And, Or, Not, SizeOf
from mkc.operations import LessThan, GreaterThen, LessOrEqual, GreaterOrEquals
from mkc.scope import Scope


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

            for include_path in self.include_paths:
                cur = os.path.normpath(f'{include_path}/{filename}')
                if cur in obj.link_files:
                    return obj.link_files[cur]

        return None

    def generate(self) -> dict[str, File]:
        res: dict[str, File] = {}

        for obj in self.object_files:
            for path, source in obj.link_files.items():
                res[path] = f'{source}'

        return res
