:x1 = 3
:y1 = 4
repeat :x1 [
    :x1 = :x1 - 1
    :y1 = :y1 - 1
]
forward (:x1 + 1 + :y1 + 1)