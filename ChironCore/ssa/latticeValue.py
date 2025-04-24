"""LatticeValue class for holding lattice value for a variable"""
class LatticeValue:
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    CONSTANT = "CONSTANT"

    def __init__(self, value_type: str, constant=None):
        self.value_type = value_type
        self.constant = constant  # Only relevant for CONSTANT

    @staticmethod
    def top():
        return LatticeValue(LatticeValue.TOP)

    @staticmethod
    def bottom():
        return LatticeValue(LatticeValue.BOTTOM)

    @staticmethod
    def constant(value):
        return LatticeValue(LatticeValue.CONSTANT, value)

    def is_top(self) -> bool:
        return self.value_type == LatticeValue.TOP

    def is_bottom(self) -> bool:
        return self.value_type == LatticeValue.BOTTOM

    def is_constant(self) -> bool:
        return self.value_type == LatticeValue.CONSTANT

    def __eq__(self, other: 'LatticeValue') -> bool:
        if self.value_type != other.value_type:
            return False
        if self.is_constant():
            return self.constant == other.constant
        return True

    def __repr__(self) -> str:
        if self.is_top():
            return "⊤"
        elif self.is_bottom():
            return "⊥"
        else:
            return f"C({self.constant})"
        
    def get_constant(self):
        if self.is_constant():
            return self.constant
        raise ValueError("LatticeValue is not a constant")