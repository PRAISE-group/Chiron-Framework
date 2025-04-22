
// max steps = 5, max obstacles = 2

assume :s1 == 0 || :s1 == 1 || :s1 == 2 || :s1 == 3 || :s1 == 4
assume :s2 == 0 || :s2 == 1 || :s2 == 2 || :s2 == 3 || :s2 == 4
assume :s3 == 0 || :s3 == 1 || :s3 == 2 || :s3 == 3 || :s3 == 4
assume :s4 == 0 || :s4 == 1 || :s4 == 2 || :s4 == 3 || :s4 == 4
assume :s5 == 0 || :s5 == 1 || :s5 == 2 || :s5 == 3 || :s5 == 4

assume !(:s4 == 0) || (:s5 == 0)
assume !(:s3 == 0) || (:s5 == 0 && :s4 == 0)
assume !(:s2 == 0) || (:s5 == 0 && :s4 == 0 && :s3 == 0)
assume !(:s1 == 0) || (:s5 == 0 && :s4 == 0 && :s3 == 0 && :s2 == 0)

:step = 50

:length = 0

:targetX = 3 * :step
:targetY = 0 * :step

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
if (:s1 != 0) [:length = :length + 1]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s2 == 1) [forward :step]
if (:s2 == 2) [left 90 forward :step right 90]
if (:s2 == 3) [backward :step]
if (:s2 == 4) [left 90 backward :step right 90]
if (:s2 != 0) [:length = :length + 1]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s3 == 1) [forward :step]
if (:s3 == 2) [left 90 forward :step right 90]
if (:s3 == 3) [backward :step]
if (:s3 == 4) [left 90 backward :step right 90]
if (:s3 != 0) [:length = :length + 1]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s4 == 1) [forward :step]
if (:s4 == 2) [left 90 forward :step right 90]
if (:s4 == 3) [backward :step]
if (:s4 == 4) [left 90 backward :step right 90]
if (:s4 != 0) [:length = :length + 1]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

if (:s5 == 1) [forward :step]
if (:s5 == 2) [left 90 forward :step right 90]
if (:s5 == 3) [backward :step]
if (:s5 == 4) [left 90 backward :step right 90]
if (:s5 != 0) [:length = :length + 1]

assume !(:turtleX == :obs1x && :turtleY == :obs1y)
assume !(:turtleX == :obs2x && :turtleY == :obs2y)

assert !(:turtleX == :targetX && :turtleY == :targetY && :length <= 2)


/*
Similar to the path planning code, this code gives us a path that has least distance to travel.
Only the assert statement is changed. Rest of the code is same.
*/

