:step = 70
repeat 5 [
    pendown
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 70
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 70
    penup
]