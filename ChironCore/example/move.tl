:a = 1
:y = 0
repeat :a [
    :x = :y + 2
]

goto (:x, :y)

assert :x > 0
assert :turtleX > 0