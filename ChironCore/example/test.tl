class :Shape {
    :__length = 250
    def moveForward(:self) {
        forward :self.:length
        return
    }
}

class :Polygon {
    :sides = 4
    :length = 100
}

class :Hexagon(:Polygon, :Shape) {
    :__sides = 6
    def drawHex(:self) {
        repeat :self.:__sides [
            :self.moveForward()
            right 60
        ]
        return
    }
}

:hex = new :Hexagon()
:hex.drawHex()