class :__Node {
    :x = 0
    :y = 0
}


def drawV(:__x, :__y, :__r) {
    penup
    goto(:__x - :__r, :__y + :__r)
    pendown
    goto(:__x, :__y - :__r)
    goto(:__x + :__r, :__y + :__r)
    return 0
}

def drawSquare(:__x, :__y, :__r) {
    penup
    goto(:__x - :__r, :__y + :__r)
    pendown
    repeat 4 [
        forward (2 * :__r)
        right 90
    ]
    return 0
}

def drawLine(:__x1, :__y1, :__x2, :__y2) {
    penup
    goto(:__x1, :__y1)
    pendown
    goto(:__x2, :__y2)
    return 0
}


def saveNode(:__x, :__y,:__allNodes,:cnt) {
    :__n = new :__Node()
    :__n.:x = :__x
    :__n.:y = :__y
    :__allNodes[:cnt]=:__n
    return 0
}

def crossNode(:__x, :__y, :__r) {
    drawLine(:__x - :__r, :__y + :__r, :__x + :__r, :__y - :__r)
    drawLine(:__x - :__r, :__y - :__r, :__x + :__r, :__y + :__r)
    return 0
}


def drawTree(:__x, :__y, :__r, :__depth, :__spread, :__allNodes,:cnt) {
    drawSquare(:__x, :__y, :__r)
    saveNode(:__x, :__y,:__allNodes,:cnt)
    if :__depth > 1 [
        :__offset = :__spread / 2
        :__dy = 80
        :__lx = :__x - :__offset
        :__rx = :__x + :__offset
        :__cy = :__y - :__dy
        drawLine(:__x - :__r, :__y - :__r, :__lx - :__r, :__cy + :__r)
        drawLine(:__x + :__r, :__y - :__r, :__rx + :__r, :__cy + :__r)
        drawTree(:__lx, :__cy, :__r, :__depth - 1, :__spread / 2, :__allNodes,2*:cnt+1)
        drawTree(:__rx, :__cy, :__r, :__depth - 1, :__spread / 2, :__allNodes,2*:cnt+2)
    ]
    return 0
}

def dfsmark(:node, :__allNodes, :target) {
    if :node >=7 [  
        return 0
    ]

    :cur = :__allNodes[:node]
    
    if :cur.:x == :target.:x && :cur.:y == :target.:y [
        crossNode(:cur.:x, :cur.:y, 20)
        return 1
    ]

    drawV(:cur.:x, :cur.:y, 20)

    :lhs = 2 * :node + 1
    :rhs = 2 * :node + 2
    


    if dfsmark(:lhs, :__allNodes, :target) == 1 [
        return 1
    ]
   
    if  dfsmark(:rhs, :__allNodes, :target)== 1 [
        return 1
    ]

    return 0
}



:n = new :__Node()

:__allNodes = [:n, :n , :n, :n , :n, :n , :n ]

:cnt = 0
drawTree(0, 250, 20, 3, 240,:__allNodes,:cnt)

:target = new :__Node()

:target.:x=:__allNodes[3].:x
:target.:y=:__allNodes[3].:y


:r= dfsmark(0,:__allNodes,:target)

print(:r)

