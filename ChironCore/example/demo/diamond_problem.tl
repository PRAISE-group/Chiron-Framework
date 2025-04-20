class :Animal {
    :walk = 1
    def walk(:self)
    {
        print(:self.:walk)
        return 0
    }
}

class :Lion(:Animal)
{

}
class :Tiger(:Animal)
{

}

class :Liger(:Lion, :Tiger)
{
}

:liger = new :Liger()
:liger.:walk = 2
:liger.walk()