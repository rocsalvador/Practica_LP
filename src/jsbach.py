from random import Random
from socket import SOCK_STREAM
from time import time
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
import sys
import os
from jsbachLexer import jsbachLexer
from jsbachVisitor import jsbachVisitor
from jsbachParser import jsbachParser


class TreeVisitor(jsbachVisitor):
    def __init__(self, initProc="Main"):
        self.symTableStack = []
        self.funcTable = {}
        self.strNotes = ""
        self.initProc = initProc
        self.tempo = 120
        self.time = [4, 4]

    def writeNotes(self, outFileName):
        with open(outFileName + ".lily", "w") as outFile:
            outFile.write("\\version \"2.20.0\"\n\\score {\n\t\\absolute {")
            outFile.write("\n\t\t\\time " + str(int(self.time[0])) + "/" + str(int(self.time[1])))
            outFile.write(" \n\t\t\\tempo 4 = " + str(int(self.tempo)) + "\n\t\t")
            outFile.write(self.strNotes)
            outFile.write("\n\t}\n\t\\layout { }\n\t\\midi { }\n}\n")

    def visitRoot(self, ctx: jsbachParser.RootContext):
        mainCtx = None
        for procDef in ctx.procDef():
            if procDef.PROCNAME().getText() == self.initProc:
                mainCtx = procDef
            else:
                self.visit(procDef)
        if mainCtx is None:
            raise Exception("Procedure is not defined: " + self.initProc)
        self.visit(mainCtx)

    def visitParenthesis(self, ctx: jsbachParser.ParenthesisContext):
        return self.visit(ctx.expr())

    def visitWhile(self, ctx: jsbachParser.WhileContext):
        condition = self.visit(ctx.expr())
        while condition:
            self.visit(ctx.statements())
            condition = self.visit(ctx.expr())

    def visitIf(self, ctx: jsbachParser.IfContext):
        condition = self.visit(ctx.expr())
        if condition:
            self.visit(ctx.statements(0))
        elif ctx.statements(1):
            self.visit(ctx.statements(1))

    def visitRead(self, ctx: jsbachParser.ReadContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        scopeSymTable[ctx.ID().getText()] = int(input())

    def visitProcCall(self, ctx: jsbachParser.ProcCallContext):
        procName = ctx.PROCNAME().getText()
        if procName not in self.funcTable:
            raise Exception("Procedure is not defined: " + ctx.PROCNAME().getText())

        if len(ctx.expr()) >= len(self.funcTable[procName]):
            raise Exception("Too many arguments in procedure call: " + procName)
        elif len(ctx.expr()) < len(self.funcTable[procName]) - 1:
            raise Exception("Too few arguments in procedure call: " + procName)

        scopeSymTable = {}
        i = 1
        for expr in ctx.expr():
            value = self.visit(expr)
            scopeSymTable[self.funcTable[procName][i]] = value
            i += 1
        self.symTableStack.append(scopeSymTable)

        self.visitChildren(self.funcTable[procName][0])
        self.symTableStack.pop()

    def visitReprod(self, ctx: jsbachParser.ReprodContext):
        value1 = self.visit(ctx.expr(0))
        noteTy = ''
        valueTy = 4
        if ctx.expr(1):
            valueTy = self.visit(ctx.expr(1))

        if (type(valueTy) is list and type(value1) is list and len(value1) != len(valueTy)):
            raise Exception("The length of the array of notes and the array of note types differ: " + ctx.getText())

        if type(value1) is list:
            i = 0
            for note in value1:
                if type(note) is list:
                    self.strNotes += '< '
                    for x in note:
                        self.strNotes += self.getLilyNote(x) + ' '
                    self.strNotes += '>'
                else:
                    self.strNotes += self.getLilyNote(note)

                if type(valueTy) is not list:
                    noteTy = str(int(valueTy))
                else:
                    noteTy = str(int(valueTy[i]))
                self.strNotes += noteTy
                i += 1
        else:
            self.strNotes += self.getLilyNote(value1) + str(int(valueTy))
        self.strNotes += ' '

    def visitRemove(self, ctx: jsbachParser.RemoveContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        arrayName = ctx.ID().getText()

        i = self.visit(ctx.expr())
        if i % 1 != 0:
            raise Exception("Cannot acces a non integer arrat position: " + ctx.getText())
        i = int(i)
        if i > len(scopeSymTable[arrayName]) or i == 0:
            raise Exception("Array remove out of bound: " + ctx.getText())

        del scopeSymTable[arrayName][i-1]

    def visitPush(self, ctx: jsbachParser.PushContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        arrayName = ctx.ID().getText()
        value = self.visit(ctx.expr())
        if arrayName not in scopeSymTable:
            scopeSymTable[arrayName] = []
        if type(scopeSymTable[arrayName]) is not list:
            raise Exception("Cannot append values to a non array type: " + ctx.getText())
        scopeSymTable[arrayName].append(value)

    def visitArithmetic(self, ctx):
        value_1 = self.visit(ctx.expr(0))
        value_2 = self.visit(ctx.expr(1))

        if ctx.MINUS():
            return value_1 - value_2
        elif ctx.SUM():
            return value_1 + value_2
        elif ctx.MUL():
            return value_1 * value_2
        elif ctx.DIV():
            if value_2 == 0:
                raise Exception("Division by 0: " + ctx.getText())
            return float(value_1 / value_2)
        elif ctx.MOD():
            return value_1 % value_2

    def visitProcDef(self, ctx: jsbachParser.ProcDefContext):
        procName = ctx.PROCNAME().getText()
        if procName in self.funcTable:
            raise Exception("Procedure already defined: " + procName)

        if procName != self.initProc:
            self.funcTable[procName] = [ctx]
            for param in ctx.ID():
                self.funcTable[procName].append(param.getText())
        else:
            self.symTableStack.append({})
            self.visitChildren(ctx)
            self.symTableStack.pop()

    def visitWrite(self, ctx: jsbachParser.WriteContext):
        for child in ctx.writeParams().getChildren():
            val = self.visit(child)
            if type(val) is float and val % 1 == 0:
                val = int(val)
            print(val, end=" ")
        print()

    def visitRelational(self, ctx: jsbachParser.RelationalContext):
        value_1 = self.visit(ctx.expr(0))
        value_2 = self.visit(ctx.expr(1))

        if ctx.GT():
            return int(value_1 > value_2)
        elif ctx.GE():
            return int(value_1 >= value_2)
        elif ctx.EQ():
            return int(value_1 == value_2)
        elif ctx.NEQ():
            return int(value_1 != value_2)
        elif ctx.LT():
            return int(value_1 < value_2)
        elif ctx.LE():
            return int(value_1 <= value_2)

    def visitAssign(self, ctx: jsbachParser.AssignContext):
        value = self.visit(ctx.expr())
        if ctx.TEMPO():
            self.tempo = value
        elif ctx.TIME():
            if type(value) is not list or len(value) != 2:
                raise Exception("Time feature must be assigned with a two length array")
            self.time = value
        else:
            varName = ctx.ID().getText()
            scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
            scopeSymTable[varName] = value
        return 0

    def visitNoteExpr(self, ctx: jsbachParser.NoteExprContext):
        return self.visit(ctx.note())

    def visitArraySize(self, ctx: jsbachParser.ArraySizeContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        return len(scopeSymTable[ctx.ID().getText()])

    def visitArrayAccess(self, ctx: jsbachParser.ArrayAccessContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        arrayName = ctx.ID().getText()
        i = self.visit(ctx.expr())
        if i % 1 != 0:
            raise Exception("Cannot acces a non integer array position: " + ctx.getText())
        i = int(i)

        if i > len(scopeSymTable[arrayName]) or i == 0:
            raise Exception("Array access out of bound: " + ctx.getText())

        return scopeSymTable[arrayName][i - 1]

    def visitArrayDecl(self, ctx: jsbachParser.ArrayDeclContext):
        array = []
        for expr in ctx.expr():
            array.append(self.visit(expr))
        return array

    def visitNote(self, ctx: jsbachParser.NoteContext):
        note = ctx.NOTE().getText()
        value = ord(note[0]) - 65
        scale = 4
        if len(note) == 3:
            scale = int(note[1])
            if note[2] == 'b':
                value += 0.25
            else:
                value += 0.75
        elif len(note) == 2:
            if note[1] == 'b':
                value += 0.25
            elif note[1] == '#':
                value += 0.75
            else:
                scale = int(note[1])
        if not note[0] == 'A' and not note[0] == 'B':
            scale -= 1
        value += scale * 7
        return value

    def visitId(self, ctx: jsbachParser.IdContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        if not ctx.getText() in scopeSymTable:
            scopeSymTable[ctx.getText()] = 0
            return 0
        else:
            return scopeSymTable[ctx.getText()]

    def visitNumValue(self, ctx: jsbachParser.NumValueContext):
        value = float(ctx.getText())
        return value

    def visitString(self, ctx: jsbachParser.StringContext):
        return ctx.getText()[1:len(ctx.getText())-1]

    def getLilyNote(self, note):
        strNote = chr(97 + int(note) % 7)
        # es -> bem
        # is -> sost
        mod = note % 1
        if mod == 0.25:
            strNote += 'es'
        elif mod == 0.75:
            strNote += 'is'

        if note >= 23:
            x = int((note - 23) / 7) + 1
            for _ in range(x):
                strNote += '\''
        elif note < 16:
            if note >= 9:
                strNote += ','
            elif note >= 2:
                strNote += ',,'
            else:
                strNote += ',,,'
        return strNote

    def visitRandom(self, ctx: jsbachParser.RandomContext):
        rand = Random(time())
        return Random.randint(rand, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))


class JsbachErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        super().syntaxError(recognizer, offendingSymbol, line, column, msg, e)
        raise Exception("Syntax error in " + str(line) + ":" + str(column) + " -> " + msg)


def main():
    nArgs = len(sys.argv)

    if nArgs < 2:
        print("Usage:")
        print("python3 path/to/jsbach.py source_file.jsb [initial_procedure]")
        exit(1)

    input_stream = FileStream(sys.argv[1])
    lexer = jsbachLexer(input_stream)
    lexer.addErrorListener(JsbachErrorListener())
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    parser.addErrorListener(JsbachErrorListener())
    tree = parser.root()

    if nArgs == 3:
        initProc = sys.argv[2]
        visitor = TreeVisitor(initProc)
    else:
        visitor = TreeVisitor()
    visitor.visit(tree)

    outFileName = os.path.basename(sys.argv[1]).split(".jsb")[0]
    visitor.writeNotes(outFileName)

    os.system("lilypond " + outFileName + ".lily")
    os.system("timidity -Ow -o " + outFileName + ".wav " + outFileName + ".midi")
    os.system("ffmpeg -y -i " + outFileName + ".wav -codec:a libmp3lame -qscale:a 2 " + outFileName + ".mp3")

    if os.system("command -v ffplay") == 0:
        os.system("ffplay -nodisp -autoexit " + outFileName + ".mp3")


if __name__ == '__main__':
    main()
