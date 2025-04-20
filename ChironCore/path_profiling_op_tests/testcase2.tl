pendown

repeat 2 [
    if (:x > :y) [
        repeat 3 [
            forward :p
            right 120
        ]
    ] else [
        repeat 4 [
            forward :z
            left 90
        ]
    ]
    :x = :x - 5
    :z = :z + 5
]

penup