pendown

if (:x < :z) [
    penup
    goto (:x, :z)
    pendown
    repeat 4 [
        forward :y
        right 90
    ]
] else [
    penup
    goto (:z, :x)
    pendown
    repeat 5 [
        forward :p
        left 72
    ]
]

penup