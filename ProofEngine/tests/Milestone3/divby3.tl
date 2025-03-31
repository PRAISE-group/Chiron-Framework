:s = 0
repeat :k[
    :x = :n - ((:n/10)*10)
    :s1 = :s + :x
    :n1 = :n/10
    :n = :n1
    :s = :s1
]
if((:s - ((:s/3)*3)) == 0)[
    :ans = 1
] else[
    :ans = 0
]
