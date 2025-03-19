if (:x > :y)[
    :x1 = :y
] else [
    :x1 = :x
]
if (:x > :y)[
    :y1 = :x
] else [
    :y1 = :y
]
if (:y1 > :z)[
    :y2 = :z
] else [
    :y2 = :y1
]
if (:y1 > :z)[
    :z1 = :y1
] else [
    :z1 = :z
]
if (:x1 > :y2)[
    :x2 = :y2
] else [
    :x2 = :x1
]
if (:x1 > :y2)[
    :y3 = :x1
] else [
    :y3 = :y2
]
