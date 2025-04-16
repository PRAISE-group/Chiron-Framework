# Bounded Model Checker (BMC) of Chiron

## Introduction

A Bounded Model Checker (BMC) engine is a verification tool used to check the satisfiability of a condition within a given bound without actually running the code. It systematically explores all possible states of a system up to a specified depth to detect errors.

The BMC engine works by encoding the system's behavior and the properties to be verified into a logical formula. This formula is then solved using a SAT (Satisfiability) solver. If the solver finds a solution within the bounds, it indicates a counterexample that demonstrates a violation of the property being checked. If no solution is found within the given bound, the system is considered correct up to the bounds.

### What makes BMC interesting

The BMC engine provides an automated approach to verify the correctness of complex systems. Unlike traditional testing, which relies on specific test cases, BMC explores all possible states within a given bound, ensuring thorough coverage. This makes it particularly effective in uncovering subtle bugs that might be missed by conventional methods.

The use of SAT solvers to encode and solve logical formulas demonstrates the power of combining formal methods with computational tools. The ability to detect counterexamples and provide concrete scenarios where a property fails is invaluable for debugging and improving system reliability.

Moreover, BMC's ability to handle constraints, conditions, and configurations, including loop unrolling and custom angle restrictions, makes it a versatile tool for diverse software verification applications.

## How to use Chiron BMC

### Adding Bounds 
We can restrict the domain of variables by `assume` statements. For example:
- `assume :x >= 0` bounds the domain of variable `:x` in the positive side of number line
- `assume :x*:x + :y*:y <= r*r` restricts the point `(:x, :y)` inside the circle of radius `r`.

### Adding Conditions
We add the conditions to be checked by `assert` statements. For example:
- `assert :x >= 0 && :y >= 0` checks whether the point `(:x, :y)` lies in the first quadrant
- `assert :x*:x + :y*:y >= r*r` checks whether the point `(:x, :y)` lies outside the circle of radius `r`.

### Handling Loops

Loops in the code are managed through a technique called **loop unrolling**. Loop unrolling involves replicating the loop's body multiple times, constrained by a specified unroll bound. For the purpose of understaning unrolling, we store the unrolled code in file `unrolled_code.tl`.

### Adding Loop Unroll Bound
`-ub <UNROLL_BOUND>` is used to set the unroll bound of loops. By default, it is set to 10.

A custom unroll bound for a particular loop can be set by using the `@unroll` decorator. For example,
```c
@unroll <UNROLL_BOUND> repeat <value> [
    ...
]
```

### Tracking Position of Turtle
We assume that turle starts at position $(0, 0)$ and facing at $0^\circ$ angle with respect to the positive direction of $x$-axis. The position of turtle is maintained by the variables `:turtleX` ($x$-coordinate), `:turtleY` ($y$-coordinate) and `:turtleThetaDeg` (angle in degrees).

### Adding Angle Constraints
By default, the turtle can face towards $0^\circ$, $90^\circ$, $180^\circ$ and $270^\circ$. Custom angles can be added by maintaining a configuration file that specifies the angles along with their cosine and sine values in the following format:

```plaintext
<angle_1>, <cos(angle_1)>, <sin(angle_1)>
<angle_2>, <cos(angle_2)>, <sin(angle_2)>
...
```

This configuration file is then passed to the BMC engine using the `-aconf <filename>` argument.

### Tracking Pen State
The variable `:turtlePen` is used to maintain the up/down state of pen.
- `:turtlePen = 0` indicates pendown state
- `:turtlePen = 1` indicates penup state

At the start of the program, pen is in pendown state.

## Examples
Examples for working of the BMC engine are provided in the `/ChironCore/bmc_examples/` directory. To run the BMC engine on these test cases, navigate to the `ChironCore` directory and execute the following command:

```bash
./chiron.py <path_to_test_file> -bmc -ub <UNROLL_BOUND> -aconf <ANGLE_CONF_FILE>
```
where `-ub` and `-aconf` are optional arguments

## Implementation Methodology

1. **Loop Unrolling**:  
    All the loops of the code are unrolled based on the unroll bound and the unrolled code is used for further processing.

2. **Converting Chiron Intermediate Representation (IR) into Three Address Code (TAC)**:  
    The Chiron IR of the unrolled code is generated and is transformed into TAC to simplify the representation of operations and facilitate further analysis.

3. **Generating Static Single Assignment (SSA)**:  
    The TAC is converted into SSA form to simplify data flow analysis and accurately track variable dependencies and states throughout the program.

4. **SAT Solver Integration**:  
    The SSA form is translated into SMT-LIB statements. This process encodes the constraints, conditions, and properties into a series of logical assertions and declarations to accurately represent the program's semantics. These statements are then checked for satisfiability using the Z3 solver.

5. **Reporting Results**:  
    - **Checking tightness of bounds**:  
        The BMC engine verifies if a solution exists within the given bounds. If no solution is found, it suggests relaxing the bounds.

    - **Checking satisfiability under all bounds**:  
        The BMC engine checks satisfiability until either a counterexample is found or all possible states of the program within the specified bounds are exhausted. If no violations are detected, the system is considered correct up to the given bounds.

    - **Counter Example generation**:  
        If the BMC engine detects a violation, it generates a counterexample for the input variables.

## Acknowledgement
We express our gratitude to Professor Subhajit Roy and Chiron team for their unwavering guidance and support throughout the duration of this project. Their assistance significantly influenced the course of our journey, making it markedly distinct from what it would have been otherwise.