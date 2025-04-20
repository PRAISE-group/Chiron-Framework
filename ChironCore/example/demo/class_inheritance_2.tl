class :Shape {
    :length = 250
    def moveForward(:self) 
    {
        forward :self.:length
        return 0
    }
}

class :Hexagon(:Shape) {
    :sides = 6
    def drawHex(:self) {
        repeat :self.:sides [
           :f=  :self.moveForward()
            right 60
        ]
        return 0
    }
    def __moveForward(:self, :distance) {
        forward :distance
        return 0
    }
}

:hex = new :Hexagon()
:f= :hex.drawHex()
# This does not work #
:f= :hex.__moveForward(100) 