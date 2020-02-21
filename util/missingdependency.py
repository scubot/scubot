class MissingDependencyException(Exception):
    def __init__(self, missing_module):
        self.missing_module = missing_module

    def __str__(self):
        return f"Missing module {self.missing_module}"
