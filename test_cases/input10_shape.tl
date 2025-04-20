voidfunc drawRectangle(:x, :y, :len) {
	penup
	goto (:x, :y)
	pendown
	repeat 4 [
		forward :len
		left 90
	]
	voidreturn
}

voidfunc drawPentagon(:x, :y, :len) {
	penup
	goto (:x, :y)
	pendown
	repeat 5 [
		forward :len
		left 72
	]
	voidreturn
}

voidfunc drawHexagon(:x, :y, :len) {
	penup
	goto (:x, :y)
	pendown
	repeat 6 [
		backward :len
		left 60
	]
	voidreturn
}

:x = 20
:y = 30
:z = 20
:p = 40

:steps = 3

pendown

repeat :steps [

	if (:x > :y) [
		procedure drawRectangle(:x, :y, :x)
	] else [
		procedure drawPentagon(:y, :x, :p)
	]

	if (:z >= :p) [
		procedure drawHexagon(:p, :x + :z, :x)
	]

	:x = :x + 10
	:y = :y + 10
	:z = :z + 10
]

penup