assume(:i==1 && :TURTLEPEN==0 && :xstart==0 && :ystart==40 && :TURTLEANGLE==0 && :TURTLEX==:xstart && :TURTLEY==:ystart && :inriver==0)
repeat :n[
    invariant(:TURTLEX==:xstart+30*(:n-:REPCOUNTER) && :TURTLEY==:ystart+30*(:n-:REPCOUNTER) && :TURTLEPEN==0 && :i==1 && :TURTLEANGLE==0 && :inriver == 0 && :xstart == 0 && :ystart == 40)
    penup
    forward 40
    right 90
    forward 40
    pendown
    forward :i*15
    if(:TURTLEX==:TURTLEY)[
        :inriver = 1
    ]
    :i = :i +1
    penup
    forward 40
    right 90
    forward 40
    pendown
    forward :i*15
    if(:TURTLEX==:TURTLEY)[
        :inriver = 1
    ]
    :i = :i +1
    penup
    forward 40
    right 90
    forward 40
    pendown
    forward :i*15
    if(:TURTLEX==:TURTLEY)[
        :inriver = 1
    ]
    :i = :i +1
    penup
    forward 40
    right 90
    forward 40
    pendown
    forward :i*15
    if(:TURTLEX==:TURTLEY)[
        :inriver = 1
    ]
    :i = 1
]
assert(:inriver==0)