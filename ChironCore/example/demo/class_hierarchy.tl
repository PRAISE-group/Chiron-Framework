class :Base {
    def Base(:arg1) {}
}

class :Level1(:Base) {
    def oneA() {}
    def twoA(:arg1, :arg2) {}
}

class :Level2(:Level1) {
    def twoA(:arg1, :arg2) {}
    def twoB(:arg1, :arg2, :arg3) {}
}

class :Deroute(:Base) {
    def something(:arg1, :arg2) {}
}

class :Level3(:Level2, :Deroute) {
    def threeA() {}
    def threeB(:arg1, :arg2, :arg3, :arg4) {}
}
