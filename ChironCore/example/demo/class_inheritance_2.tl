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
}

:hex = new :Hexagon()
:hex.drawHex()