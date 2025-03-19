class :Shape {
    :length = 250
}

class :Star(:Shape) {
    :points = 5
    def drawStar(:self) {
        :angle = 144
        repeat :self.:points [
            forward :self.:length
            right :angle
        ]
        return
    }
}

def drawSquare(:size) {
    repeat 4 [
        forward :size
        right 90
    ]
    return
}

:star = new :Star()
:star.drawStar()
penup
goto(-25, 100)
pendown
:size = 300
drawSquare(:size)
