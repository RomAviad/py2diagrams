import ast

from py2diagrams.parsers.base import BaseAnalyzer


class AssignAnalyzerResult(object):
    def __init__(self, name):
        self.name = name


class AssignAnalyzer(BaseAnalyzer):
    def __init__(self, base_node): # ast.Assign):
        if not isinstance(base_node, ast.Assign):
            raise TypeError("AssignAnalyzer can only parse type ast.Assign nodes as baseline")
        super().__init__(base_node)

    def analyze(self):
        result = []
        target = self.base_node.targets[0]
        if isinstance(target, ast.Name):
            result = [AssignAnalyzerResult(target.id)]
        elif isinstance(target, ast.Tuple):
            result = [AssignAnalyzerResult(elt.id) for elt in target.elts]
        return result
