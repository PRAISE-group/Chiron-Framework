def drawSquare(:x, :y, :len) {
    penup
    goto(:x - :len/2, :y + :len/2)
    pendown
    repeat 4 [
        forward :len
        right 90
    ]
    return 0
}

def drawTree(:x, :y, :len, :depth, :spread) {
    drawSquare(:x, :y, :len)

    if :depth > 1 [
        :dy = 80
        :nextY = :y - :dy
        :offset = :spread / 2

        :lx = :x - :offset

        penup
        goto(:x, :y - :len/2)
        pendown
        goto(:lx, :nextY + :len/2)

        drawTree(:lx, :nextY, :len, :depth - 1, :spread / 2)

        goto(:x, :y - :len/2)

        :rx = :x + :offset

        penup
        goto(:x, :y - :len/2)
        pendown
        goto(:rx, :nextY + :len/2)

        drawTree(:rx, :nextY, :len, :depth - 1, :spread / 2)

        goto(:x, :y - :len/2)
    ]
    return 0
}

drawTree(0, 250, 40, 4, 240)
