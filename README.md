# Program Analysis with Chiron

A framework to teach program analysis, verification, and testing in a graduate-level course.

```
░█████╗░██╗░░██╗██╗██████╗░░█████╗░███╗░░██╗
██╔══██╗██║░░██║██║██╔══██╗██╔══██╗████╗░██║
██║░░╚═╝███████║██║██████╔╝██║░░██║██╔██╗██║
██║░░██╗██╔══██║██║██╔══██╗██║░░██║██║╚████║
╚█████╔╝██║░░██║██║██║░░██║╚█████╔╝██║░╚███║
░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝
```
[![Architecture Diagram](./assets/Architecture_Digram.png)](./assets/Architecture_Digram.png)

## Video Demo 

Fuzzer Demo in Chiron Framework. Click the image below

<a href="https://raw.githubusercontent.com/PRAISE-group/Chiron-Framework/master/assets/Fuzzer_Demo.mp4" title="Link Title"><img src="https://raw.githubusercontent.com/PRAISE-group/Chiron-Framework/master/assets/Screenshot%20from%202025-01-16%2012-34-51.png" alt="Alternate Text" /></a>

- [Some nice words in WSS' 2023, IIT Delhi about Chiron Framework](https://www.linkedin.com/posts/ashupdsce_wss-wss2023-iitd-activity-7150851909581463553-bJ6-?utm_source=share&utm_medium=member_desktop)
- [ASE 2023 Conference Page](https://conf.researchr.org/details/ase-2023/ase-2023-papers/117/An-Integrated-Program-Analysis-Framework-for-Graduate-Courses-in-Programming-Language)
- [Read our research paper here](https://ieeexplore.ieee.org/document/10298417)

## Citation 

If you want to cite this work, you may use this.

```
@INPROCEEDINGS{ase_2023_chiron,
  author={Chatterjee, Prantik and Kalita, Pankaj Kumar and Lahiri, Sumit and Muduli, Sujit Kumar and Singh, Vishal and Takhar, Gourav and Roy, Subhajit},
  booktitle={2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)}, 
  title={An Integrated Program Analysis Framework for Graduate Courses in Programming Languages and Software Engineering}, 
  year={2023},
  volume={},
  number={},
  pages={598-610},
  keywords={Surveys;Computer languages;Program processors;Software algorithms;Software systems;Task analysis;Engines;program analysis verification and testing;programming languages;software engineering;graduate level course;education},
  doi={10.1109/ASE56229.2023.00101}}
```
### Installing Dependencies

```bash
$ pip install antlr4-python3-runtime==4.7.2 networkx z3-solver numpy 
$ sudo apt-get install python3-tk
```

### Generating the ANTLR files.

The `antlr` files need to be rebuilt if any changes are made to the `tlang.g4` file or when installing Chiron for the first time.
We use a visitor pattern to generate the AST from parsing. 

```
$ cd ChironCore/turtparse
$ java -cp ../extlib/antlr-4.7.2-complete.jar org.antlr.v4.Tool \
  -Dlanguage=Python3 -visitor -no-listener tlang.g4
```

### Running an example

The main directory for source files is `ChironCore`. We have examples of the turtle programs in `examples` folder.
To pass parameters (input params) for running a turtle program, use the `-d` flag. Pass the parameters as a python dictionary. 

```bash
$ cd ChironCore
$ ./chiron.py -r ./example/example1.tl -d '{":x": 20, "y": 30, ":z": 20, ":p": 40}'
```

### See help for other command line options

```bash
$ python3 chiron.py --help


░█████╗░██╗░░██╗██╗██████╗░░█████╗░███╗░░██╗
██╔══██╗██║░░██║██║██╔══██╗██╔══██╗████╗░██║
██║░░╚═╝███████║██║██████╔╝██║░░██║██╔██╗██║
██║░░██╗██╔══██║██║██╔══██╗██║░░██║██║╚████║
╚█████╔╝██║░░██║██║██║░░██║╚█████╔╝██║░╚███║
░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝


Chiron v1.0.1
------------
usage: chiron.py [-h] [-p] [-r] [-gr] [-b] [-z] [-t TIMEOUT] [-d PARAMS] [-c CONSTPARAMS] [-se] [-ai] [-dfa] [-sbfl]
                 [-bg BUGGY] [-vars INPUTVARSLIST] [-nt NTESTS] [-pop POPSIZE] [-cp CXPB] [-mp MUTPB] [-ng NGEN]
                 [-vb VERBOSE]
                 progfl

Program Analysis Framework for ChironLang Programs.

positional arguments:
  progfl

options:
  -h, --help            show this help message and exit
  -p, --ir              pretty printing the IR of a Chiron program to stdout (terminal)
  -r, --run             execute Chiron program, the figure/shapes the turle draws is shown in a UI.
  -gr, --fuzzer_gen_rand
                        Generate random input seeds for the fuzzer before fuzzing starts.
  -b, --bin             load binary IR of a Chiron program
  -z, --fuzz            Run fuzzer on a Chiron program (seed values with '-d' or '--params' flag needed.)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout Parameter for Analysis (in secs). This is the total timeout.
  -d PARAMS, --params PARAMS
                        pass variable values to Chiron program in python dictionary format
  -c CONSTPARAMS, --constparams CONSTPARAMS
                        pass variable(for which you have to find values using circuit equivalence) values to Chiron program
                        in python dictionary format
  -se, --symbolicExecution
                        Run Symbolic Execution on a Chiron program (seed values with '-d' or '--params' flag needed) to
                        generate test cases along all possible paths.
  -ai, --abstractInterpretation
                        Run abstract interpretation on a Chiron Program.
  -dfa, --dataFlowAnalysis
                        Run data flow analysis using worklist algorithm on a Chiron Program.
  -sbfl, --SBFL         Run Spectrum-basedFault localizer on Chiron program
  -bg BUGGY, --buggy BUGGY
                        buggy Chiron program path
  -vars INPUTVARSLIST, --inputVarsList INPUTVARSLIST
                        A list of input variables of given Chiron program
  -nt NTESTS, --ntests NTESTS
                        number of tests to generate
  -pop POPSIZE, --popsize POPSIZE
                        population size for Genetic Algorithm.
  -cp CXPB, --cxpb CXPB
                        cross-over probability
  -mp MUTPB, --mutpb MUTPB
                        mutation probability
  -ng NGEN, --ngen NGEN
                        number of times Genetic Algorithm iterates
  -vb VERBOSE, --verbose VERBOSE
                        To display computation to Console

```
