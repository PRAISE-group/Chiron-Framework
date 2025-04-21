
grammar tlang;

start : statement_list EOF
      ;

statement_list : declaration_list strict_ilist ;

declaration_list : (declaration)* ;

strict_ilist : (instruction | comment)*
             ;

declaration : classDeclaration
		| functionDeclaration
		;

instruction : 
		  assignment
		 | printStatement
	    | conditional
	    | loop
	    | moveCommand
	    | penCommand
	    | gotoCommand
	    | pauseCommand
		| objectInstantiation
		| returnStatement
		| functionCall
		
	    ;

conditional : ifConditional | ifElseConditional ;

ifConditional : 'if' expression '[' strict_ilist ']' ;

ifElseConditional : 'if' expression '[' strict_ilist ']' 'else' '[' strict_ilist ']' ;

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
		  lvalue  '=' expression      
	   ;

printStatement : PRINT '(' expression ')' ;

multiplicative : MUL | DIV;
additive : PLUS | MINUS;

unaryArithOp : MINUS ;



returnStatement : RETURN ( expression ( ',' expression )* ) ;

expression : 
             unaryArithOp expression               #unaryExpr
           | expression multiplicative expression  #mulExpr
		   | expression additive expression        #addExpr
		   | lvalue  '=' expression                #assignExpr
		   | '(' expression ')'                    #parenExpr
		   | value                                 #valueExpr
		   | NOT expression						   #notExpr
           | expression binCondOp expression	   #binExpr
	       | expression logicOp expression		   #logExpr
	       | PENCOND							   #penExpr


;

classDeclaration : 'class' VAR ('(' VAR (',' (VAR)*)? ')')? '{' classBody '}' ;

classBody : (classAttributeDeclaration)* (functionDeclaration)*;

classAttributeDeclaration : assignment | objectInstantiation ;

objectInstantiation : lvalue '=' 'new' VAR '(' ')' ;

dataLocationAccess : baseVar ('.' VAR | '[' expression ']')+ ;

baseVar : VAR ;

lvalue
    : VAR
    | dataLocationAccess
    ;

// function call
functionCall : methodCaller NAME '(' arguments ')' ;
methodCaller : ((VAR | '[' expression ']') '.')* ;


// function declaration
functionDeclaration : 'def' NAME '(' parameters ')' '{' strict_ilist '}' ;

parameters : ( VAR  ( ',' VAR )* )? ;
arguments : ( expression ( ',' expression )* )? ;


comment : '#' (NAME)* '#' ;

logicOp : AND | OR ;


binCondOp :  EQ | NEQ | LT | GT | LTE | GTE
	 ;


PLUS     : '+' ;
MINUS    : '-' ;
MUL  	 : '*' ;
DIV      : '/' ;

AND: '&&';
OR : '||';

RETURN : 'return' ;

PRINT : 'print' ;


PENCOND : 'pendown?';
LT : '<' ;
GT : '>' ;
EQ : '==';
NEQ: '!=';
LTE: '<=';
GTE: '>=';

NOT: '!' ;

value : NUM
      | VAR
	  | array
	  | dataLocationAccess
	  | functionCall 							
	  | REAL
      ;

NUM  : [0-9]+        ;
REAL : [0-9]+('.'[0-9]+)?;
VAR  : ':''__'?[a-zA-Z_] [a-zA-Z0-9]* ;

NAME : '__'?[a-zA-Z]+     ;

Whitespace: [ \t\n\r]+ -> skip;
