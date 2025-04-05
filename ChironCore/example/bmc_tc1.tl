:t = 1
assume :x > 0
repeat 2 [
    :t = :t * :x
    assert :t > 0
]
:s = 5 * :x
:z = :t + :s + 2
// assert :z >= -5


// cant do the following
// if (b > 0) [    // :a is not defined earlier
//     :a = 1    
// ]
// forward :a