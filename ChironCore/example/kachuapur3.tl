class :Point {
    :x = 6
    :y = 4
    def draw(:self)
    {
        print(:self.:x)
        return 0
    }
    def drawy(:self)
    {
        print(:self.:y)
        return 0
    }
}

class :Circle {
    :point = new :Point()
    
}

:point = new :Point()
:circle = new :Circle()
:circle1 = new :Circle()
print(:circle.:point.:x)
:circle.:point.:x = :circle.:point.:y = -100
print(:point.:x)
print(:circle.:point.:x)
print(:circle1.:point.:x)

:circle.:point.draw()

:circle1.:point.drawy()