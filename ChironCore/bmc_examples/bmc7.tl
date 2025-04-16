// left 90          // valid
// assert 1 > 0     // true

// left 45          // invalid
// assert 1 > 0     // true

// left 90          // valid
// assert 1 < 0     // flase

// left 45          // invalid
// assert 1 < 0     // flase

// repeat 3 [
//     left 90
// ]

forward 10
// assume :turtleX <= 5
assert :turtleX == 10

@unroll 50 repeat :turtleX [
    :x = :x + 1
]

assert :x <= 100

