:i = 0
:n = 50
repeat :n[
    if(:i % 4 == 0)[
        forward 78
    ]
    if(:i % 4 == 1)[
        forward 46
    ]
    if(:i % 4 == 2)[
        forward 65
    ]
    if(:i % 4 == 3)[
        forward 32
    ]
    left 90
    :i = :i +1
]