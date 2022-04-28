from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from TreeVisitor import TreeVisitor
import sys


def main():
    if len(sys.argv) == 2:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(input('? '))
    lexer = ExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    tree = parser.root()
    visitor = TreeVisitor()
    visitor.visit(tree)

main()