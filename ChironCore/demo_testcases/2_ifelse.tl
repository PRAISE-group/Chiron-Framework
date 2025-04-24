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
  :x = (:a + :b*:b + 3/2 + 8)/:a
]
:b = 5
repeat :d[
    forward 10/3
    :b = :b + 1/2
]
forward :x - 50