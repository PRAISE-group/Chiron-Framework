class Lattice():
    '''
        Base class for the abstract values
    '''
    '''Initialize abstract value'''

    def __init__(self, data):
        pass

    '''To display abstract values'''

    def __str__(self):
        pass

    '''To check whether abstract value is bot or not'''

    def isBot(self):
        pass

    '''To check whether abstract value is Top or not'''

    def isTop(self):
        pass

    '''Implement the meet operator'''

    def meet(self, other):
        pass

    '''Implement the join operator'''

    def join(self, other):
        pass

    '''partial order with the other lattice value'''
    def __le__(self, other):
        pass

    '''equality check with other lattice value'''
    def __eq__(self, other):
        pass

    '''
        Add here for other operations
    '''

class TransferFunction():
    def __init__(self):
        pass