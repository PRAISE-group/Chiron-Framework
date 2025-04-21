# Pull Request Template for Feature Additions.

## Brief description feature

The path profiling is being done as discussed in the Ball Larus Path Profiling paper.

This involves:
1. Saving the original IR
2. Identifying paths in the CFG
3. Computing edge weights
4. Instrumenting the IR
5. Running the instrumented program
6. Reporting the results

The static branch predictor is build by indexing the predictor table with the (path id, program counter) \
On running any program, the control flow graph is generated in the file **`control_flow_graph.png`** using which we can track down the paths shown in the file **`path_profile_data.txt`**

We have added **two new flags** in our project:

1. **`-bl`** – for generating Ball-Larus path profiling data.
2. **`-bl_op`** – for generating Ball-Larus path profiling data with **branch predictor optimization**.

## Example

### Running Ball-Larus Path Profiling Only

To generate only the Ball-Larus path profiling data, use the command:

```bash
./chiron.py -bl ./path_profiling_tests/testcase2.tl
```

---

### Running Ball-Larus Path Profiling with Branch Predictor Optimization

To generate profiling data along with branch prediction optimization:

```bash
./chiron.py -bl_op ./BallLarus/inputs.txt ./example/example1.tl
```

The directory `path_profiling_tests` contains testcases including if-else, loops, nested loops, and other control flow constructs. These tests can be used for the `-bl` flag.

The directory `path_profiling_op_tests` contains testcases for the `-bl_op` flag.




On running:

```bash
./chiron.py -bl ./path_profiling_tests/testcase0.tl
```

The following output is generated:

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '4', '5', '8', '10', 'END']: 1
```
![CFG Output for testcase0](https://raw.githubusercontent.com/SamyakSinghania/Ball-Larus-PathProfiling/master/ChironCore/path_profiling_tests/cfg0.png)

**`Explanation:`** From the code and the cfg, we can clearly verify that the path profile generated for the execution is indeed correct.

On running:

```bash
./chiron.py -bl_op ./BallLarus/inputs.txt ./path_profiling_op_tests/testcase6.tl
```

The following output is generated:

\*\*File: \*\***`predictor_accuracy.txt`**

```
Total Count: 7
Correct Count: 6
Accuracy: 0.8571428571428571
-----------------------
Total Count: 7
Correct Count: 6
Accuracy: 0.8571428571428571
-----------------------
```

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '2', '7', '11', '13', 'END']:  5
['START', '5', '7', '11', '13', 'END']:  1
['START', '5', '7', '8', '13', 'END']:  1
['START', '2', '7', '8', '13', 'END']:  3
```

![CFG Output for testcase6](https://raw.githubusercontent.com/SamyakSinghania/Ball-Larus-PathProfiling/master/ChironCore/path_profiling_op_tests/cfg6.png)

**`Explanation:`** The values of x,y,z,p were randomly generated based on which a specific path will be taken in the double diamond CFG. Based on the path profile and execution of branch instructions of the training inputs, a static branch predictor was learned which gives the predictions for the branch instructions of the test inputs.

On running:

```bash
./chiron.py -bl ./path_profiling_tests/testcase1.tl
```

The following output is generated:

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '2', '3']: 1
['2', '3']: 2
['2', '7', 'END']: 1 
```

On running:

```bash
./chiron.py -bl ./path_profiling_tests/testcase2.tl
```

The following output is generated:

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '2', '3', '4', '5']: 1
['4', '5']: 9
['4', '9']: 3
['2', '3', '4', '5']: 2
['2', '12', 'END']: 1
```

On running:

```bash
./chiron.py -bl_op ./BallLarus/inputs.txt ./path_profiling_op_tests/testcase1.tl
````

The following output is generated:

\*\*File: \*\***`predictor_accuracy.txt`**

```
Total Count: 88
Correct Count: 81
Accuracy: 0.9204545454545454
------------------------
Total Count: 107
Correct Count: 100
Accuracy: 0.9345794392523364
------------------------
```

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '2', '3', '4', '8', '9']: 8
['8', '9']: 72
['8', '13', '23', '24', '28', '29']: 20
['28', '29']: 125
['28', '33']: 25
['2', '3', '4', '8', '9']: 16
['2', '38', 'END']: 10
['START', '2', '3', '14', '18', '19']: 2
['18', '19']: 24
['18', '23', '24', '28', '29']: 5
['2', '3', '14', '18', '19']: 4
['18', '23', '33']: 1
['8', '13', '23', '33']: 4
```

On running:

```bash
./chiron.py -bl_op ./BallLarus/inputs.txt ./path_profiling_op_tests/testcase2.tl
```

The following output is generated:

\*\*File: \*\***`predictor_accuracy.txt`**

```
Total Count: 37
Correct Count: 34
Accuracy: 0.918918918918919
------------------------
Total Count: 37
Correct Count: 34
Accuracy: 0.918918918918919
------------------------
```

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '2', '3', '4', '5', '6']: 8
['5', '6']: 28
['5', '10', '17']: 14
['2', '3', '4', '5', '6']: 6
['2', '21', 'END']: 10
['START', '2', '3', '11', '12', '13']: 2
['12', '13']: 18
['12', '17']: 6
['2', '3', '11', '12', '13']: 4
```

On running:

```bash
./chiron.py -bl_op ./BallLarus/inputs.txt ./path_profiling_op_tests/testcase3.tl
```

The following output is generated:

\*\*File: \*\***`predictor_accuracy.txt`**

```
Total Count: 20
Correct Count: 18
Accuracy: 0.9
------------------------
Total Count: 20
Correct Count: 18
Accuracy: 0.9
------------------------
```

\*\*File: \*\***`path_profile_data.txt`**

```
['START', '2', '6', '7']: 6
['6', '7']: 18
['6', '11', '21', 'END']: 6
['START', '12', '16', '17']: 4
['16', '17']: 16
['16', '21', 'END']: 4
```

### Why is the feature interesting?

Give use cases for the feature.

```c
Path profiling can be used to perform optimizations like inlining and loop unrolling along frequently executed paths (hot paths). It can also support building a branch predictor or enable speculative optimizations along likely execution paths.
```

## Other Details


The source code lies in the directory `BallLarus`. The main implementation of the algorithm is in the file:

```
/ChironCore/BallLarus/ballLarus.py
```

This directory also includes a dedicated interpreter for Ball-Larus, derived from the pre-existing interpreter for better modularity.

The file generate_inputs.py in ChironCore/BallLarus/ can be used to generate multiple input flags for usage of -bl_op flag.

The following files are generated upon running the profiling:

1. **`hash_dump.txt`**\
   Contains the path indexes along with their frequencies.

2. **`path_profile_data.txt`**\
   Contains the actual path profile data along with their frequencies.

3. **`predictions_pc.txt`**\
   Contains the program counter (PC) values and corresponding branch predictor predictions.

4. **`predictor_accuracy.txt`**\
   Contains the final accuracy of the branch predictor based on the profiling data.

