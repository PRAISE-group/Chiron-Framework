:x = 0
:y = 100
:z = 39
repeat 3 [ 
  if (:x < :y) [ 
    :uninit = 10
    :x = :x + 2
    if (:x - 2 == 0) [
      forward :x
    ] else [
      backward :y
      :t = 90
      left :t
      :y = :y - 1
    ]
    right 90
    backward :x
  ]
  forward :uninit  
  ]
penup
goto (:x, :y)
pendown
repeat 4[
    forward :z
    right 90
]