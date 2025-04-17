:r = 1
repeat 4 [
    :r = :r * :x
]

:s = 1
@unroll 6 repeat :m [
    if (:m % 2 == 0) [
        :s = :s * :x
    ] else [
        repeat 3 [
            :s = :s * 2 * :x
        ]
    ]
]

:z = 5*:r - 7*:s
assert :z > -1000


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc3.tl -bmc -ub 3
This would give an error because the 1st loops iterates 4 times, which is more the specified unroll bound 3. So, we loosen the bound.

Run this program by:
./chiron.py bmc_examples/bmc3.tl -bmc -ub 7
In this case, there exists a counter example (for free input variable :x and :m) to the condition that gets printed.
Eg: take :x = 3 and :m = 1.
*/