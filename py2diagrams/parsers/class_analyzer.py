import ast

from py2diagrams.parsers.assign_analyzer import AssignAnalyzer, AssignAnalyzerResult
from py2diagrams.parsers.base import BaseAnalyzer
from py2diagrams.parsers.function_analyzer import FunctionAnalyzer


class ClassAnalyzerResult(object):
    def __init__(self, name, methods=[], class_properties=[], instance_fields=[], bases=[]):
        self.name = name
        self.methods = methods
        self.instance_fields = instance_fields
        self.class_properties = class_properties
        self.bases = bases

    def __eq__(self, other):
        return self.name == other.name and self.methods == other.methods and \
               self.instance_fields == other.instance_fields and self.class_properties == other.class_properties and \
               self.bases == other.bases

    def print_puml(self, include_puml_boundary=True):
        if include_puml_boundary:
            print("@startuml")
        print("class {}".format(self.name), "{")
        for class_property in self.class_properties:
            private_marker = "-" if class_property.is_private else "+"
            print("  {} {}".format(private_marker, class_property.name))
        for method in self.methods:
            private_marker = "-" if method.is_private else "+"
            args_string = ", ".join([arg["name"] for arg in method.arguments if arg["name"] != "self"])
            predicate = ""
            if method.is_static:
                predicate = "{static}"
            elif method.is_abstract:
                predicate = "{abstract}"
            print("  {} {}{}({})".format(private_marker, predicate, method.name, args_string))
        print("}")
        for base in self.bases:
            print("{}<|--{}".format(base, self.name))
        if include_puml_boundary:
            print("@enduml")


class ClassPropertyRepresentation(AssignAnalyzerResult):
    @property
    def is_private(self):
        return self.name.startswith("_")


class ClassAnalyzer(BaseAnalyzer):
    def __init__(self, base_node):
        if not isinstance(base_node, ast.ClassDef):
            raise TypeError("ClassAnalyzer can only parse type ast.ClassDef nodes as baseline")
        super().__init__(base_node)
        self.name = base_node.name
        self.types = {
            ast.Assign: "Class Property",
            ast.FunctionDef: "Method"
        }

    def analyze(self):
        bases = [base.id for base in self.base_node.bases if base.id != "object"]
        result = ClassAnalyzerResult(self.name, [], [], [], bases)
        for node in self.base_node.body:
            node_type = type(node)
            # analyzer = self.type_to_analyzer.get(node_type)
            # node_representation = analyzer.analyze(node)
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("__"):
                analyzer = FunctionAnalyzer(node)
                node_representation = analyzer.analyze()
                result.methods.append(node_representation)
            elif isinstance(node, ast.Assign):
                analyzer = AssignAnalyzer(node)
                target_representations = analyzer.analyze()
                class_property_representations = [ClassPropertyRepresentation(a.name) for a in target_representations]
                result.class_properties.extend(class_property_representations)
        # result.print_puml(False)
        return result
        # [print(node.name) for node in self.base_node.body if self.types.get(type(node)) == "Method"]