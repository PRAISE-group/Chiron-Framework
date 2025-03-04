from cfg.ChironCFG import *
import ChironTAC.ChironTAC as ChironTAC
import ChironSSA.ChironSSA as ChironSSA

def buildSSA(tac, cfg, line2BlockMap):
    """
    Builds SSA form from TAC and CFG.
    """

    ssa = []
    lastDeclaration = {}         # lastDeclaration[bb][var] = version
    varCounter = {}              # varCounter[var] = counter
    phiStatements = {}           # phiStatements[bb][var] = [var_1, var_2, ...]
    ssaLineCounter = 0
    block2ssaLine = {}           # block2ssaLine[bb] = ssaLine

    # Initialize
    for (stmt, tgt), line in zip(tac, range(len(tac))):
        if isinstance(stmt, ChironTAC.AssignmentCommand):
            varCounter[stmt.lvar.__str__()] = 0

    for node in cfg:
        phiStatements[node] = {}
        lastDeclaration[node] = {}

    # Renamed the declarations of variables in TAC
    for (stmt, tgt), line in zip(tac, range(len(tac))):
        if isinstance(stmt, ChironTAC.AssignmentCommand):
            var = stmt.lvar.__str__()
            lastDeclaration[line2BlockMap[line]][var] = varCounter[var]
            varCounter[var] += 1
            stmt.lvar = ChironTAC.Var(f"{var}__{varCounter[var] - 1}")
            tac[line] = (stmt, tgt)

    for node in cfg:
        predes = cfg.predecessors(node)
        for parent in predes:
            for var in lastDeclaration[parent]:
                if var not in phiStatements[node]:
                    phiStatements[node][var] = []
                phiStatements[node][var].append(lastDeclaration[parent][var])

    visited = {}
    for node in cfg:
        visited[node] = False

    lastUsed = {}
    for var in varCounter.keys():
        lastUsed[var] = varCounter[var]

    for (stmt, tgt), line in zip(tac, range(len(tac))):
        node = line2BlockMap[line]
        if visited[node] == False:
            visited[node] = True
            block2ssaLine[node] = ssaLineCounter
            for var in phiStatements[node].keys():
                if len(phiStatements[node][var]) > 1:
                    ssaLineCounter += 1
                    ssa.append((ChironSSA.PhiCommand(ChironSSA.Var(f"{var}__{varCounter[var]}"), [ChironSSA.Var(f"{var}__{version}") for version in phiStatements[node][var]]), 1))
                    lastUsed[var] = varCounter[var]
                    varCounter[var] += 1

        if isinstance(stmt, ChironTAC.AssignmentCommand):
            rvar1 = ChironSSA.Unused()
            rvar2 = ChironSSA.Unused()
            if isinstance(stmt.rvar1, ChironTAC.Var):
                if stmt.rvar1.__str__() not in lastUsed.keys():
                    lastUsed[stmt.rvar1.__str__()] = 0
                rvar1 = ChironSSA.Var(f"{stmt.rvar1.__str__()}__{lastUsed[stmt.rvar1.__str__()]}")
            elif isinstance(stmt.rvar1, ChironTAC.BoolTrue):
                rvar1 = ChironSSA.BoolTrue()
            elif isinstance(stmt.rvar1, ChironTAC.BoolFalse):
                rvar1 = ChironSSA.BoolFalse()
            elif isinstance(stmt.rvar1, ChironTAC.Num):
                rvar1 = ChironSSA.Num(stmt.rvar1.value)
            if isinstance(stmt.rvar2, ChironTAC.Var):
                if stmt.rvar2.__str__() not in lastUsed.keys():
                    lastUsed[stmt.rvar2.__str__()] = 0
                rvar2 = ChironSSA.Var(f"{stmt.rvar2.__str__()}__{lastUsed[stmt.rvar2.__str__()]}")
            elif isinstance(stmt.rvar2, ChironTAC.BoolTrue):
                rvar2 = ChironSSA.BoolTrue()
            elif isinstance(stmt.rvar2, ChironTAC.BoolFalse):
                rvar2 = ChironSSA.BoolFalse()
            elif isinstance(stmt.rvar2, ChironTAC.Num):
                rvar2 = ChironSSA.Num(stmt.rvar2.value)
            lvar = ChironSSA.Var(f"{stmt.lvar.__str__()}")
            
            lvar_string = lvar.__str__().rsplit('__', 1)[0]
            lastUsed[lvar_string] = int(lvar.__str__().rsplit('__', 1)[1])
            
            ssaLineCounter += 1
            ssa.append((ChironSSA.AssignmentCommand(lvar, rvar1, rvar2, stmt.op), tgt))

        elif isinstance(stmt, ChironTAC.ConditionCommand):
            tgt_block = line2BlockMap[line + tgt]
            if isinstance(stmt.cond, ChironTAC.BoolTrue):
                ssa.append((ChironSSA.ConditionCommand(ChironSSA.BoolTrue()), tgt_block))
            elif isinstance(stmt.cond, ChironTAC.BoolFalse):
                ssa.append((ChironSSA.ConditionCommand(ChironSSA.BoolFalse()), tgt_block))
            else:
                if isinstance(stmt.cond, ChironTAC.Var):
                    if stmt.cond.__str__() not in lastUsed.keys():
                        lastUsed[stmt.cond.__str__()] = 0
                    cond = ChironSSA.Var(f"{stmt.cond.__str__()}__{lastUsed[stmt.cond.__str__()]}")
                elif isinstance(stmt.cond, ChironTAC.Num):
                    cond = ChironSSA.Num(stmt.cond.value)
                ssa.append((ChironSSA.ConditionCommand(cond), tgt_block))
            ssaLineCounter += 1
        
        elif isinstance(stmt, ChironTAC.AssertCommand):
            if isinstance(stmt.cond, ChironTAC.BoolTrue):
                ssa.append((ChironSSA.AssertCommand(ChironSSA.BoolTrue()), tgt))
            elif isinstance(stmt.cond, ChironTAC.BoolFalse):
                ssa.append((ChironSSA.AssertCommand(ChironSSA.BoolFalse()), tgt))
            else:
                if isinstance(stmt.cond, ChironTAC.Var):
                    if stmt.cond.__str__() not in lastUsed.keys():
                        lastUsed[stmt.cond.__str__()] = 0
                    cond = ChironSSA.Var(f"{stmt.cond.__str__()}__{lastUsed[stmt.cond.__str__()]}")
                elif isinstance(stmt.cond, ChironTAC.Num):
                    cond = ChironSSA.Num(stmt.cond.value)
                ssa.append((ChironSSA.AssertCommand(cond), tgt))
            ssaLineCounter += 1
        
        elif isinstance(stmt, ChironTAC.MoveCommand):
            var = None
            if isinstance(stmt.var, ChironTAC.Var):
                if stmt.var.__str__() not in lastUsed.keys():
                    lastUsed[stmt.var.__str__()] = 0
                var = ChironSSA.Var(f"{stmt.var.__str__()}__{lastUsed[stmt.var.__str__()]}")
            elif isinstance(stmt.var, ChironTAC.Num):
                var = ChironSSA.Num(stmt.var.value)
            ssa.append((ChironSSA.MoveCommand(stmt.direction, var), tgt))
            ssaLineCounter += 1

        elif isinstance(stmt, ChironTAC.PenCommand):
            ssa.append((ChironSSA.PenCommand(stmt.status), tgt))
            ssaLineCounter += 1

        elif isinstance(stmt, ChironTAC.GotoCommand):
            x_var = None
            y_var = None
            if isinstance(stmt.xcor, ChironTAC.Var):
                if stmt.xcor.__str__() not in lastUsed.keys():
                    lastUsed[stmt.xcor.__str__()] = 0
                x_var = ChironSSA.Var(f"{stmt.xcor.__str__()}__{lastUsed[stmt.xcor.__str__()]}")
            elif isinstance(stmt.xcor, ChironTAC.Num):
                x_var = ChironSSA.Num(stmt.xcor.value)
            if isinstance(stmt.ycor, ChironTAC.Var):
                if stmt.ycor.__str__() not in lastUsed.keys():
                    lastUsed[stmt.ycor.__str__()] = 0
                y_var = ChironSSA.Var(f"{stmt.ycor.__str__()}__{lastUsed[stmt.ycor.__str__()]}")
            elif isinstance(stmt.ycor, ChironTAC.Num):
                y_var = ChironSSA.Num(stmt.ycor.value)
            ssa.append((ChironSSA.GotoCommand(x_var, y_var), tgt))
            ssaLineCounter += 1

        elif isinstance(stmt, ChironTAC.NoOpCommand):
            ssa.append((ChironSSA.NoOpCommand(), tgt))
            ssaLineCounter += 1
        
        elif isinstance(stmt, ChironTAC.PauseCommand):
            ssa.append((ChironSSA.PauseCommand(), tgt))
            ssaLineCounter += 1
        
        else:
            raise Exception(f"Unknown TAC command: {stmt}")
    
    block2ssaLine[line2BlockMap[len(tac)]] = ssaLineCounter
        
    for (stmt, tgt), line in zip(ssa, range(len(ssa))):
        if isinstance(stmt, ChironSSA.ConditionCommand):
            tgt = block2ssaLine[tgt] - line
            ssa[line] = (stmt, tgt)

    return ssa

def printSSA(ssa):
    """
    Prints SSA form.
    """
    print("\nSSA Form:")
    for (stmt, tgt), line in zip(ssa, range(len(ssa))):
            print(f"[L{line}]".rjust(5), stmt, f"[{tgt}]")

