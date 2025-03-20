if (:a > 0) [
if (:z > 0) [
:x=:y+2

]

:z=:x+1

]

goto (:x, :y)
assert:turtleX<0
