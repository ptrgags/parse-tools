from parser.trees import CSTNode
from parser.tokens import TokenStream

class ParseSymbol:
    def __init__(self, symbol_type, symbol):
        self.symbol_type = symbol_type
        self.symbol = symbol

    def __repr__(self):
        return "{}: {}".format(self.symbol_type, self.symbol)

class TableParser:
    """
    A table-based parser that takes rule
    descriptions and a parse table and constructs
    a concrete syntax tree from them.

    IMPORTANT: TableParser.add_rules() and TableParser.add_table()
        must be called in the body of each subclass.
    """
    def __init__(self, lexer, start_rule, skip=[]):
        """
        Constructor

        :param Lexer lexer: the Lexer to wrap
        :param str start_rule: the rule to start with
        :param str skip: list of whitespace characters to skip
        """
        self.tokens = TokenStream(lexer, skip)

        # Initialize the symbols on the stack
        self.symbol_stack = [
            ParseSymbol('term', 'EOF'),
            ParseSymbol('rule', start_rule)
        ]

        # Another stack to help construct the CST
        self.cst_stack = []

    def parse(self):
        while self.symbol_stack:
            # Read the next symbol to match
            symbol = self.symbol_stack.pop()
            if symbol.symbol_type == 'rule_end':
                self.finish_rule(symbol)
            elif symbol.symbol_type == 'term':
                finished = self.parse_terminal(symbol)
                if finished:
                    return self.cst_stack[0]
            elif symbol.symbol_type == 'rule':
                self.parse_rule(symbol)

    def finish_rule(self, symbol):
        """
        Finish a syntactic rule. Pop the top CST node off
        the stack and append it to the children of the node underneath.
        """
        child = self.cst_stack.pop()
        try:
            self.cst_stack[-1].children.append(child)
        except IndexError:
            self.cst_stack.append(child)

    def parse_terminal(self, symbol):
        """
        Match a terminal symbol to a token. This adds a child
        node to the top CST node on the stack
        """
        #Get the last CST node and the next token
        last_node = self.cst_stack[-1]
        token = self.tokens.peek()

        if symbol.symbol == '':
            # Match empty string, creating a new CST node
            last_node.children.append(CSTNode('term', ''))
        elif symbol.symbol == 'EOF':
            # Match EOF. If it succeeds, we have finished
            self.tokens.expect('EOF')
            return True
        else:
            # Match a specific token type, creating a new CST node
            self.tokens.expect(symbol.symbol)
            last_node.children.append(CSTNode('term', token.tag, token.value))

        # We are not yet finished
        return False

    def parse_rule(self, symbol):
        """
        Replace a rule with a rule from the parse table. This
        also adds a syntax tree node to the stack
        """

        # Add a syntax tree node for the current rule to the
        # CST stack
        rule_node = CSTNode(symbol.symbol_type, symbol.symbol)
        self.cst_stack.append(rule_node)

        # Look at the next token. when replacing a rule, no
        # tokens are removed from the stream
        token = self.tokens.peek()

        # Look up the next rule in the parse table
        try:
            rule = self.PARSE_TABLE[symbol.symbol][token.tag]
        except KeyError:
            raise SyntaxError("Invalid Token {} for rule {}".format(
                token, symbol.symbol))

        #  Look up the rule in the rule list. Also add a rule terminator
        # to the end since this will help construct the tree
        next_rule = self.RULES[rule] + [ParseSymbol('rule_end', None)]

        # Add the rule to the top of the symbol stack. It is reversed
        # so the rule's first symbol is on top
        self.symbol_stack.extend(next_rule[::-1])

    # TODO: Add a method for reading rules from a file
    @classmethod
    def add_rules(cls, rules):
        """
        Add a list of rules to the parser.
        The rules are a dict of rule name -> list((symbol_type, symbol))
        representing grammar rules of a left-factored LL(1) grammar.

        symbol_type is one of:
        - "term" (terminal symbol)
        - "rule" (syntactic rule)

        symbol is a tag of one of the token types defined at the lexing
        stage. It can also be '' to represent matching nothing

        :param dict{str -> list(tuple)} rules: the rules
        """
        cls.RULES = {
            rule_name: [ParseSymbol(*sym) for sym in rule]
            for rule_name, rule in rules.items()}

    # TODO: Add a method for constructing the parse table from the rules
    @classmethod
    def add_parse_table(cls, table):
        """
        Add the parse table needed for the parser.
        The parse table is a dict of dicts:
        {rule_name -> {next_token -> next_rule}}
        This represents a sparse 2D matrix that represents a parse table.
        rule_name and next_rule must correspond with rules defined in
        add_rules.

        :param dict{str -> {str -> str}} table: the parse table as
            described above.
        """
        cls.PARSE_TABLE = table
