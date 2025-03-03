
grammar tlang;

start : instruction_list EOF
      ;

instruction_list : (instruction)*
		 ;

strict_ilist : (instruction)+
             ;

instruction : functionCallWithReturnValues
		| assignment
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
		   | functionCall 							#functionCallExpr

 	   ;


classDeclaration : 'class' VAR '{' classBody '}' ;

classBody : (classAttributeDeclaration)* (functionDeclaration)*;

classAttributeDeclaration : assignment | objectInstantiation ;

objectInstantiation : ( VAR | objectOrArrayAccess) '=' 'new' VAR '(' ')' ;

objectOrArrayAccess : baseAccess ('.' VAR | '[' expression ']')+ ;

baseAccess : VAR ;

// function call
functionCall : NAME '(' arguments ')' ;

functionCallWithReturnValues : ( VAR | objectOrArrayAccess) ( ',' ( VAR | objectOrArrayAccess) )+ '=' functionCall ;

// function declaration
functionDeclaration : 'def' NAME '(' parameters ')' '{' strict_ilist '}' ;

parameters : ( ( VAR | Self ) ( ',' VAR )* )? ;
arguments : ( expression ( ',' expression )* )? ;

Self : 'self' ;

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
REAL : [0-9]+('.'[0-9]+)?;
VAR  : ':'[a-zA-Z_] [a-zA-Z0-9]* ;

NAME : [a-zA-Z]+     ;

Whitespace: [ \t\n\r]+ -> skip;
