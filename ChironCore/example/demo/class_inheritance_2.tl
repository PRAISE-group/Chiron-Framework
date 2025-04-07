class :Shape {
    :length = 250
    def moveForward(:self) 
    {
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
    def __moveForward(:self, :distance) {
        forward :distance
        return
    }
}

:hex = new :Hexagon()
:hex.drawHex()
# This does not work #
:hex.__moveForward(100) 