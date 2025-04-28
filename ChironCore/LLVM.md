# LLVM Build Instructions

## Installing Dependencies

### MacOS
Ensure you have Homebrew installed, then run:
```sh
brew install llvm antlr4-cpp-runtime
```

### Linux (Fedora/RHEL)
```sh
sudo dnf install llvm-devel antlr4-cpp-runtime-devel
```

### Linux (Arch Linux)
```sh
sudo pacman -S llvm antlr4-runtime
```

### Linux (Ubuntu/Debian)
```sh
wget https://apt.llvm.org/llvm.sh
chmod +x llvm.sh
sudo ./llvm.sh 18
```

#### Installing ANTLR4 C++ Runtime Manually
Since the official package might be outdated, download and build the latest version:
```sh
wget https://www.antlr.org/download/antlr4-cpp-runtime-4.13.2-source.zip
unzip antlr4-cpp-runtime-4.13.2-source.zip
cd antlr4-cpp-runtime-4.13.2-source
mkdir build && cd build
cmake ..
make
sudo make install
```

### Updating Makefile Paths
After installing LLVM and ANTLR4 runtime, you may need to update the `Makefile` to reflect the correct include paths and library paths based on your OS and installation method. Modify the following variables in the `Makefile` accordingly:
```makefile
LLVM_INCLUDE ?= /path/to/llvm/include
LLVM_LIB ?= /path/to/llvm/lib
ANTLR_INCLUDE ?= /path/to/antlr4-runtime/include
ANTLR_LIB ?= /path/to/antlr4-runtime/lib
```
Ensure these paths are correctly set before running the `make` command.

## Generating the ANTLR files.

The `antlr` files need to be rebuilt for CPP if any changes are made to the `tlang.g4` file.

```
$ cd ./turtparse
$ java -cp ../extlib/antlr-4.13.2-complete.jar org.antlr.v4.Tool -Dlanguage=Cpp -visitor -no-listener tlang.g4
```

## Building the Project
Run the following command to compile the project:
```sh
make
```
This will generate the `main` binary.

## Running the Compiler on an example
To generate an executable from a `.tl` source file, use:
```sh
./chiron.py -l -o output ./example/example1.tl -p -r -d '{":x": 20, ":y": 30, ":z": 20, ":p": 40}'
```
This will produce an output executable named `output` along with LLVM IR representation `output.ll`.

## Running the Output Executable
After generating the output binary, execute it using:
```sh
./output
```

## Cleaning Up
To remove compiled binaries and object files, run:
```sh
make clean
```
To remove only object files, use:
```sh
make cleanobj
```

## Supported command-line flags

Chiron supports a wide range of command-line flags for program analysis and code generation. When it comes to generating LLVM Intermediate Representation (IR) and compiling to a binary, only a specific subset of flags are applicable.

To generate LLVM IR and an executable, the `-l` or `--llvm` flag must be provided. Once this flag is set, only the following flags are supported and should be used in combination:

- `-o` / `--llvm_output`: Specifies the name of the output file for LLVM IR and the compiled executable.
- `-dump`/ `--dump_ir`: Dumps the LLVM IR to output_filename.ll
- `-p` / `--ir`: Pretty-prints the intermediate representation (IR) of the Chiron program to the terminal.
- `-r` / `--run`: Executes the Chiron program using the generated LLVM binary.
- `-opt` / `--optimise` : Optimises the program by performing basic dead code elimination.
- `-d` / `--params`: Passes input parameters to the Chiron program in dictionary format.