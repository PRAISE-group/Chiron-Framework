:x = 100
pendown
repeat 2 [
  :x = 50
  if (:x == 50) [
    forward :x
    :x = :x + 10 
  ]
  left 30
]
penup
goto (:x, :x)  