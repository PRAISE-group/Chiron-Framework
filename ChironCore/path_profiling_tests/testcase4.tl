pendown
:counter = 0
repeat 3 [
    if (:counter < 2) [
        repeat 4 [
            forward 50
            right 90
        ]
    ] else [
        repeat 3 [
            forward 70
            right 120
        ]
    ]
    :counter = :counter + 1
    right 30
]
penup