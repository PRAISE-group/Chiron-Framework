if (:p > 0) [
    :x = 20
    :f = :x * 2 + :x
    backward :x
    // left 50
] else [
    :x = 10
]
assert :x == 20
forward :x