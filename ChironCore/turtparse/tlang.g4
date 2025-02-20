
grammar tlang;

start : instruction_list EOF
      ;

instruction_list : (instruction)*
		 ;

strict_ilist : (instruction)+
             ;

instruction : assignment
		| printStatement
	    | conditional
	    | loop
	    | moveCommand
	    | penCommand
	    | gotoCommand
	    | pauseCommand
		| classDeclaration
		| objectInstantiation
		| functionDeclaration
		| functionCall
		| functionCallWithReturnValues
		| returnStatement
	    ;

conditional : ifConditional | ifElseConditional ;

ifConditional : 'if' condition '[' strict_ilist ']' ;

ifElseConditional : 'if' condition '[' strict_ilist ']' 'else' '[' strict_ilist ']' ;

loop : 'repeat' value '[' strict_ilist ']' ;

gotoCommand : 'goto' '(' expression ',' expression ')';

moveCommand : moveOp expression ;
moveOp : 'forward' | 'backward' | 'left' | 'right' ;

penCommand : 'penup' | 'pendown' ;

pauseCommand : 'pause' ;

array
 : '[' ( expression ( ',' expression )* )? ']'
 ;

assignment : 
		  ( VAR | objectOrArrayAccess )  '=' expression      
	   ;

printStatement : 'print' '(' expression ')' ;

multiplicative : MUL | DIV;
additive : PLUS | MINUS;

unaryArithOp : MINUS ;

PLUS     : '+' ;
MINUS    : '-' ;
MUL  	 : '*' ;
DIV      : '/' ;


returnStatement : 'return' ( expression ( ',' expression )* )? ;

expression : 
             unaryArithOp expression               #unaryExpr
           | expression multiplicative expression  #mulExpr
		   | expression additive expression        #addExpr
		   | '(' expression ')'                    #parenExpr
		   | value                                 #valueExpr
	       | ( VAR | objectOrArrayAccess)  '=' expression   #assignExpr

 	   ;


classDeclaration : 'class' VAR '{' classBody '}' ;

classBody : (classAttributeDeclaration)* ;

classAttributeDeclaration : assignment ';' ;

objectInstantiation : ( VAR | objectOrArrayAccess) '=' 'new' VAR '(' ')' ;

objectOrArrayAccess : baseAccess ('.' VAR | '[' expression ']')+ ;

baseAccess : VAR ;

// function call
functionCall : NAME '(' arguments ')' ;

functionCallWithReturnValues : VAR ( ',' VAR )* '=' functionCall ;

// function declaration
functionDeclaration : 'def' NAME '(' parameters ')' '{' strict_ilist '}' ;

parameters : ( VAR ( ',' VAR )* )? ;
arguments : ( expression ( ',' expression )* )? ;


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
	  | array
	  | objectOrArrayAccess
	  | REAL
      ;

NUM  : [0-9]+        ;
REAL : [+-]?[0-9]+('.'[0-9]+)?;
VAR  : ':'[a-zA-Z_] [a-zA-Z0-9]* ;

NAME : [a-zA-Z]+     ;

Whitespace: [ \t\n\r]+ -> skip;
