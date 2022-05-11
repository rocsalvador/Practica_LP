from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from TreeVisitor import TreeVisitor
import sys
import os

def writeNotes(notes, outFileName):
    outFile = open(outFileName + ".lily", "w")
    outFile.write("\\version \"2.22.1\"\n\\score {\n\t\\absolute {\n\t\t\\tempo 4 = 240\n\t\t")
    outFile.write(notes)
    outFile.write("\n\t}\n\t\\layout { }\n\t\midi { }\n}\n")


def main():
    input_stream = FileStream(sys.argv[1])
    
    lexer = ExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    tree = parser.root()

    if len(sys.argv) >= 3:
        initProc = sys.argv[2]
        if len(sys.argv) == 4:
            visitor = TreeVisitor(initProc)
        else:
            visitor = TreeVisitor(initProc, sys.argv[3:])
    else:
        visitor = TreeVisitor()
    visitor.visit(tree)

    outFileName = sys.argv[1].split(".jsb")[0]
    writeNotes(visitor.getNotes(), outFileName)

    if os.system("lilypond " + outFileName + ".lily") > 0:
        exit(1)   
    os.system("timidity -Ow -o " + outFileName + ".wav " + outFileName + ".midi")

    # if ffplay command exists, play the wav file
    if os.system("command -v ffplay") == 0:
        os.system("ffplay -nodisp -autoexit " + outFileName + ".wav")

main()