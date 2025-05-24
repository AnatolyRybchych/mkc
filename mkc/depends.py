
from copy import deepcopy

class Depends:
    def __init__(self):
        self.dependencies: dict[int] = {}

    def get_recursive_dependencies(self) -> list[list]:
        def step(dependency, visited: set) -> list[list]:
            visited = deepcopy(visited)
            if id(dependency) in visited:
                return [[dependency]]

            visited.add(id(dependency))
            recursive = []
            if isinstance(dependency, Depends):
                for subsequesnt in dependency.dependencies.values():
                    recursive += step(subsequesnt, visited)

            for trace in recursive:
                trace.insert(0, dependency)

            return recursive

        return step(self, set())

    def depend_on(self, dependency):
        self.dependencies[id(dependency)] = dependency
        assert len(self.get_recursive_dependencies()) == 0
