repeat 3 [
    repeat 4 [
        :x = :y + 2
    ]
    :z = :x + 1
]

assert :y >= :x

