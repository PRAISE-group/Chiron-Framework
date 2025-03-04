from cfg.ChironCFG import *
import ChironAST.ChironTAC as ChironTAC
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
        if isinstance(stmt, ChironTAC.TAC_AssignmentCommand):
            varCounter[stmt.lvar.__str__()] = 0
            lastDeclaration[line2BlockMap[line]] = {}
    for node in cfg:
        phiStatements[node] = {}

    # Renamed the declarations of variables in TAC
    for (stmt, tgt), line in zip(tac, range(len(tac))):
        if isinstance(stmt, ChironTAC.TAC_AssignmentCommand):
            var = stmt.lvar.__str__()
            lastDeclaration[line2BlockMap[line]][var] = varCounter[var]
            varCounter[var] += 1
            stmt.lvar = ChironTAC.TAC_Var(f"{var}__{varCounter[var] - 1}")
            tac[line] = (stmt, tgt)

    for node in cfg:
        predes = cfg.predecessors(node)
        for parent in predes:
            if lastDeclaration.get(parent) == None:
                continue

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
                    ssa.append((ChironSSA.SSA_PhiCommand(ChironSSA.SSA_Var(f"{var}__{varCounter[var]}"), [ChironSSA.SSA_Var(f"{var}__{version}") for version in phiStatements[node][var]]), 1))
                    lastUsed[var] = varCounter[var]
                    varCounter[var] += 1

        if isinstance(stmt, ChironTAC.TAC_AssignmentCommand):
            rvar1 = None
            rvar2 = None
            if isinstance(stmt.rvar1, ChironTAC.TAC_Var):
                if stmt.rvar1.__str__() not in lastUsed.keys():
                    lastUsed[stmt.rvar1.__str__()] = 0
                rvar1 = ChironSSA.SSA_Var(f"{stmt.rvar1.__str__()}__{lastUsed[stmt.rvar1.__str__()]}")
            elif isinstance(stmt.rvar1, ChironTAC.TAC_BoolTrue):
                rvar1 = ChironSSA.SSA_BoolTrue()
            elif isinstance(stmt.rvar1, ChironTAC.TAC_BoolFalse):
                rvar1 = ChironSSA.SSA_BoolFalse()
            elif isinstance(stmt.rvar1, ChironTAC.TAC_Num):
                rvar1 = ChironSSA.SSA_Num(stmt.rvar1.value)
            if isinstance(stmt.rvar2, ChironTAC.TAC_Var):
                if stmt.rvar2.__str__() not in lastUsed.keys():
                    lastUsed[stmt.rvar2.__str__()] = 0
                rvar2 = ChironSSA.SSA_Var(f"{stmt.rvar2.__str__()}__{lastUsed[stmt.rvar2.__str__()]}")
            elif isinstance(stmt.rvar2, ChironTAC.TAC_BoolTrue):
                rvar2 = ChironSSA.SSA_BoolTrue()
            elif isinstance(stmt.rvar2, ChironTAC.TAC_BoolFalse):
                rvar2 = ChironSSA.SSA_BoolFalse()
            elif isinstance(stmt.rvar2, ChironTAC.TAC_Num):
                rvar2 = ChironSSA.SSA_Num(stmt.rvar2.value)
            lvar = ChironSSA.SSA_Var(f"{stmt.lvar.__str__()}")
            
            lvar_string = lvar.__str__().rsplit('__', 1)[0]
            lastUsed[lvar_string] = int(lvar.__str__().rsplit('__', 1)[1])
            
            ssaLineCounter += 1
            ssa.append((ChironSSA.SSA_AssignmentCommand(lvar, rvar1, rvar2, stmt.op), tgt))

        elif isinstance(stmt, ChironTAC.TAC_ConditionCommand):
            tgt_block = line2BlockMap[line + tgt]
            if isinstance(stmt.cond, ChironTAC.TAC_BoolTrue):
                ssa.append((ChironSSA.SSA_ConditionCommand(ChironSSA.SSA_BoolTrue()), tgt_block))
            elif isinstance(stmt.cond, ChironTAC.TAC_BoolFalse):
                ssa.append((ChironSSA.SSA_ConditionCommand(ChironSSA.SSA_BoolFalse()), tgt_block))
            else:
                if isinstance(stmt.cond, ChironTAC.TAC_Var):
                    if stmt.cond.__str__() not in lastUsed.keys():
                        lastUsed[stmt.cond.__str__()] = 0
                    cond = ChironSSA.SSA_Var(f"{stmt.cond.__str__()}__{lastUsed[stmt.cond.__str__()]}")
                elif isinstance(stmt.cond, ChironTAC.TAC_Num):
                    cond = ChironSSA.SSA_Num(stmt.cond.value)
                ssa.append((ChironSSA.SSA_ConditionCommand(cond), tgt_block))
            ssaLineCounter += 1
        
        elif isinstance(stmt, ChironTAC.TAC_AssertCommand):
            if isinstance(stmt.cond, ChironTAC.TAC_BoolTrue):
                ssa.append((ChironSSA.SSA_AssertCommand(ChironSSA.SSA_BoolTrue()), tgt))
            elif isinstance(stmt.cond, ChironTAC.TAC_BoolFalse):
                ssa.append((ChironSSA.SSA_AssertCommand(ChironSSA.SSA_BoolFalse()), tgt))
            else:
                if isinstance(stmt.cond, ChironTAC.TAC_Var):
                    if stmt.cond.__str__() not in lastUsed.keys():
                        lastUsed[stmt.cond.__str__()] = 0
                    cond = ChironSSA.SSA_Var(f"{stmt.cond.__str__()}__{lastUsed[stmt.cond.__str__()]}")
                elif isinstance(stmt.cond, ChironTAC.TAC_Num):
                    cond = ChironSSA.SSA_Num(stmt.cond.value)
                ssa.append((ChironSSA.SSA_AssertCommand(cond), tgt))
            ssaLineCounter += 1
        
        elif isinstance(stmt, ChironTAC.TAC_MoveCommand):
            var = None
            if isinstance(stmt.var, ChironTAC.TAC_Var):
                if stmt.var.__str__() not in lastUsed.keys():
                    lastUsed[stmt.var.__str__()] = 0
                var = ChironSSA.SSA_Var(f"{stmt.var.__str__()}__{lastUsed[stmt.var.__str__()]}")
            elif isinstance(stmt.var, ChironTAC.TAC_Num):
                var = ChironSSA.SSA_Num(stmt.var.value)
            ssa.append((ChironSSA.SSA_MoveCommand(stmt.direction, var), tgt))
            ssaLineCounter += 1

        elif isinstance(stmt, ChironTAC.TAC_PenCommand):
            ssa.append((ChironSSA.SSA_PenCommand(stmt.status), tgt))
            ssaLineCounter += 1

        elif isinstance(stmt, ChironTAC.TAC_GotoCommand):
            x_var = None
            y_var = None
            if isinstance(stmt.xcor, ChironTAC.TAC_Var):
                if stmt.xcor.__str__() not in lastUsed.keys():
                    lastUsed[stmt.xcor.__str__()] = 0
                x_var = ChironSSA.SSA_Var(f"{stmt.xcor.__str__()}__{lastUsed[stmt.xcor.__str__()]}")
            elif isinstance(stmt.xcor, ChironTAC.TAC_Num):
                x_var = ChironSSA.SSA_Num(stmt.xcor.value)
            if isinstance(stmt.ycor, ChironTAC.TAC_Var):
                if stmt.ycor.__str__() not in lastUsed.keys():
                    lastUsed[stmt.ycor.__str__()] = 0
                y_var = ChironSSA.SSA_Var(f"{stmt.ycor.__str__()}__{lastUsed[stmt.ycor.__str__()]}")
            elif isinstance(stmt.ycor, ChironTAC.TAC_Num):
                y_var = ChironSSA.SSA_Num(stmt.ycor.value)
            ssa.append((ChironSSA.SSA_GotoCommand(x_var, y_var), tgt))
            ssaLineCounter += 1

        elif isinstance(stmt, ChironTAC.TAC_NoOpCommand):
            ssa.append((ChironSSA.SSA_NoOpCommand(), tgt))
            ssaLineCounter += 1
        
        elif isinstance(stmt, ChironTAC.TAC_PauseCommand):
            ssa.append((ChironSSA.SSA_PauseCommand(), tgt))
            ssaLineCounter += 1
        
        else:
            raise Exception(f"Unknown TAC command: {stmt}")
    
    block2ssaLine[line2BlockMap[len(tac)]] = ssaLineCounter
        
    for (stmt, tgt), line in zip(ssa, range(len(ssa))):
        if isinstance(stmt, ChironSSA.SSA_ConditionCommand):
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
