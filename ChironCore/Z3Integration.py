import subprocess
import os

def Z3Solver(smtlib_code):
    """
    Executes Z3 with the given SMT-LIB code string.

    Args:
        smtlib_code (str): The SMT-LIB code to be solved by Z3.

    Returns:
        tuple: A tuple containing the Z3 output (stdout) and errors (stderr).
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

        return result.stdout, result.stderr

    except FileNotFoundError:
        os.remove(temp_file)
        raise RuntimeError("Error: Z3 is not installed or not in PATH. Try running `z3 -h` to check.")