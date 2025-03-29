//:delta = 10
//repeat 5 [
//    forward :delta
//    left 90
//    forward :delta
//    left 90
//    :delta = :delta + 10
//]
//
//:a = 29
//assert :turtleX >= -:a && :turtleX <= :a && :turtleY >= -:a && :turtleY <= :a

repeat :a [
    forward 10
]

assume :a < 1
assert :turtleX <= 1 && :turtleX >= -1 && :turtleY <= 1 && :turtleY >= -1
