
from mkc.translation_unit import TranslationUnit
from mkc.objfile import ObjFile
from mkc.struct import Struct
from mkc.base_type import *
from mkc.typedef import Typedef
from mkc.ptr import Ptr

class Codebase(TranslationUnit):
    def __init__(self):
        self.object_files = []
        self.include_paths = []

    def add_new_obj(self) -> ObjFile:
        object_file = ObjFile()
        self.object_files.append(object_file)
        return object_file

    def add_new_file(self, filename):
        return self.add_new_obj().add_new_file(filename)
