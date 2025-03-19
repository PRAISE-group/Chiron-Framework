pendown
:angle = 45
repeat 5 [
    forward 100
    if (:angle > 30) [
        right 90
    ] else [
        left 90
    ]
    :angle = :angle + 15
]
penup