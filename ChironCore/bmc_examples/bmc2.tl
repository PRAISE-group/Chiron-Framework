:t = 1
// assume :x > 0
repeat 2 [
    :t = :t * :x
    assert :t >= 0
]


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc2.tl -bmc

In this program, :x is a free input variable. After the 1st iteration, :t = :x and after the 2nd iteration, :t = :x * :x.
In the case when assume statement is commented, :t >= 0 is violated for any :x < 0. Thus the BMC outputs a negative :x as a counter example.
In the case when assume statement is uncommented, the domain of :x is restricted among the positive real numbers. Hence, the assert consition always holds true.
*/