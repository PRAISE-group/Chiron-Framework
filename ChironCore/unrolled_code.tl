:a=1
:y=0
if (:a > 0) [
:x=:y+2

]
if (:a > 1) [
:x=:y+2

]

goto (:x, :y)
assert:x>0
assert:turtleX>0
