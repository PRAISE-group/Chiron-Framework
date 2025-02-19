def drawRectangle(:l, :b)
{
    if :l == 0 [
        return
    ]
    if :l <= 1 [
        :b = :b + 40
    ] else [
        :b = :b + 22
    ]
    drawRectangle(:l - 1, :b)
    return
}

def drawCircle()
{
    :r = 10
    :p1 = 80
    :p2 = 80
    if :p1 == 0 [
        :p1 = 2
    ] else [
        :p2 = 1
    ]
    return :p2, :p1
}

:l, :b = drawCircle()
print(:b)
if :b <= 42 [
   :l = :l + 40
] else [
   :l = :l + 22
]
print(:l)