
from mkc.file import File

class TranslationUnit:
    def __init__(self):
        self.include_paths = []
        self.link_files = {}

    def add_new_file(self, filename: str) -> File:
        assert filename not in self.link_files
        file = File(filename, self)
        self.link_files[filename] = file
        return file

