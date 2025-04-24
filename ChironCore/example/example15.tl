:x = 10
repeat 3 [
  :x = 20  
  repeat 2 [
    :x = :x + 5  
    forward :x
  ]
  right :x 
]