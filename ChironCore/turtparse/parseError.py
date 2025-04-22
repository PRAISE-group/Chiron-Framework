class SyntaxException(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        self.message=message
        self.errors = errors

    def __str__(self):
        return self.message + "\nLine : " + str(self.errors[0]) +\
            ", Column : " + str(self.errors[1]) +\
            "\nReport: (" + self.errors[2] + ")"

class SyntaxErrorListener():
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxException("Syntax Error", (line, column, msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print("Ambiguity detected:")
        print(f"  Start index: {startIndex}")
        print(f"  Stop index: {stopIndex}")
        print(f"  Exact: {exact}")
        print(f"  Ambiguous alternatives: {ambigAlts}")
        raise ValueError("Ambiguity error.")

        
        # # Print details about each alternative
        # for alt in ambigAlts:
        #     print(f"  Alternative {alt}:")
        #     for config in configs:
        #         if config.alt == alt:
        #             print(f"    {self.getConfigDescription(recognizer, config)}")
    
    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        print("Full context attempt:")
        print(f"  Start index: {startIndex}")
        print(f"  Stop index: {stopIndex}")
        print(f"  Conflicting alternatives: {conflictingAlts}")

        # Print details about each alternative
        for alt in conflictingAlts:
            print(f"  Alternative {alt}:")
            for config in configs:
                if config.alt == alt:
                    print(f"    {self.getConfigDescription(recognizer, config)}")

    def getConfigDescription(self, recognizer, config):
        return (f"(Rule: {recognizer.ruleNames[config.state.ruleIndex]}, "
                f"State: {config.state.stateNumber}, "
                )

        
        # Add any additional custom error handling or logging as needed



    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        # Get the current token
        current_token = recognizer.getCurrentToken()
        
        # Get the rule names
        rule_names = recognizer.ruleNames
        
        # Print basic information
        print(f"Context sensitivity detected at token '{current_token.text}' (line {current_token.line}, column {current_token.column})")
        
        # Print conflicting rules
        print("Conflicting rules:")
        for config in configs:
            rule_index = config.state.ruleIndex
            if rule_index >= 0 and rule_index < len(rule_names):
                rule_name = rule_names[rule_index]
                print(f"  - {rule_name}")
        
        print(f"Predicted alternative: {prediction}")        
        # raise ValueError("Exit due to context sensitivity.")
