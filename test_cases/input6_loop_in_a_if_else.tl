:counter = 5
if :counter > 0 [
    repeat 3 [
        :counter = :counter - 1
    ]
] else [
    repeat 2 [
        :counter = :counter + 1
    ]
]
