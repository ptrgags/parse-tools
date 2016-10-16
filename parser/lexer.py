import re

from .tokens import Token

class Lexer:
    """
    Generic Lexer

    IMPORTANT: Subclasses must define token types. See
        Lexer.compile_regexes() for more info

    Also note that each Lexer should be wrapped in a
    TokenStream to support peek(), eat() and returning EOF
    """

    def __init__(self, text):
        '''
        Constructor

        text -- Text to perform lexical analysis on
        '''
        self.text = text
        self.pos = 0

    def __iter__(self):
        """
        Read through the text and generate
        Tokens as a stream
        """
        while self.pos < len(self.text):
            error = True
            for regex, tag in self.TOKEN_TYPES:
                match = regex.match(self.text, self.pos)
                if match:
                    error = False
                    yield Token(tag, match.group(0))
                    self.pos = match.end(0)
                    break
                else:
                    continue
            if error:
                raise Exception((
                    'Syntax Error:\n'
                    'Invallid token in input "{}"\n'
                    'starting at position {}: "{}"'.format(
                        self.text, self.pos, self.text[self.pos:])))

    @classmethod
    def compile_regexes(cls, token_types):
        """
        Compile token patterns to regex objects. Call this
        at the class level in subclasses

        :param list(tuple) token_types: list of (pattern, tag)
            where pattern is a regex string
        """
        cls.TOKEN_TYPES = [
            (re.compile(pattern), tag)
            for pattern, tag in token_types]
