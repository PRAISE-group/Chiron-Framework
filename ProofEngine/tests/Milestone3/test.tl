assume((:s==0) && (:i==0))
repeat 10 [
    invariant(:s == (:i*(:i+1))/2 && :REPCOUNTER + :i == :n)
    :i = :i+1
    :s = :s+:i
]
assert(:s == 55)