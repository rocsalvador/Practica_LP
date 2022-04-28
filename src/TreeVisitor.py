if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor

class TreeVisitor(ExprVisitor):
    def __init__(self):
        self.symTableStack = []
        # self.outFile = open("a.out", "w")
        self.funcTable = {}

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


    def visitArithmetic(self, ctx):
        value_1 = self.visit(ctx.expr(0))
        value_2 = self.visit(ctx.expr(1))

        if ctx.MINUS():
            return value_1 - value_2
        elif ctx.SUM():
            return value_1 + value_2


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


    def visitArraySize(self, ctx: ExprParser.ArraySizeContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        return len(scopeSymTable[ctx.ID().getText()])


    def visitArrayAccess(self, ctx: ExprParser.ArrayAccessContext):
        scopeSymTable = self.symTableStack[len(self.symTableStack)-1]
        i = self.visit(ctx.expr())
        return scopeSymTable[ctx.ID().getText()][i]
        

    def visitArrayDecl(self, ctx: ExprParser.ArrayDeclContext):
        notes = []
        for note in ctx.NOTE():
            notes.append(self.getNoteValue(note.getText()))
        return notes


    def getNoteValue(self, note):
        value = 0
        if len(note) == 1:
            if note[0] == 'A':
                value = 21
            elif note[0] == 'B':
                value = 22
            elif note[0] == 'C':
                value = 23
            elif note[0] == 'D':
                value = 24
            elif note[0] == 'E':
                value = 25
            elif note[0] == 'F':
                value = 26
            elif note[0] == 'G':
                value = 27
        else:
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
            value += int(note[1]) * 7
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