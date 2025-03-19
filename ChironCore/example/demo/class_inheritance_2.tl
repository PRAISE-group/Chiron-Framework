class :Shape {
    :length = 250
}

class :Hexagon(:Shape) {
    :sides = 6
    def drawHex(:self) {
        repeat :self.:sides [
            forward :self.:length
            right 60
        ]
        return
    }
}

:hex = new :Hexagon()
:hex.drawHex()
