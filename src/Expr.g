grammar Expr;

root
        : procDef+ EOF ;


procDef
        : PROCNAME ID* '|:' statements ':|'
        ;

statements
        : IF expr '|:' (statements)+ ':|'
        | WHILE expr '|:' statements ':|'
        | READ ID
        | ID ASSIG expr
        | WRITE expr
        | REPROD
        | PROCNAME expr*
        ;

expr
        : '(' expr ')'
        | expr op=(SUM|MINUS) expr
        | ID '[' ID ']'
        | '#' ID
        | NUM
        | ID
        ;

READ    : '<?>' ;
WRITE   : '<!>' ;
REPROD  : '<:>' ;
ASSIG   : '<-' ;
PUSH    : '<<' ;
REMOVE  : '8<' ;
IF      : 'if' ;
WHILE   : 'while' ;
NOTE    : ('C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B') | ('C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B') NUM ;
ID      : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
PROCNAME: ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')+ ;
NUM     : [0-9]+ ;
SUM     : '+' ;
MINUS   : '-' ;
WS      : [ \n]+ -> skip ;
