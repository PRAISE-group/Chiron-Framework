assume(1==1)
if (:x > 0)[
    :sign = 1
] else [
    :sign = 0
]
if (:x < 0)[
    :sign = -1
]
assert((:x > 0 && :sign == 1) || (:x < 0 && :sign < 0) || (:x == 0 && :sign == 0))