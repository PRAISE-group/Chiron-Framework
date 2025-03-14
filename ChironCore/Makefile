CXX = g++
# CXXFLAGS = -std=c++17 -I/opt/homebrew/Cellar/llvm/19.1.7_1/include -I/opt/homebrew/opt/antlr4-cpp-runtime/include -I./turtparse -I./ChironAST
# LDFLAGS = -L/opt/homebrew/Cellar/llvm/19.1.7_1/lib -L/opt/homebrew/opt/antlr4-cpp-runtime/lib -lLLVM -lantlr4-runtime

ifeq ($(shell uname), Darwin)
    LLVM_INCLUDE ?= /opt/homebrew/Cellar/llvm/19.1.7_1/include
    LLVM_LIB ?= /opt/homebrew/Cellar/llvm/19.1.7_1/lib
    ANTLR_INCLUDE ?= /opt/homebrew/opt/antlr4-cpp-runtime/include
    ANTLR_LIB ?= /opt/homebrew/opt/antlr4-cpp-runtime/lib
else
    LLVM_INCLUDE ?= /usr/include/llvm-12
    LLVM_LIB ?= /usr/lib/llvm-12
    ANTLR_INCLUDE ?= /usr/local/include
    ANTLR_LIB ?= /usr/local/lib
endif

CXXFLAGS = -std=c++17 -I$(LLVM_INCLUDE) -I$(ANTLR_INCLUDE) -I./turtparse -I./ChironAST

LDFLAGS = -L$(LLVM_LIB) -L$(ANTLR_LIB) -lLLVM -lantlr4-runtime
SRCS = main.cpp \
       turtparse/tlangLexer.cpp \
       turtparse/tlangParser.cpp \
       turtparse/tlangBaseVisitor.cpp \
       ChironAST/chironVisitor.cpp \
       ChironAST/codegenerator.cpp

OBJS = $(SRCS:.cpp=.o)
TARGET = main

# Default target
all: $(TARGET)

# Compile the executable
$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $(TARGET) $(LDFLAGS)

# Compile C++ source files into object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up generated files
clean:
	rm -f $(OBJS) $(TARGET)
