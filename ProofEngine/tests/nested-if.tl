assume(:x == 0 && :y == 0)
repeat :n[
    invariant(:x > 0)
    :x = :x + 1
    if(:x > 1)[
        :y = :x - 1
        if(:y > 5)[
            :z = :z + 1
            :w = :w - 1
        ]
        else[
            :z = :z - 1
            :w = :w + 1
        ]
    ]
    else[
        :y = :x + 1
        if(:y < 5)[
            :z = :z - 1
            :w = :w + 1
        ]
    ]
]
assert(:z > 0 && :w > 0)