assume :step > 0 && :step < 50
assume :iterations > 0

:count = 0
:inc = 2

repeat :iterations [
    forward :step

    if :count % 2 == 0 [
        left 90
    ] else [
        right 90
    ]

    :count = :count + 1
    :step = :step + :inc

    if (:count + 1) % 8 == 0 [
        :inc = - :inc
    ]
]

assert :turtleX * :turtleX + :turtleY * :turtleY <= 100
