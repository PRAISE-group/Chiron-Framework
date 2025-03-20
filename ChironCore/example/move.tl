:y = 0
repeat :a [
    :x = :y + 2
]

goto (20, :y)

assert :x > 0
assert :turtleX > 0