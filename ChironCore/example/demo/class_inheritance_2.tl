class :Shape {
    :length = 250
    def moveForward(:self) {
        forward :self.:length
        return
    }
}

class :Hexagon(:Shape) {
    :sides = 6
    def drawHex(:self) {
        repeat :self.:sides [
            :self.moveForward()
            right 60
        ]
        return
    }
    def moveForward(:self) {
        forward 100
        return
    }
}

:hex = new :Hexagon()
:hex.drawHex()