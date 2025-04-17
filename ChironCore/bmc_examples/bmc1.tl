:y = :x * :x
assert :y >= 0


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc1.tl -bmc

In this program :x is the free input variable. Since :y is square of :x, :y is positive hence the BMC engine outputs that consition is always satified.
If we change the assert statement to :y >= 1, then the BMC gives us a counter example of :x such that :y < 1. Eg: :x = 0 is a counter example.
*/