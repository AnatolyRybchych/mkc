
from mkc.file import File
from mkc.scope import Scope

class TranslationUnit(Scope):
    def __init__(self, codebase):
        Scope.__init__(self, Scope.LEVEL_TRANSLATION, codebase)

        self.include_paths = []
        self.link_files = {}

    def add_new_file(self, filename: str) -> File:
        assert filename not in self.link_files
        file = File(filename, self)
        self.link_files[filename] = file
        return file

