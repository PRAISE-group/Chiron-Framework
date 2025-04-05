assume(:x==0)
repeat 4 [
    invariant(:y + :x*90 == 360)
    :x = :x + 1
    pendown
    if (:x == 4) [
        left 90
    ]
    else [
        right 90
    ]
    forward 10
    penup
]
assert(:y == 270)
