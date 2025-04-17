:r = 1
repeat 7 [
    :r = :r * :x
]
// :r = :x ** 7

:s = 1
@unroll 4 repeat :m [
    :s = :s * :x
]
/*
Here, :m <= 4 (since unroll bound is 4 for this loop)
:s = 1 if :m = 0
:s = :x ** :m if :m > 0
*/

:z = 5*:r - 7*:s              // :z = 5*(:x ** 7) - 7*(:x ** :m)
assert :z < -100


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc3.tl -bmc -ub 5
This would give an error because the 2nd loops iterates 7 times, which is more the specified unroll bound 5. So, we loosen the bound.

Run this program by:
./chiron.py bmc_examples/bmc3.tl -bmc -ub 7
In this case, there exists a counter example (for free input variable :x and :m) to the condition that gets printed.
Eg: take :x = 0 and :m = 0. Thus, :z = -7 >= -100
*/