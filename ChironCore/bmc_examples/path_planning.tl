
// max steps = 5, max obstacles = 2

assume :s1 == 0 || :s1 == 1 || :s1 == 2 || :s1 == 3 || :s1 == 4
assume :s2 == 0 || :s2 == 1 || :s2 == 2 || :s2 == 3 || :s2 == 4
assume :s3 == 0 || :s3 == 1 || :s3 == 2 || :s3 == 3 || :s3 == 4
assume :s4 == 0 || :s4 == 1 || :s4 == 2 || :s4 == 3 || :s4 == 4
assume :s5 == 0 || :s5 == 1 || :s5 == 2 || :s5 == 3 || :s5 == 4

:step = 50

:targetX = 3 * :step
:targetY = 5 * :step

:obs1x = 1 * :step
:obs1y = 1 * :step

:obs2x = 0 * :step
:obs2y = 1 * :step

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s1 == 1) [forward :step]
if (:s1 == 2) [left 90 forward :step right 90]
if (:s1 == 3) [backward :step]
if (:s1 == 4) [left 90 backward :step right 90]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s2 == 1) [forward :step]
if (:s2 == 2) [left 90 forward :step right 90]
if (:s2 == 3) [backward :step]
if (:s2 == 4) [left 90 backward :step right 90]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s3 == 1) [forward :step]
if (:s3 == 2) [left 90 forward :step right 90]
if (:s3 == 3) [backward :step]
if (:s3 == 4) [left 90 backward :step right 90]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s4 == 1) [forward :step]
if (:s4 == 2) [left 90 forward :step right 90]
if (:s4 == 3) [backward :step]
if (:s4 == 4) [left 90 backward :step right 90]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s5 == 1) [forward :step]
if (:s5 == 2) [left 90 forward :step right 90]
if (:s5 == 3) [backward :step]
if (:s5 == 4) [left 90 backward :step right 90]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

assert !(:turtleX == :targetX && :turtleY == :targetY)


/*
This code assumes that the turtle can move in a 2D grid in 4 directions, moving :steps amount of distance at a time.
We check whether there is a path from (0, 0) to (:targetX, :targetY) that is reachable in at most 5 steps, also avoiding the 2 obstacles.
In each step, turtle decides to not move or move in +x, +y, -x, -y directions (corresponding to values 0, 1, 2, 3, 4 respectively).
We assert that the turtle is unable to reach the target. If there exists a path then the assertion is false and BMC returns a path.
*/

