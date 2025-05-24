
from mkc.file import File

class TranslationUnit:
    def __init__(self):
        self.include_paths = []
        self.link_files = {}

    def add_file(self, file: File):
        assert file.path not in self.link_files

        self.link_files[file.path] = file
        return self

    def add_new_file(self, filename: str) -> File:
        file = File(filename)
        self.add_file(file)
        return file

