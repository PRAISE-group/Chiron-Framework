CXX = g++
CXXFLAGS = -std=c++17 -I/opt/homebrew/Cellar/llvm/19.1.7_1/include -I/opt/homebrew/opt/antlr4-cpp-runtime/include -I./turtparse -I./ChironAST
LDFLAGS = -L/opt/homebrew/Cellar/llvm/19.1.7_1/lib -L/opt/homebrew/opt/antlr4-cpp-runtime/lib -lLLVM -lantlr4-runtime

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
