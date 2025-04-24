:delta=10
:i = 0
repeat 8 [
  :i = 1 + :i
  right(90)
  forward(:delta * :i)
]
