import subprocess
import os
import re

def Z3Solver(smtlib_code):
    """
    Executes Z3 with the given SMT-LIB code string and processes the output.

    Args:
        smtlib_code (str): The SMT-LIB code to be solved by Z3.

    Returns:
        str: A formatted string containing the verification results and counterexamples (if any).

    Explanation:
        - This function writes the SMT-LIB code to a temporary file and runs Z3 as a subprocess.
        - It processes the Z3 output to determine whether the conditions are verified or not.
        - If a condition fails, it extracts the counterexample and formats it for output.
        - The function handles both single-condition and multi-condition verification scenarios.
    """
    # Write the SMT-LIB code to a temporary file
    temp_file = "temp.smt2"
    with open(temp_file, "w") as f:
        f.write(smtlib_code)

    # Run Z3 as a subprocess
    try:
        result = subprocess.run(['z3', temp_file], capture_output=True, text=True)

        # Clean up the temporary file
        os.remove(temp_file)

        # Process the Z3 output
        results, models = split_sat_blocks_and_extract_models(result.stdout)
        
        output = ""
        if(len(results) == 3):  # Handle multi-condition verification (e.g., Initialization, Loop, Final)
            conditions = ["Initialization", "Loop", "Final"]
    
            for i, condition in enumerate(conditions):
                if results[i] == "unsat":
                    output += f"{condition} Condition verified :)\n"
                elif results[i] == "sat":
                    output += f"{condition} Condition verification failed :(\n"
                    output += "Counterexample:\n"
                    for var, val in models[i].items():
                        output += f"{var} : {val}\n"
                output += "\n"
        
        elif len(results) == 1:  # Handle single-condition verification
            if results[0] == "unsat":
                output += "Condition verified :)\n"
            elif results[0] == "sat":
                output += "Condition verification failed :(\n"
                output += "Counterexample:\n"
                for var, val in models[0].items():
                    output += f"{var} : {val}\n"
            output += "\n"
        
        # Add a note if any condition fails
        if "sat" in results:
            output += "Please refer to \"control_flow_graph.png\" for variable names.\n" 
        return output                
            
    except FileNotFoundError:
        # Handle the case where Z3 is not installed or not in the PATH
        os.remove(temp_file)
        raise RuntimeError("Error: Z3 is not installed or not in PATH. Try running `z3 -h` to check.")


def split_sat_blocks_and_extract_models(input_string):
    """
    Splits the Z3 output into blocks based on "sat" and "unsat" results and extracts models for "sat" blocks.

    Args:
        input_string (str): The raw output from Z3.

    Returns:
        tuple: A tuple containing:
            - results (list): A list of "sat" or "unsat" results for each block.
            - sat_models (list): A list of models (dictionaries) for "sat" blocks or "UNSAT" for "unsat" blocks.

    Explanation:
        - This function parses the Z3 output to separate "sat" and "unsat" blocks.
        - For "sat" blocks, it extracts variable assignments (models) from the output.
        - Each model is represented as a dictionary mapping variable names to their values.
    """
    # Split the input into lines
    lines = input_string.strip().splitlines()
    
    results = []  # List to store "sat" or "unsat" results
    blocks = []  # List to store corresponding blocks of output

    current_block = []  # Temporary storage for the current block
    current_result = None  # Temporary storage for the current result ("sat" or "unsat")

    # Iterate through each line of the Z3 output
    for line in lines:
        line = line.strip()
        if line == "sat" or line == "unsat":  # Check for result indicators
            if current_result is not None:
                # Store the previous result and block
                results.append(current_result)
                blocks.append(current_block)
                current_block = []  # Reset the current block
            current_result = line  # Update the current result
        else:
            # Add the line to the current block
            current_block.append(line)

    # Add the last result and block (if any)
    if current_result is not None:
        results.append(current_result)
        blocks.append(current_block)

    # Extract variables from "sat" blocks
    sat_models = []
    for result, block in zip(results, blocks):
        if result == "sat":  # Process "sat" blocks to extract models
            model = {}
            i = 0
            while i < len(block):
                line = block[i]
                # Match variable definitions in the block
                match = re.match(r"\(define-fun (\S+) \(\) Int", line)
                if match and i + 1 < len(block):
                    var_name = match.group(1)  # Extract the variable name
                    value_line = block[i + 1].strip(" )")  # Extract the value
                    
                    # Normalize negative numbers
                    if value_line.startswith("(-"):
                        value_line = "-" + value_line[3:].strip(" )")
                    
                    model[var_name] = value_line  # Add the variable and its value to the model
                    i += 2  # Skip the next line as it's already processed
                else:
                    i += 1  # Move to the next line
            sat_models.append(model)  # Add the model to the list of models
        else:
            sat_models.append("UNSAT")  # Add "UNSAT" for unsat blocks

    return results, sat_models

