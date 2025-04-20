valuefunc factorial(:x){
	if(:x == 1)[
		:y = 1
	]
	else[
		:y = get factorial(:x-1)
		:y = :y * :x
	]
	valuereturn :y
}
valuefunc countdivisors(:n){
	:count = 0
	:i=1
	repeat :n [
		if(((:n/:i)*:i)==:n)[
			:count = :count + 1
		]
		:i = :i + 1
	]
	valuereturn :count
}
valuefunc expensive(:n){
	:sum=0
	:i = 1
	repeat :n [
		:sum = :sum + get countdivisors(:i)
		:i = :i + 1
	]
	valuereturn :sum 
}
:x = 20
:y = 30
:z = 20
:p = 40

:steps = 1

pendown

repeat :steps [
	:a = get expensive(100000)
	goto(:a,:a)
]

penup