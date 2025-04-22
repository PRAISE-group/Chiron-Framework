assume :t > 0
assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)

repeat 7 [
    pendown
    assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)

    forward :t
    assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)

    left 45
    assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)

    penup
    assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)

    forward :t
    assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)

    left 45
    assert !(:turtleX*:turtleX + :turtleY*:turtleY > 20*20 && :turtlePen == 0)
]


/*
Explaination:

Run this program by:
./chiron.py bmc_examples/bmc6.tl -bmc -aconf angles.conf

Consider the circle of radius 20 and center at (0,0)
Note that assert condition is not(turtle outside circle and pendown). We place the condition after every instruction.
So, we are asserting that turtle should not draw anything outside circle at any instance.

But for large :t, turtle draws outside circle and a counter example of free input variable :t is given by BMC.
Eg: :t = 21
*/