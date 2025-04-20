
def drawRectangle(:l, :b)
{
    penup
    goto (:l, :b)
    pendown
    forward :l
    right 90
    forward :b
    right 90
    forward :l
    right 90
    forward :b
    penup
    return 0
}

def drawCircle()
{
    :vara = 20
    :varb = 100
    :varc = 60
    repeat 1 [
        goto (0, 0)
        pendown
        repeat 6 [
            if (:vara != :varb) [
                if ( :vara > :varb) [ right :vara ]
                else [ left :varb ]
            ]
            else [
            if ((:vara <= :varc) || (:varb <= :varc)) [
                :vara = :varc / :vara
                :varb = :varb / :varc
                :varc = :varb
            ]
            ]
            forward :vara
            right :varb
            forward :varc
            left :varc
        ]
        left 45
        ]
        penup
        return :vara, :varb
}

def factorial(:n)
{
    if :n == 1 [
        return 1
    ]
    return :n * (:f=factorial(:n - 1))
}

:f= drawRectangle(50, 50)
:a= drawCircle()
print(factorial(6))
