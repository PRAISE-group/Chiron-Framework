:step = 10
:rot  = 45
:dist = 20
forward :step
right :rot
forward :dist
penup
forward :step + :dist
pendown
left 90