import ast
import os

from py2diagrams.parsers.class_analyzer import ClassAnalyzer


def execute(base_path):
    if not os.path.exists(base_path):
        raise FileNotFoundError()
    results = {}
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if not file.endswith(".py"):
                continue
            with open(os.path.join(root, file)) as f:
                content = f.read()
            module_ast = ast.parse(content)
            for node in module_ast.body:
                try:
                    analyzer = ClassAnalyzer(node)
                    analyze_result = analyzer.analyze()
                    results[analyze_result.name] = analyze_result
                except:
                    pass
    for name, result in results.items():
        result.print_puml(False)

