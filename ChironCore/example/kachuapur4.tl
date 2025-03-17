class :Animal {
    :tail = 1
    :legs = 2

    def inheritTheMethod(:self)
    {
        print(:self.:tail)
        print(:self.:legs)
        return
    }
}

class :Cat(:Animal) {
    :legs = 4
    :tail = 1
    def printProperties(:self)
    {
        print(:self.:tail)
        print(:self.:legs)
        return
    }
    def incrementLegs(:self, :delta)
    {
        :self.:legs = :self.:legs + :delta
        return :self.:legs
    }
}

class :dummy{
    :test = 1
}

:whiskers2 = new :Cat()
:delta = 4
:legs = :whiskers2.incrementLegs(:delta)
:whiskers2.:tail = 2
print(:legs)
print(:whiskers2.:legs)
:whiskers2.printProperties()
:whiskers2.inheritTheMethod()

print(:whiskers2.:legs)
print(:whiskers2.:tail)
:whisker = new :Cat()
print(:whisker.:legs)
print(:whisker.:tail)

