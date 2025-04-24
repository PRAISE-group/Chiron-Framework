:x = 10
:y = 20
pendown
repeat 3 [
  if (:x < :y) [
    repeat 2 [
      forward :x
      right 90
      :x = :x + 5
    ]
  ] else [
    goto (:x, :y)
    pendown
    repeat 4 [
      left 45
      backward :y
      :y = :y - 2
    ]
  ]
  :x = :x * 2
  :y = :y / 2
]
penup