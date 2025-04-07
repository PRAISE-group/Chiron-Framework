#!/bin/bash

# Step 1: Generate ANTLR files
cd turtparse || exit
java -cp ../extlib/antlr-4.7.2-complete.jar org.antlr.v4.Tool \
  -Dlanguage=Python3 -visitor -no-listener tlang.g4
cd ..

# Step 2: Loop through arguments
for path in "$@"; do
    if [[ -d "$path" ]]; then
        # Argument is a directory: loop over files inside
        for file in "$path"/*; do
            if [[ -f "$file" ]]; then
                echo "Running: $file"
                python3 ./chiron.py -r "$file"
                pid=$!

                wait "$pid"
            fi
        done
    elif [[ -f "$path" ]]; then
        # Argument is a file: run directly
        echo "Running: $path"
        python3 ./chiron.py -r "$path"
        pid=$!

        wait "$pid"
    else
        echo "Warning: '$path' is not a valid file or directory"
    fi
done

