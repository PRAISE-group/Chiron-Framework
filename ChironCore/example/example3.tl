:x = 50
:y = 100
penup
forward :x
right :y
pendown
backward 20
:z = :x + :y
goto (:x+:y+:z, :z)
left :z