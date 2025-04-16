:p = 1

repeat 5 [
    :t = :t * :x
]

:q = 1
repeat 4 [
    :q = :q * :x
]

:r = 1
repeat 7 [
    :r = :r * :x
]

:s = 1

repeat :o [
    :s = :s * :x
    :o = :o - 1
]

:z = 2*:p - 3*:q + 5*:r - 7*:s
assert :z < -10000

