def drawRectangle(:l, :b)
{
    if :l <= 42 [
        :b = :b + 40
    ] else [
        :b = :b + 22
    ]
    return
}

def drawCircle()
{
    :r = 10
    :p1 = 1
    :p2 = 1
    if :p1 == 0 [
        :p1 = 2
    ] else [
        :p2 = 0
    ]
    drawRectangle(80, 20)
    return
}

drawRectangle(80, 20)
drawCircle()
:b = :l
if :b <= 42 [
   :l = :l + 40
] else [
   :l = :l + 22
]
