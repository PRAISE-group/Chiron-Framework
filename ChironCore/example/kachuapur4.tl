class :Animal {
    :tail = 1
}

class :Cat(:Animal) {
    :legs = 4
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


:whiskers2 = new :Cat()
:delta = 4
:legs = :whiskers2.incrementLegs(:delta)
print(:legs)
print(:whiskers2.:legs)

