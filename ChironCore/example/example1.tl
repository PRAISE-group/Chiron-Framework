pendown

repeat 3 [

	if (:x > :y) [
		penup
		goto (:x, :y)
		pendown
		repeat 4 [
			forward :x
			left 90
		]
	] else [
		penup
		goto (:y, :x)
		pendown
		repeat 5 [
			forward :p
			left 72
		]
	]

	if (:z >= :p) [
		penup
		goto (:p, :x + :z)
		pendown
		repeat 6 [
			backward :x
			left 60
		]
	]

	:x = :x + 10
	:y = :y + 10
	:z = :z + 10
]

penup