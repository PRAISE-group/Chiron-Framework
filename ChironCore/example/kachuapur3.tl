class :a {
    :b = 3;
    :c = 4;
    :d = [2,3,4,[5,6]];
}

:b = new :a()
:b.:c = 5
print(:b.:c)
:x = :a.:c + :b.:c * 2
:y = :b.:d[3][1]
print(:x)
print(:y)
:b.:d[3][1]=99
print(:b.:d )