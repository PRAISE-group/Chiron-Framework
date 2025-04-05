@unroll 5
repeat :a [
    forward 10
    if (:a < 2) [
        :y = 3
    ]
]
repeat :a [
    forward 10
    if (:a < 2) [
        :y = 3
    ]
]

assert :turtleX <= 1 && :turtleX >= -1 && :turtleY <= 1 && :turtleY >= -1
