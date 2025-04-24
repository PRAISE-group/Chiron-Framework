:x = 0
repeat 2 [
  if (:x < 5) [
    :x = :x + 1
    if (:x - 2 == 0) [
      :x = :x * 2
      repeat :x [
        :x = :x - 1  
        forward :x + 20
      ]
    ]
  ]
]