
def add(:a, :b)
{
    return :a + :b
}
def increment(:a)
{
    return (add(:a, 1))
}
print(increment(4)*5)
