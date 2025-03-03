class :Point {
    :x = 6
    :y = 4
}

class :Circle {
    :point = new :Point()
}

:point = new :Point()
:circle = new :Circle()
print(:circle.:point.:x)
:circle.:point.:x = :circle.:point.:y = 0
print(:point.:x)
print(:circle.:point.:x)

