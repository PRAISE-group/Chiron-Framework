pendown

repeat 2 [
    if (:x < :z) [
        forward :x
        left 30
    ] else [
        forward :p
        right 60
    ]
    if (:y >= :p) [
        backward :z
        right 45
    ] else [
        forward :y
        left 45
    ]
    :x = :x + 10
    :z = :z - 5
]

repeat 3 [
    forward (:x + :y)
    left 120
]

penup