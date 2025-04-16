import subprocess
import os
import re

def Z3Solver(smtlib_code):
    """
    Executes Z3 with the given SMT-LIB code string and processes the output.

    Args:
        smtlib_code (str): The SMT-LIB code to be solved by Z3.

    Returns:
        list: A list of results for each condition, including whether it is verified and the counterexample if not.
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

        if "sat" in results:
            output += "Please refer to \"control_flow_graph.png\" for variable names.\n" 
        return output                
            
    except FileNotFoundError:
        os.remove(temp_file)
        raise RuntimeError("Error: Z3 is not installed or not in PATH. Try running `z3 -h` to check.")


def split_sat_blocks_and_extract_models(input_string):
    lines = input_string.strip().splitlines()
    
    results = []
    blocks = []

    current_block = []
    current_result = None

    for line in lines:
        line = line.strip()
        if line == "sat" or line == "unsat":
            if current_result is not None:
                results.append(current_result)
                blocks.append(current_block)
                current_block = []
            current_result = line
        else:
            current_block.append(line)

    if current_result is not None:
        results.append(current_result)
        blocks.append(current_block)

    # Extract variables from sat blocks
    sat_models = []
    for result, block in zip(results, blocks):
        if result == "sat":
            model = {}
            i = 0
            while i < len(block):
                line = block[i]
                match = re.match(r"\(define-fun (\S+) \(\) Int", line)
                if match and i + 1 < len(block):
                    var_name = match.group(1)
                    value_line = block[i + 1].strip(" )")
                    
                    # Normalize negative numbers
                    if value_line.startswith("(-"):
                        value_line = "-" + value_line[3:].strip(" )")
                    
                    model[var_name] = value_line
                    i += 2  # Skip next line as it's already processed
                else:
                    i += 1  # Move to next line
            sat_models.append(model)
        else:
            sat_models.append("UNSAT")

    return results, sat_models

