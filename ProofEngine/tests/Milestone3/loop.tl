:x = :a
:s = :a

repeat :n [
    if(:n > 20)[
        :n = 30
    ] else [
        :n = 20
    ]
    :x1 = :x + :d
    :s1 = :s + :x1
    :x = :x1
    if(:n <= 25)[
        :n = 65
    ] else [
        :n = 98
    ]
    :s = :s1
]
:x = 5
:s = 342

