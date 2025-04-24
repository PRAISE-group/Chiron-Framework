:a = 100
:b = 50
:c = 0
pendown

repeat 3 [ 
  
  :a = :a - 20
  :b = :b + 10
  
  repeat 2 [  
    :shadow = :a * 2  
    if (:shadow > :b) [
     
      :shadow = :shadow / 2
      if(:shadow<100)[
        forward :shadow
      ]
      else[
        forward 100
      ] 
      right 45
    ] else [
     
      :shadow = :shadow + :b
       if(:shadow<100)[
        backward :shadow
      ]
      else[
        backward 100
      ] 
      left 90
    ]
    
    
    :c = :c + :shadow
    
    repeat 1 [  
     
      :a = 5
      forward :a
      :a = :a + (:shadow + 3)
      left 90
      
      if (:c > 75) [
        :b = :b - (:a * 2)
        penup
        if(:a<100 && :b<100)[
            goto (:a, :b)
        ]
        else[
            goto (0, 0)
        ]
        pendown
      ]
    ]
  ]
  
  if (:c < 200) [ 
    :temp = (:a + :b) * :c
    repeat 1 [  
      :a = :a + (:temp / 10)
      :b = :b - (:a + 5)
      :c = :c + 1
      
      if (:b < 40) [
        :temp = :temp / 2
        forward 10
      ] else [
        :temp = :temp * 2
        backward 10
      ]
    ]
  ] else [
    :d = :a * :b * :c
    repeat 1 [
      :d = :d / (:a + 1)
      right 20
      :c = :d + 10
      forward 10
    ]
  ]
  
  :a = :a + :b
  :b = :b - :c
]

if (!(:d==0)) [
  goto (0, 0)
  penup
]