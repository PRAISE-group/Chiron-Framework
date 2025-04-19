:step = 10

penup
goto (-150, -150)
pendown
forward 300
left 90
forward 300
left 90
forward 300 
left 90
forward 300
left 90

penup
goto (-200, -200)
pendown
forward 400
left 90
forward 400
left 90
forward 400 
left 90
forward 400
left 90

penup
goto (:xstart, :ystart)
repeat 5 [
    pendown
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 10
    forward :step
    left 90
    forward :step
    left 90
    :step = :step + 10
    penup
]