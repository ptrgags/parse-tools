class CSTNode:
    """
    Concrete Syntax Tree where each node is either a
    syntactic category or a terminal symbol
    """
    def __init__(self, symbol_type, symbol, value=None):
        self.symbol_type = symbol_type
        self.symbol = symbol
        self.value = value
        self.children = []

    def pretty(self, depth=0):
        return "{}{}".format(
            "{:4} {}{}\n".format(depth, "--" * depth, repr(self)),
            "".join(x.pretty(depth + 1) for x in self.children))

    def __str__(self):
        return self.pretty()

    def __repr__(self):
        return "{}/{}: {}".format(self.symbol_type, self.symbol, self.value)
