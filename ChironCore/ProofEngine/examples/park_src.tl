penup
goto (-50,-50)
pendown
forward 100
left 90
forward 100
left 90
forward 100
left 90
forward 100
left 90

penup
goto (200,200)
pendown
forward 100
left 90
forward 100
left 90
forward 100
left 90
forward 100
left 90
penup

:step = 25

goto (13,-30)
pendown
repeat 10 [
    forward :step
    left 90
    forward :step
    right 90
]