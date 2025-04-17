class :Shape {
    :length = 250
}

class :Triangle(:Shape) {
    :sides = 3
}

:tri = new :Triangle()
:count = 0
repeat :tri.:sides [
    forward :tri.:length
    right 120
    :count = :count + 1
]
