def draw(:r) {

    :circumference = 2 * 3.14 * :r
    :steps = 36
    :stepLength = :circumference / :steps
    :turnAngle = 360 / :steps
    
    repeat :steps [
        forward(:stepLength)
        right(:turnAngle)
    ]
    return 0

}

def draw(:w, :h) {
    forward(:w)
    right(90)
    forward(:h)
    right(90)
    forward(:w)
    right(90)
    forward(:h)
    right(90)
    return 0
}

def draw(:a, :b, :c) {
    forward(:a)
    right(120)
    forward(:b)
    right(120)
    forward(:c)
    right(120)
    return 0
}


draw(100)
draw(100,100)
draw(100,100,100)