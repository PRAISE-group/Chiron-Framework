
grammar tlang;

start : function_list instruction_list EOF
      ;

instruction_list : (instruction)*
		 ;

strict_ilist : (instruction)+
             ;

function_list: (function_declaration)*
        ;

function_declaration : voidFunction
        | valueFunction
        ;
		
voidFunction : 'voidfunc' NAME parametersDeclaration '{' instruction_list voidReturn '}' ;

valueFunction : 'valuefunc' NAME parametersDeclaration '{' instruction_list valueReturn '}' ;

voidReturn: 'voidreturn' ;

valueReturn: 'valuereturn' expression ;

parametersDeclaration: '(' ')'
        | '(' VAR (',' VAR)* ')'
        ;

parameterCall: '(' ')'
        | '(' expression (',' expression)* ')'
        ;
voidFuncCall: 'procedure' NAME parameterCall;

valueFuncCall: 'get' NAME parameterCall;

instruction : assignment
	    | conditional
	    | loop
	    | moveCommand
	    | penCommand
	    | gotoCommand
	    | pauseCommand
		| voidFuncCall
	    ;

conditional : ifConditional | ifElseConditional ;

ifConditional : 'if' condition '[' strict_ilist ']' ;

ifElseConditional : 'if' condition '[' strict_ilist ']' 'else' '[' strict_ilist ']' ;

loop : 'repeat' value '[' strict_ilist ']' ;

gotoCommand : 'goto' '(' expression ',' expression ')';

assignment : VAR '=' expression
	   ;

moveCommand : moveOp expression ;
moveOp : 'forward' | 'backward' | 'left' | 'right' ;

penCommand : 'penup' | 'pendown' ;

pauseCommand : 'pause' ;

expression : 
             unaryArithOp expression               #unaryExpr
           | expression multiplicative expression  #mulExpr
		   | expression additive expression        #addExpr
		   | value                                 #valueExpr
		   | '(' expression ')'                    #parenExpr
		   | valueFuncCall						   #funcExpr
 	   ;

multiplicative : MUL | DIV;
additive : PLUS | MINUS;

unaryArithOp : MINUS ;

PLUS     : '+' ;
MINUS    : '-' ;
MUL  	 : '*' ;
DIV      : '/' ;


// TODO :
// procedure_declaration : 'to' NAME (VAR)+ strict_ilist 'end' ;

condition : NOT condition
          |expression binCondOp expression
	  | condition logicOp condition
	  | PENCOND
	  | '(' condition ')'
	  ;


binCondOp :  EQ | NEQ | LT | GT | LTE | GTE
	 ;

logicOp : AND | OR ;

PENCOND : 'pendown?';
LT : '<' ;
GT : '>' ;
EQ : '==';
NEQ: '!=';
LTE: '<=';
GTE: '>=';
AND: '&&';
OR : '||';
NOT: '!' ;

value : NUM
      | VAR
      ;

NUM  : [0-9]+        ;

VAR  : ':'[a-zA-Z_] [a-zA-Z0-9]* ;

NAME : [a-zA-Z]+     ;

Whitespace: [ \t\n\r]+ -> skip;
