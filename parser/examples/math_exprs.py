#!/usr/bin/env python3
from parser.lexer import Lexer
from parser.tokens import TokenStream

class ExpressionLexer(Lexer):
    Lexer.compile_regexes([
        (r'\d+', 'NUMBER'),
        (r'\+', 'PLUS'),
        (r'-', 'MINUS'),
        (r'/', 'DIVIDE'),
        (r'\*', 'TIMES'),
        (r'\(', 'LEFT_PAREN'),
        (r'\)', 'RIGHT_PAREN'),
        (r'\s+', 'SPACE'),
    ])

if __name__ == '__main__':
    ts = TokenStream(ExpressionLexer("3 + 2 * (3 + 1)"))
    try:
        while True:
            print(ts.eat())
    except RuntimeError:
        print("it's okay")
