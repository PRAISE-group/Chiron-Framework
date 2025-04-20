class :Point {
    :x = 6

}

class :Circle {
    :point = new :Point()
    
}

:point = new :Point()
:circle = new :Circle()
print(:circle.:point.:x)
