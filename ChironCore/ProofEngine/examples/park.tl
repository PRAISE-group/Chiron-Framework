assume(:xstart <= 100 && :ystart <= 100 && :xstart >= -100 && :ystart >= -100 && :TURTLEX == :xstart && :TURTLEY == :ystart && :TURTLEANGLE == 0 && :step == 50)
repeat 10 [
    invariant (:TURTLEX == :xstart+50*(10-:REPCOUNTER) && :TURTLEY == :ystart+50*(10-:REPCOUNTER) && :step == 50 && :TURTLEANGLE == 0 && :xstart <= 100 && :ystart <= 100 && :xstart >= -100 && :ystart >= -100)
    forward :step
    left 90
    forward :step
    right 90
]
assert((:TURTLEX <= 600 && :TURTLEX >= 400) && (:TURTLEY <=600 && :TURTLEY >= 400) && :TURTLEANGLE==0 && :xstart <= 100 && :ystart <= 100 && :xstart >= -100 && :ystart >= -100)