assume(:TURTLEX == 0 && :TURTLEY == 0 && :TURTLEANGLE == 0 && :step == 1 && :TURTLEPEN == 1 && :n >= 0)
repeat :n [
    invariant(:TURTLEX == :REPCOUNTER-:n && :TURTLEY == :REPCOUNTER-:n && (:step == ((2*:n) + 1)-2*:REPCOUNTER) && :TURTLEANGLE == 0 && :TURTLEPEN == 1 && :step > 0)
    pendown
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 1
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 1
    penup
]
assert(:TURTLEX<5 && :TURTLEX>-5 && :TURTLEY<(:n+1) && :TURTLEY>(-:n-1) && :TURTLEPEN == 1 && :TURTLEANGLE == 0 && :step == ((2*:n) + 1))