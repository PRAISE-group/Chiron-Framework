:cnt = 0
:i = 0
:radius=45
:steps=10
repeat :steps [
  :i = :cnt + :i
  :cnt = :cnt + 1   
  forward(1 + :cnt)
  right(:radius)
]
