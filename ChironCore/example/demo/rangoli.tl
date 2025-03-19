def sqroot(:n)
{
    if (:n == 0) [ 
        return 0 
        ]
    if (:n == 1) [ 
        return 1 
        ]
    
    :low = 0
    :high = :n
    :ans = 0
    :epsilon = 0.0001  
    repeat 50 [ 
        :mid = (:low + :high) / 2
        :square = :mid * :mid
        
        if (:square == :n) [
            return :mid
        ]
        
        if (:square < :n) [
            :low = :mid
            :ans = :mid 
        ]
        else [
            :high = :mid
        ]
        
        if ((:high - :low) < :epsilon) [
            return :ans
        ]
    ]
    return :ans
}

def drawRangoli(:size)
{
    pendown
    forward :size
    left 90
    forward :size
    left 90
    forward :size
    left 90
    forward :size
    penup

    left 90
    forward :size/2
    left 45
    :size = sqroot((:size * :size ) / 2)
    if :size > 10
     [ drawRangoli(:size) ]
    return
}

penup
class :Point {
    :x = -300
    :y = -300
}
:point = new :Point()
goto (:point.:x, :point.:y)

drawRangoli(:size)