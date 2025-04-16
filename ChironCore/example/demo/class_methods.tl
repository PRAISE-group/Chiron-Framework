class :Pentagon {
    :sides = 5
    :length = 250
    def drawShape(:self) {
        :angle = 360 / :self.:sides
        repeat :self.:sides [
            forward :self.:length
            right :angle
        ]
        return 0
    }
}

:pent = new :Pentagon()
:pent.drawShape()
