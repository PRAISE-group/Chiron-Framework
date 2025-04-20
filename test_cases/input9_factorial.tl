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
pendown
goto(get factorial(:inp),0)
pendown