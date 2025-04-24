:x = 50
:y = 100
pendown
forward :x
right :y
pendown
backward 20
:z = :x + :y
left :z
:x = 25
forward :x
:x = :x + (1/3)
forward :x
:x = :x + (1/3)
forward :x
:x = :x + (1/3)
forward :x
:x = :x + (1/3)
forward :x
goto (:x, :x)