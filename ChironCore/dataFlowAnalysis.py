'''
    This file implements the worklist algorithm.
    WorkList class is the class for worklist queue
    and necessary functions to operate on the worklist.
    worklistAlgorithm actually implements the worklist algorithm.
'''

from queue import Queue
import sys
import cfg.cfgBuilder as cfgB
import cfg.ChironCFG as cfgK

sys.path.insert(0, '../Submission/')
from submissionDFA import *
from abstractInterpretation import *

class DataFlowAnalysis(AbstractInterpreter):
    def __init__(self, irHandler):
        super().__init__(irHandler)
        self.pc = 0