def add(:a, :b)
{
    return :a + :b
}
class :Test
{
def increment(:self, :val)
{
    return add(2, 3)
}
}

:test = new :Test()
:val = 1
:val = :test.increment(:val) * 2
print(:val)