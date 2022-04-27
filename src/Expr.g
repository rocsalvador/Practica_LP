grammar Expr;

root
        : procDef+ EOF ;


procDef
        : PROCNAME ID* '|:' statements* ':|'
        ;

statements
        : IF expr '|:' statements* ':|' (ELSE '|:' statements* ':|')?
        | WHILE expr '|:' statements ':|'
        | READ ID
        | ID ASSIG expr
        | WRITE expr+
        | REPROD
        | PROCNAME expr*
        ;

expr
        : '(' expr ')'
        | expr op=(SUM|MINUS) expr
        | expr op=(NEQ|GT|GE) expr
        | ID '[' ID ']'
        | '#' ID
        | NUM
        | ID
        | STRING
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
