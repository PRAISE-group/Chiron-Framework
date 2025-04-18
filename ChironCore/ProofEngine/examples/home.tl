assume(:xstart <= 150 && :ystart <= 150 && :xstart >= -150 && :ystart >= -150 && :TURTLEX == :xstart && :TURTLEY == :ystart && :TURTLEANGLE == 0 && :step == 10 && :TURTLEPEN == 1 && :n >= 0 && :outgone == 0)
repeat 5 [
    invariant(
            (
                (:TURTLEX <= 200 && :TURTLEX >= -200 && :TURTLEY <= 200 && :TURTLEY >= -200 && :outgone == 0) || ((:TURTLEX > 200 || :TURTLEX < -200 || :TURTLEY > 200 || :TURTLEY < -200) && :outgone == 1)
            ) && 
            
            (:TURTLEX == :xstart+10*(:REPCOUNTER-5) && :TURTLEY == :ystart+10*(:REPCOUNTER-5) && :step == 110-20*:REPCOUNTER && :TURTLEANGLE == 0 && :TURTLEPEN == 1 && :step > 0 && :xstart <= 150 && :ystart <= 150 && :xstart >= -150 && :ystart >= -150)
        )
    pendown
    forward :step
    if(:TURTLEX > 200 || :TURTLEX < -200 || :TURTLEY > 200 || :TURTLEY < -200)[
        :outgone = 1
    ]
    left 90
    forward :step
    if(:TURTLEX > 200 || :TURTLEX < -200 || :TURTLEY > 200 || :TURTLEY < -200)[
        :outgone = 1
    ]
    left 90
    :step = :step + 10
    forward :step
    if(:TURTLEX > 200 || :TURTLEX < -200 || :TURTLEY > 200 || :TURTLEY < -200)[
        :outgone = 1
    ]
    left 90
    forward :step
    if(:TURTLEX > 200 || :TURTLEX < -200 || :TURTLEY > 200 || :TURTLEY < -200)[
        :outgone = 1
    ]
    left 90
    :step = :step + 10
    if(:TURTLEX > 200 || :TURTLEX < -200 || :TURTLEY > 200 || :TURTLEY < -200)[
        :outgone = 1
    ]
    penup
]
assert(:outgone != 1)