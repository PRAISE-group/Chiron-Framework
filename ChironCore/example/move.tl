:a = 2

repeat :a [
    forward 50
    :a = :a - 2
]

assert :turtleX == 50