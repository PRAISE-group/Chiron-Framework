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
:inp = 100000
pendown
repeat 20000[
goto(get factorial(:inp),0)
]
goto(0,100)
pendown