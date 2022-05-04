from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from TreeVisitor import TreeVisitor
import sys

def writeNotes(notes, outFileName):
    outFile = open(outFileName + ".lily", "w")
    outFile.write("\\version \"2.22.1\"\n\\score {\n\t\\absolute {\n\t\t\\tempo 4 = 240\n\t\t")
    outFile.write(notes)
    outFile.write("\n\t}\n\t\\layout { }\n\t\midi { }\n}")


def main():
    if len(sys.argv) >= 2:
        input_stream = FileStream(sys.argv[1])
    else:
        input_stream = InputStream(input('? '))
    
    lexer = ExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    tree = parser.root()

    visitor = TreeVisitor()
    visitor.visit(tree)

    outFileName = sys.argv[2]
    writeNotes(visitor.getNotes(), outFileName)


main()