if (:a > :b + :c) [
    :result = :a - :b
    if (:c > :a - :b) [
        :result = :result + :c - :a
        if (:result < :b - :c) [
            :result = :result + :b + :b
        ] else [
            :result = :result - :c - :c
        ]
    ] else [
        :result = :a + :c
        if (:a + :c - :b > :result) [
            :result = :result + :a - :b - :b
        ] else [
            :result = :result - :a + :b + :b
        ]
    ]
] else [
    :result = :b + :c
    if (:b + :c - :a < :a + :a) [
        :result = :result - :a - :a
        if (:result + :b > 0) [
            :result = :result + :b + :b - :c
        ] else [
            :result = :result + :c + :c - :b
        ]
    ] else [
        :result = :a + :a + :a
        if (:result - :c < :b + :b) [
            :result = :result + :b + :b + :b
        ] else [
            :result = :result - :c - :c - :c
        ]
    ]
]

goto (:result, 0)

