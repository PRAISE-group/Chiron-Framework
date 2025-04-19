assume(:s==0 && :i==:a)
repeat :n [
    invariant(:s == (((:n-:REPCOUNTER)*(2*:a + (:n-:REPCOUNTER-1)*:d))/2) && (:i == :a + (:n-:REPCOUNTER)*:d) )
    :s = :s + :i
    :i = :i + :d
]
assert(:s == ((:n*(2*:a + (:n-1)*:d))/2))