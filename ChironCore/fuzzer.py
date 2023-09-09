## Coverage Guided Fuzzing

"""
This file implements the main fuzzer loop.
Pick an input using a distribution, mutate it
run the program with the mutated input and return
coverage metric and compare to previous metric to
check if we found any improvement due to the mutation.

This loop continues until time limit is exhausted or we
ran out of inputs inorder to continue mutations for the
fuzzer loop.
"""

import sys
import time
import random
import copy
import uuid
from interpreter import *

sys.path.insert(0, "../Submission/")
from fuzzSubmission import *


class InputObject:
    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.data = data
        # Flag to check if ever picked
        # for mutation or not.
        self.pickedOnce = False


class Fuzzer(ConcreteInterpreter):
    # Execute the program using the input from mutator
    def __init__(self, irHandler, params):
        """
        ir (List): List of program IR statments
        params (dict): Mapped variables with initial assignments.
        """
        super().__init__(irHandler)
        self.ir = irHandler.ir
        self.params = params
        self.corpus = []
        self.timeout = 0
        self.customMutator = CustomMutator()  # From submission
        self.coverage = CustomCoverageMetric()  # From submission

    def handleStmt(self, ir, inputList={}, end=0):
        coverage = []
        terminated = False
        self.pc = 0
        self.initProgramContext(inputList)
        coverage.append(self.pc)
        # The maximum time for one execution of the
        # fuzzed program must be less than end time.
        while time.monotonic() <= end:
            terminated = self.interpret()
            # List of PC values -> Execution Trace -> Stmts Hit!
            coverage.append(self.pc)
            if terminated:
                break
        if time.monotonic() >= end:
            print("[fuzzer] Program took too long to execute. Terminated")
        else:
            print("[fuzzer] Program Ended.")
        return list(set(coverage))

    def seedCorpusRandom(self, varsList):
        # HonggFuzz starts with a buffer of atleast
        # four elements. Lets start with 8 say.
        for _ in range(8):
            inputDict = {}
            for variable in varsList:
                inputDict[variable] = random.randint(-10, 10)
            input_i = InputObject(data=inputDict)
            self.corpus.append(input_i)

    def fuzz(self, timeLimit=0, generateRandom=False):
        """[summary]

        Args:
            timeLimit (float/int): Total time(sec) to run the fuzzer loop for.
            generateRandom (boolean): Whether to generate random seed inputs at the starting.

        Returns:
            tuple (coverage, corpus) : Return coverage information and corpus of inputs used for fuzzing.
        """

        # If Dummy List needed.
        if generateRandom:
            varList = []
            for key, _ in self.params.items():
                variable = key.replace(":", "").strip()
                varList.append(variable)
            self.seedCorpusRandom(varList)

        # get the variables used in the program.

        print(f"[fuzzer] Starting Fuzzer : init args -> {self.params}")

        # Initial Seed values from user.
        temp_input = InputObject(data=self.params)
        self.corpus.append(temp_input)

        start_time = time.monotonic()
        # Fuzzing ends at this timestamp.
        endTime = time.monotonic() + timeLimit

        # Either supply dummy corpus
        # or use user-provided inputs.
        while True:
            # Initialize current coverage to empty as loop starts.
            self.coverage.curr_metric = []

            # Pick a random input and choose it for mutation.
            pickedInput = random.choice(self.corpus)

            # Set this flag since the input is picked once now.
            pickedInput.pickedOnce = True
            print(f"[fuzzer] Fuzzing with Input ID : {pickedInput.id}")
            pickInputRandom = copy.deepcopy(pickedInput)

            pickInputRandom.pickedOnce = False
            mutated_input = self.customMutator.mutate(
                pickInputRandom, self.coverage, self.ir
            )

            # Get new coverage from execution.
            # The maximum time for one execution of the
            # fuzzed program must be less than end time.
            self.coverage.curr_metric = self.handleStmt(
                self.ir, mutated_input.data, end=endTime
            )
            # Print the coverage : Representational
            print(f"[fuzzer] Coverge for execution : {self.coverage.curr_metric}")

            # Check if coverage improved.
            if self.coverage.compareCoverage(
                self.coverage.curr_metric, self.coverage.total_metric
            ):
                mutated_input.id = str(uuid.uuid4())
                mutated_input.pickedOnce = False
                self.coverage.total_metric = self.coverage.updateTotalCoverage(
                    self.coverage.curr_metric, self.coverage.total_metric
                )
                # Add mutated input if coverage improved.
                self.corpus.append(mutated_input)

            exhaustedBudget = True if time.monotonic() >= endTime else False
            if exhaustedBudget:
                time_delta = time.monotonic() - start_time
                print(f"[fuzzer] Time Exhausted : {time_delta}")
                break

        print(f"[fuzzer] Terminating Fuzzer Loop.")
        # Return coverage information and corpus of inputs.
        return (self.coverage, self.corpus)
