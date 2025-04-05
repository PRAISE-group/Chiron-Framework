:a = -1
:y = 0
if (:a > 0) [
    :x = :y + 2
]
if (:a > 1) [
    :x = :y + 3
]
goto (:x, :y)
assert :turtleX == 2 && :turtleY == 0
right :x
assert :x > 0
assert :turtleX > 0
