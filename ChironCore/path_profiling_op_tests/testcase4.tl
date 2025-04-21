pendown

repeat 3 [
    repeat 3 [
        if (:y <= :p) [
            forward :x
        ] else [
            backward :z
        ]
        right 120
    ]
    left 60
    :y = :y + 15
]

penup