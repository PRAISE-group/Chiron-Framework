:cnt = 0
:i = 0
repeat 22 [
  :i = :cnt + :i
  :cnt = :cnt + 1   
  forward(20 + :i)
  right(:radius)
]
