:a=2
:b=3
:c = :a+:b
if(:a < :b)[
    :c = :c+1
]
else[
    :c = :c+2
]