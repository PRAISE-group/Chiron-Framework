:a = 2
:y = 0
:x = 0

if (:a > 0) [
    :x = :y + 45
]
if (:a > 1) [
    :x = :y + 135
]

// :x = 135, :y = 0

assert :turtleX == 0 && :turtleY == 0

goto (:x, :y)
right :x

assert :turtleX == 135 && :turtleY == 0


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc4.tl -bmc
This gives error because right :x rotates turtle by 135 deg, which is not in default angle.

Run this program by:
./chiron.py bmc_examples/bmc4.tl -bmc -aconf angles.conf
In this case, 135 deg is in angle.conf and thus all conditions are satisfied.
*/