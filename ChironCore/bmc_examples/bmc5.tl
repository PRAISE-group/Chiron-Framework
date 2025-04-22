forward 10
left 90
forward :t              // turtle is at (10, :t)
:r = 20
assert :turtleX*:turtleX + :turtleY*:turtleY <= :r*:r
// assume -17 <= :t && :t <= 17


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc5.tl -bmc
Here, we are checking whether turtle lies in the circle of radius :r = 20. The program outputs a counter example of this case (for free variable :t). Eg: :t = -18

Now uncomment the assert statement and run this program by:
./chiron.py bmc_examples/bmc5.tl -bmc
Now, we restrict :t between [-17, 17], then the turtle does not go outside the circle and condition is satisfied.
*/
