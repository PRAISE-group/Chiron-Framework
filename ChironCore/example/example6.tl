:x = 10
:y = 20
forward :x
if (:x > :y) [
  forward :y
] else [
  backward (:y - :x)
  :x = :x + 1
  :x = :x + 1
 ]
right 90
forward :x