class BaseExample(object):
    A, _CLASS_PROPERTY_f = "foo", "bar"

    def __init__(self, base_param):
        self.base_prop = base_param

    def do_something(self):
        x = self._private_invocation()
        self._private_invocation_with_param(x)

    def _private_invocation(self):
        result = "private invocation in base class"
        print(result)
        return result

    def _private_invocation_with_param(self, param):
        if isinstance(param, str):
            print(param)
        else:
            print("private invocation with param wasn't invoked with a string")

    @staticmethod
    def static_method():
        return 42

    @classmethod
    def class_method(cls):
        return 73

    def abstract(self, p1, p2):
        """docstring"""
        x=1
        raise NotImplementedError()
