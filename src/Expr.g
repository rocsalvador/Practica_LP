grammar Expr;

root
        : procDef+ EOF ;

statements
        : (statement)*
        ;

procDef
        : PROCNAME ID* '|:' statements ':|'
        ;

statement
        : IF expr '|:' statements ':|' (ELSE '|:' statements ':|')?     # if
        | WHILE expr '|:' statements ':|'                               # while
        | READ ID                                                       # read
        | ID ASSIG expr                                                 # assign                              
        | WRITE expr+                                                   # write
        | REPROD expr                                                   # reprod
        | PROCNAME expr*                                                # procCall
        | REMOVE expr                                                   # remove
        | ID PUSH expr                                                  # push
        ;

expr
        : '(' expr ')'                          # parenthesis
        | expr (SUM|MINUS) expr                 # arithmetic
        | expr (EQ|NEQ|GT|GE|LT|LE) expr        # relational
        | ID '[' expr ']'                       # arrayAccess
        | '#' ID                                # arraySize
        | '{' NOTE* '}'                         # arrayDecl
        | NUM                                   # intValue
        | ID                                    # id
        | STRING                                # string
        ;

READ    : '<?>' ;
WRITE   : '<!>' ;
REPROD  : '<:>' ;
ASSIG   : '<-' ;
PUSH    : '<<' ;
REMOVE  : '8<' ;
IF      : 'if' ;
ELSE    : 'else' ;
WHILE   : 'while' ;
GT      : '>' ;
GE      : '>=' ;
LT      : '<' ;
LE      : '<=' ;
EQ      : '=' ;
NEQ     : '/=' ;
NOTE    : ('C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B') | ('C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B') NUM ;
ID      : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
PROCNAME: ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')+ ;
NUM     : [0-9]+ ;
STRING  : '"' ( ESC_SEQ | ~('\\'|'"') )* '"' ;
fragment
ESC_SEQ : '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\') ;
SUM     : '+' ;
MINUS   : '-' ;
COMMENT : '~~~' ~('\n'|'\r')* '\r'? '~~~' -> skip ;
WS      : [ \n]+ -> skip ;
