// left 90          // valid
// assert 1 > 0     // true

// left 45          // invalid
// assert 1 > 0     // true

// left 90          // valid
// assert 1 < 0     // flase

// left 45          // invalid
// assert 1 < 0     // flase

repeat 3 [
    left 90
]

assert :turtleX == 0