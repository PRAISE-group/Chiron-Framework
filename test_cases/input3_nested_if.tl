:x = 4
:y = 5
:z = 6
if :x < :y [
  :x = :x + 3
  if (:x < :z) [
    :x = :x + 6
  ]
  else [
    :z = :z + 1
  ]
]
else [
    :y = :y + 2
]


