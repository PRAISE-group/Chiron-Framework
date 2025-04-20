def drawSide(:length) {
    forward :length
    right 90
    return 0
}
def drawSide(:length,:righti) {
    forward :length
    right :righti
    return 0
}

:length = 250
:righti = 45
:f= drawSide(:length)
:f= drawSide(:length,:righti)
:f= drawSide(:length)
