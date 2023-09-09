class MutatorBase():
    # Base class to extend/implement a
    # custom mutation operator.
    def __init__(self):
        pass

    def mutate(self, input_data, coverageInfo, irList):
        # must return InputObject type
        # coverageInfo is of type CoverageMetricBase
        # irList : List of IR Statments (Don't Modify)
        # Don't mutate coverageInfo
        pass

    def operate(self, input_data, operatorFunc):
        # must return InputObject type
        pass

class CoverageMetricBase():
    # Base class to extend/implement a
    # custom coverage metric.
    def __init__(self):
        # Must have curr_metric, total_metric
        self.curr_metric = []
        self.total_metric = []


    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # Return True/False based on increase in coverage.
        return False

    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a
        # given input.
        return total_metric