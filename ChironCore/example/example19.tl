:a = 100
:b = 50
:c = 0
pendown

repeat 1 [  
  :a = :a - 20
  :b = :b + 10
  
  repeat 2 [ 
    :shadow = :a * 2  
    if (:shadow > :b) [
      :shadow = :shadow / 2
      forward :shadow
      right 45
    ] else [
      :shadow = :shadow + :b
      backward :shadow
      left 90
    ]

    :c = :c + :shadow
    
    repeat 1 [  
      :a = 5
      forward :a
      :a = :a + (:shadow * 3)
      left :a
      
      if (:c > 75) [
        :b = :b - (:a * 2)
        penup
        goto (0, 0)
        pendown
      ]
    ]
  ]
 :d=:a* :b * :c
  
:a = :a + :b
  :b = :b - :c
]
if (:d >10) [ 
  goto (0, 1)
  penup
]