#!/usr/bin/env python3
from parser.lexer import Lexer
from parser.tokens import TokenStream
from parser.parser import TableParser

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

class ExpressionParser(TableParser):
    TableParser.add_rules({
        'expr': [('rule', 'term'), ('rule', 'expr_')],
        'expr_1': [('term', 'PLUS'), ('rule', 'expr')],
        'expr_2': [('term', 'MINUS'), ('rule', 'expr')],
        'expr_3': [('term', '')],
        'term': [('rule', 'factor'), ('rule', 'term_')],
        'term_1': [('term', 'TIMES'), ('rule', 'term')],
        'term_2': [('term', 'DIVIDE'), ('rule', 'term')],
        'term_3': [('term', '')],
        'factor1': [('term', 'NUMBER')],
        'factor2': [
            ('term', 'LEFT_PAREN'),
            ('rule', 'expr'),
            ('term', 'RIGHT_PAREN')
        ]
    })
    TableParser.add_parse_table({
        'expr': {
            'LEFT_PAREN': 'expr',
            'NUMBER': 'expr'
        },
        'expr_': {
            'EOF': 'expr_3',
            'PLUS': 'expr_1',
            'MINUS': 'expr_2',
            'RIGHT_PAREN': 'expr_3'
        },
        'term': {
            'LEFT_PAREN': 'term',
            'NUMBER': 'term',
        },
        'term_': {
            'EOF': 'term_3',
            'PLUS': 'term_3',
            'MINUS': 'term_3',
            'TIMES': 'term_1',
            'DIVIDE': 'term_2',
            'RIGHT_PAREN': 'term_3'
        },
        'factor': {
            'LEFT_PAREN': 'factor2',
            'NUMBER': 'factor1'
        }
    })


if __name__ == '__main__':
    while True:
        try:
            expr = input('math> ')
            lexer = ExpressionLexer(expr)
            parser = ExpressionParser(lexer, 'expr', ['SPACE'])
            cst = parser.parse()
            print("Concrete Syntax Tree:\n{}".format(cst))
        except (SyntaxError, RuntimeError) as e:
            print("Error: {}".format(e))
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break
