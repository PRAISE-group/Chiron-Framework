:i = 1
:n = 50
repeat :n[
    if(:i == 5)[
        :i = 1
    ]
    penup
    forward 40
    left 90
    forward 40
    pendown
    forward :i*15
    :i = :i +1
]