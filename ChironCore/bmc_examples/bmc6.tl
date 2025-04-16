assume :a < 0
if (:b > 0) [
    :a = 1
    assert :a == 1
]
forward :a
assert :turtleX > 0
