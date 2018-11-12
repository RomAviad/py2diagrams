import ast

from py2diagrams.parsers.base import BaseAnalyzer


class FunctionAnalyzerResult(object):
    def __init__(self, name, arguments=[], return_value=None, self_assignments=None, is_private=False, is_static=False,
                 is_abstract=False):
        self.self_assignments = self_assignments
        self.is_private = is_private
        self.is_static = is_static
        self.is_abstract = is_abstract
        self.return_value = return_value
        self.name = name
        self.arguments = arguments


class FunctionAnalyzer(BaseAnalyzer):
    def __init__(self, base_node): #ast.FunctionDef):
        if not isinstance(base_node, ast.FunctionDef):
            raise TypeError("FunctionAnalyzer can only parse type ast.FunctionDef nodes as baseline")
        super().__init__(base_node)
        self.name = base_node.name
        self.is_private = self.name.startswith("_")

    @property
    def is_static(self):
        result = any(map(lambda x: x.id in {"staticmethod", "classmethod"}, self.base_node.decorator_list))
        return result

    @property
    def is_abstract(self):
        result = (isinstance(self.base_node.body[-1], ast.Raise) and
                  self.base_node.body[-1].exc.func.id == "NotImplementedError")
        return result

    def analyze(self):
        result = FunctionAnalyzerResult(self.name, [], None, [], self.is_private, self.is_static, self.is_abstract)
        for arg in self.base_node.args.args:
            result.arguments.append({
                "name": arg.arg,
                "type": arg.annotation
            })
        if self.base_node.returns:
            result.return_value = self.base_node.returns
        # TODO - Self Assignments Handling
        return result
