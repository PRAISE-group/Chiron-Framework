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
            :self.moveForward(1000)
            right 60
        ]
        return
    }
    def moveForward(:self, :distance) {
        forward :distance
        return
    }
}

:hex = new :Hexagon()
:hex.drawHex()