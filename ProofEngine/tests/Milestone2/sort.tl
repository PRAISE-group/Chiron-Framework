assume(1==1)
if (:x > :y)[
    :t = :x
    :x = :y
    :y = :t
] 
if (:y > :z)[
    :t = :y
    :y = :z
    :z = :t
] 
if (:x > :y)[
    :t = :x
    :x = :y
    :y = :t
]
assert((:x <= :y) && (:y <= :z))