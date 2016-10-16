class Token:
    """
    Simple token data structure
    """
    def __init__(self, tag, value):
        """
        Constructor
        :param str tag: token type (ex 'IDENTIFIER', 'IF', 'LEFT_PAREN').
            Note that 'EOF' is reserved for end of file.
        :param str value: the actual value of the token
        """
        self.tag = tag
        self.value = value

    def __repr__(self):
        return "Token({}, {})".format(self.tag, self.value)

    def __str__(self):
        return "{}: {}".format(self.tag, self.value)

    @staticmethod
    def eof():
        """Return a token representing end of file"""
        return Token('EOF', '')

class TokenStream:
    """
    Wrap this around a lexer.Lexer subclass and profit:
    - Lazy evaluation: uses the Lexer as a generator
    - Supports peek() and eat() for better token control
    - Supports skipping whitespace
    - Creates the EOF token at the end
    """
    def __init__(self, lexer, skip=[]):
        """
        Constructor

        :param Lexer lexer: the lexer that produces the tokens from
            text
        :param list(str) skip: list of token types to skip as
            whitespace
        """
        self.tokens = iter(lexer)
        self.current_token = self.next_token()
        self.skip_types = skip
        self.empty = False

    def peek(self):
        """
        Look at the first token without removing it from
        the stream
        """
        return self.current_token

    def eat(self):
        """
        Remove and return the first token in the stream
        """
        # If we have already exhausted all tokens,
        # raise an error
        if self.empty:
            raise RuntimeError("Trying to eat past EOF")

        # Advance to the next token
        old_token = self.current_token
        self.current_token = self.next_token()

        # EOF is the last valid token to return
        if old_token.tag == 'EOF':
            self.empty = True

        # Return the token we just ate
        return old_token

    def next_token(self):
        """
        Get the next token in the stream (skipping whitespace)
        or Token.eof() otherwise.
        """
        try:
            # Get the next token skipping whitespace
            token = next(self.tokens)
            while token.tag in self.skip_types:
                token = next(self.tokens)
            return token
        except StopIteration:
            # If there are no more tokens, return EOF
            return Token.eof()
