if (:a > 1) [
    :y = 1
] else [
    :y = 0
    if (:b < 1) [
        :x = 1
    ] else [
        :x = 2
    ]
]

if (:c == 1) [
    :x = 2
]

assert(:x > 0)
assert(:y > 0)
