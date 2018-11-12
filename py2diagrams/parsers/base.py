class BaseAnalyzer(object):
    def __init__(self, base_node):
        self.base_node = base_node

    def analyze(self):
        raise NotImplementedError()