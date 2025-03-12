:counter = 0
:step = 20
if (:step == 20) [
  forward 200
  right 90
  forward 200
]
:total = :counter + :step
goto (:total, 150)
pendown
penup