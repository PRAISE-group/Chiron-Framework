:x = 5
:a = 10
:b = :a - 10
:c = 10
:d = 50
if (:a > :b) [
  if (:c < :d) [
    :x = :c * :d
    :c = :d
    :d = :c
    :c = :d
  ]
] else [
  :x = :a - :b
]
forward :x