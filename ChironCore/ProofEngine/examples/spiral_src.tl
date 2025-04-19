:step = 40

penup 
goto (-230, -230)
pendown
forward 460
left 90
forward 460
left 90
forward 460 
left 90
forward 460
left 90

penup
goto (0,0)
repeat :n [
    pendown
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 40
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 40
    penup
]