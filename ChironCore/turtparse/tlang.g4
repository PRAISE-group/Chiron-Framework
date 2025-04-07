
grammar tlang;

start : statement_list EOF
      ;

statement_list : declaration_list strict_ilist ;

declaration_list : (declaration)* ;

strict_ilist : (instruction | comment)+
             ;

declaration : classDeclaration
		| functionDeclaration
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
		| objectInstantiation
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
		  lvalue  '=' expression      
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
		   | lvalue  '=' expression   #assignExpr
		   | '(' expression ')'                    #parenExpr
		   | value                                 #valueExpr
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

functionCallWithReturnValues : lvalue ( ',' lvalue )+ '=' functionCall ;

// function declaration
functionDeclaration : 'def' NAME '(' parameters ')' '{' strict_ilist '}' ;

parameters : ( VAR  ( ',' VAR )* )? ;
arguments : ( expression ( ',' expression )* )? ;

// TODO :
// procedure_declaration : 'to' NAME (VAR)+ strict_ilist 'end' ;

condition : NOT condition
          |expression binCondOp expression
	  | condition logicOp condition
	  | PENCOND
	  | '(' condition ')'
	  ;

comment : '#' (NAME)* '#' ;

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
	  | dataLocationAccess
	  | functionCall 							
	  | REAL
      ;

NUM  : [0-9]+        ;
REAL : [0-9]+('.'[0-9]+)?;
VAR  : ':''__'?[a-zA-Z_] [a-zA-Z0-9]* ;

NAME : '__'?[a-zA-Z]+     ;

Whitespace: [ \t\n\r]+ -> skip;
