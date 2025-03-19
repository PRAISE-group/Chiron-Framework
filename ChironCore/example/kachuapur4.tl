def add(:a, :b)
{
    return :a + :b
}
def increment(:val)
{
    return add(:val, 1)
}

:val = 1
:val = increment(:val)
print(:val)