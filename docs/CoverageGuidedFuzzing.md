### Fuzzer for Chiron. (Needed for Assignment-4)

A coverage guided `fuzzing` loop has been implemented in `ChironCore/fuzzer.py` file.

Running the `Fuzzer` Loop : (From `ChironCore folder`)

```bash

$ ./Chiron.py -t 100 --fuzz example/fuzz2.tl -d '{":x": 5, ":y": 100}'
$ ./Chiron.py -t 100 --fuzz example/example2.tl -d '{":dir": 3, ":move": 5}'
```

Fuzzer specific arguments.

```js

-t : Time budget for fuzzing in seconds. (optional)
-d : Specify initial parameters. (required)
--fuzz : Run fuzzing Loop
```