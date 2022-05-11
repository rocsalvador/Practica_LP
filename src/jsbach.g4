grammar jsbach;

root
        : procDef+ EOF ;

statements
        : (statement)*
        ;

procDef
        : PROCNAME ID* '|:' statements ':|'
        ;

string
        : STRING
        ;

writeParams
        : (string|expr)+
        ;

statement
        : IF expr '|:' statements ':|' (ELSE '|:' statements ':|')?     # if
        | WHILE expr '|:' statements ':|'                               # while
        | READ ID                                                       # read
        | ID ASSIG expr                                                 # assign                              
        | WRITE writeParams                                             # write
        | REPROD expr                                                   # reprod
        | PROCNAME expr*                                                # procCall
        | REMOVE ID '[' expr ']'                                        # remove
        | ID PUSH expr                                                  # push
        ;

note
        : NOTE 
        ;

expr
        : '(' expr ')'                          # parenthesis
        | expr (MUL|DIV|MOD) expr               # arithmetic
        | expr (SUM|MINUS) expr                 # arithmetic
        | expr (EQ|NEQ|GT|GE|LT|LE) expr        # relational
        | ID '[' expr ']'                       # arrayAccess
        | '#' ID                                # arraySize
        | '{' expr* '}'                         # arrayDecl
        | NUM                                   # intValue
        | ID                                    # id
        | note                                  # noteExpr
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
NOTE    : ('C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B') [0-8]? ;
ID      : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
PROCNAME: ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')+ ;
NUM     : [0-9]+ ;
STRING  : '"' ( ESC_SEQ | ~('\\'|'"') )* '"' ;
fragment
ESC_SEQ : '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\') ;
SUM     : '+' ;
MINUS   : '-' ;
MUL     : '*' ;
DIV     : '/' ;
MOD     : '%' ;
COMMENT : '~~~' ~('\n'|'\r')* '\r'? '~~~' -> skip ;
WS      : [ \n]+ -> skip ;