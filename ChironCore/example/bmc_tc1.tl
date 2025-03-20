:t = 1
repeat 2 [
    :t = :t * :x
]
:s = 5 * :x
:z = :t + :s + 2
assert :z >= -5
