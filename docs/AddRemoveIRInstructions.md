## Addition/Removal of Instructions from IR.

Two new functions have been added in `irgen.py` to add and remove statements from a given IR List.

## `addInstruction(IRList, Inst, pos)`

Given a list of IR Statements (`IRList`), IR instruction statement of `ChironAST` type and a position `pos` (postiton to insert an IR statement),
the function inserts the statement in `IRList`. Conditional Statements cannot be added. Relative jumps of all the affected statements are updated.

## `removeInstruction(IRList, pos)`

Given a list of IR Statements (`IRList`) and a position `pos` (postiton to delete an IR statement from `IRList`),
removeInstruction() converts the statement into a no-op, effectively removing it from the IR list,
The `NOP` functionality for interpreter has also been added in `interpreter.py`.

### Usage :

```python3
addInstruction(ir, ChironAST.AssignmentCommand(ChironAST.Var(":vara"), ChironAST.Num(5)), 11)
# 11 :vara = 5  [ 1 ]

removeInstruction(ir, 11)
# 11 : NOP [ 1 ]
```
