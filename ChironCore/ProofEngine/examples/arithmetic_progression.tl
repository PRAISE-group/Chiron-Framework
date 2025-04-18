assume((:s==0) && (:i==0))
repeat :n [
    invariant(:s == (:i*(:i+1))/2 && :REPCOUNTER + :i == :n)
    :i = :i+1
    :s = :s+:i
]
assert(:s == (:n*(:n+1))/2)