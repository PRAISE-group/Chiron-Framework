:x = 0
:y = 10

repeat 3 [ 
  if (:x < :y) [ 
    :x = :x + 2
    if (:x - 2 == 0) [
      forward :x
    ] else [
      backward :y
    ]
  ] else [
    :y = :y - 1
  ]
]
penup
goto (:x, :y)