if :a > :b [
    :x = :a
] else [
    :x = :b - 2
]

if :a > :b [
    :y = :b - 1
] else [
    :y = :a + 100
]

assert :x >= :y
