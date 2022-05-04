from asyncore import write


if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


class TreeVisitor(ExprVisitor):
    def __init__(self):
        self.symTableStack = []
        self.funcTable = {}
        self.reprodNotes = []

    def visitRoot(self, ctx: ExprParser.RootContext):
        for procDef in ctx.procDef():
            if procDef.PROCNAME().getText() == 'Main':
                mainCtx = procDef
            else:
                self.visit(procDef)
        self.visit(mainCtx)

    def visitParenthesis(self, ctx: ExprParser.ParenthesisContext):
        return self.visit(ctx.expr())

    def visitWhile(self, ctx: ExprParser.WhileContext):
        condition = self.visit(ctx.expr())
        while condition:
            self.visit(ctx.statements())
            condition = self.visit(ctx.expr())

    def visitIf(self, ctx: ExprParser.IfContext):
        condition = self.visit(ctx.expr())
        if condition:
            self.visit(ctx.statements(0))
        elif ctx.statements(1):
            self.visit(ctx.statements(1))

    def visitRead(self, ctx: ExprParser.ReadContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        scopeSymTable[ctx.ID().getText()] = int(input())

    def visitProcCall(self, ctx: ExprParser.ProcCallContext):
        scopeSymTable = {}
        i = 1
        for expr in ctx.expr():
            value = self.visit(expr)
            scopeSymTable[self.funcTable[ctx.PROCNAME().getText()][i]] = value
            i += 1
        self.symTableStack.append(scopeSymTable)

        self.visitChildren(self.funcTable[ctx.PROCNAME().getText()][0])
        self.symTableStack.pop()

    def visitReprod(self, ctx: ExprParser.ReprodContext):
        if ctx.note():
            self.reprodNotes.append(self.visit(ctx.note()))
        elif ctx.ID():
            scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
            if type(scopeSymTable[ctx.ID().getText()]) is list:
                self.reprodNotes.extend(scopeSymTable[ctx.ID().getText()])
            else:
                self.reprodNotes.append(scopeSymTable[ctx.ID().getText()])

    def visitRemove(self, ctx: ExprParser.RemoveContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        i = self.visit(ctx.expr())
        del scopeSymTable[ctx.ID().getText()][i-1]

    def visitPush(self, ctx: ExprParser.PushContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        value = self.visit(ctx.expr())
        scopeSymTable[ctx.ID().getText()].append(value)

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
            return int(value_1 / value_2)
        elif ctx.MOD():
            return value_1 % value_2

    def visitProcDef(self, ctx: ExprParser.ProcDefContext):
        if ctx.PROCNAME().getText() != 'Main':
            self.funcTable[ctx.PROCNAME().getText()] = [ctx]
            for param in ctx.ID():
                self.funcTable[ctx.PROCNAME().getText()].append(param.getText())
        else:
            self.symTableStack.append({})
            self.visitChildren(ctx)
            self.symTableStack.pop()

    def visitWrite(self, ctx: ExprParser.WriteContext):
        for expr in ctx.expr():
            ret = self.visit(expr)
            print(str(ret) + " ", end="")
        print()

    def visitRelational(self, ctx: ExprParser.RelationalContext):
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

    def visitAssign(self, ctx: ExprParser.AssignContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        value = self.visit(ctx.expr())
        scopeSymTable[ctx.ID().getText()] = value
        return 0

    def visitNoteExpr(self, ctx: ExprParser.NoteExprContext):
        return self.visit(ctx.note())

    def visitArraySize(self, ctx: ExprParser.ArraySizeContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        return len(scopeSymTable[ctx.ID().getText()])

    def visitArrayAccess(self, ctx: ExprParser.ArrayAccessContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        i = self.visit(ctx.expr())
        return scopeSymTable[ctx.ID().getText()][i-1]

    def visitArrayDecl(self, ctx: ExprParser.ArrayDeclContext):
        array = []
        for expr in ctx.expr():
            array.append(self.visit(expr))
        return array

    def visitNote(self, ctx: ExprParser.NoteContext):
        note = ctx.NOTE().getText()
        if note[0] == 'A':
            value = 0
        elif note[0] == 'B':
            value = 1
        elif note[0] == 'C':
            value = 2
        elif note[0] == 'D':
            value = 3
        elif note[0] == 'E':
            value = 4
        elif note[0] == 'F':
            value = 5
        elif note[0] == 'G':
            value = 6

        if len(note) == 1:
            scale = 4
        else:
            scale = int(note[1])

        if not note[0] == 'A' and not note[0] == 'B':
            scale -= 1

        value += scale * 7
        return value

    def visitId(self, ctx: ExprParser.IdContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        if not ctx.getText() in scopeSymTable:
            scopeSymTable[ctx.getText()] = 0
            return 0
        else:
            return scopeSymTable[ctx.getText()]

    def visitIntValue(self, ctx: ExprParser.IntValueContext):
        value = int(ctx.getText())
        return value

    def visitString(self, ctx: ExprParser.StringContext):
        return ctx.getText()[1:len(ctx.getText())-1]

    def getNotes(self):
        strNotes = ""
        for note in self.reprodNotes:
            mod = note % 7
            if mod == 0:
                strNote = 'a'
            elif mod == 1:
                strNote = 'b'
            elif mod == 2:
                strNote = 'c'
            elif mod == 3:
                strNote = 'd'
            elif mod == 4:
                strNote = 'e'
            elif mod == 5:
                strNote = 'f'
            elif mod == 6:
                strNote = 'g'
            if note > 22:
                x = int((note - 23) / 7) + 1
                for _ in range(x):
                    strNote += '\''
            elif note < 16:
                if note > 8:
                    strNote += ','
                elif note > 1:
                    strNote += ',,'
                else:
                    strNote += ',,,'

            strNotes += strNote + ' '
        return strNotes
