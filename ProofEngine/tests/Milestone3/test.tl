assume(:s==0 && :i==1)
repeat 10 [
    invariant(:s == (:i*(:i-1))/2)
    :s = :s+:i
    :i = :i+1
]
assert(:s == 55)