:counter = 1
repeat 5 [
    :half = (:counter / 2) * 2
    if :half == :counter [
        :result = :counter * 2
    ] else [
        :result = :counter + 10
    ]
    :counter = :counter + 1
]
