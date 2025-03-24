"""
Class for converting IR to Three Address Code (TAC)
"""

from ChironAST import ChironAST
from ChironTAC import ChironTAC


class TACGenerator:
    def __init__(self, ir):
        self.ir = ir
        self.tac = []
        self.tempCount = 0
        self.branchCount = 0
        self.assertCount = 0
        self.moveCount = 0
        self.gotoCount = 0
        self.ast_to_tac_line = {}
        self.line = 0
        self.freeVars = set()

    def parseExpresssion(self, expr, dest):
        """
        Parse the expression and return the TAC for the expression.
        """
        if isinstance(expr, ChironAST.BinArithOp):
            left = None
            right = None
            if isinstance(expr.lexpr, ChironAST.Num):
                left = ChironTAC.Num(expr.lexpr.val)
            elif isinstance(expr.lexpr, ChironAST.Var):
                left = ChironTAC.Var(expr.lexpr.varname)
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                left = temp
                self.parseExpresssion(expr.lexpr, temp)

            if isinstance(expr.rexpr, ChironAST.Num):
                right = ChironTAC.Num(expr.rexpr.val)
            elif isinstance(expr.rexpr, ChironAST.Var):
                right = ChironTAC.Var(expr.rexpr.varname)
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                right = temp
                self.parseExpresssion(expr.rexpr, temp)

            self.line += 1
            self.tac.append(
                (ChironTAC.AssignmentCommand(dest, left, right, expr.symbol), 1)
            )
        elif isinstance(expr, ChironAST.UMinus):
            if isinstance(expr.expr, ChironAST.Num):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.AssignmentCommand(
                            dest,
                            ChironTAC.Num(0),
                            ChironTAC.Num(expr.expr.val),
                            "-",
                        ),
                        1,
                    ),
                )
            elif isinstance(expr.expr, ChironAST.Var):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.AssignmentCommand(
                            dest,
                            ChironTAC.Num(0),
                            ChironTAC.Var(expr.expr.varname),
                            "-",
                        ),
                        1,
                    ),
                )
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                self.parseExpresssion(expr.expr, temp)
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.AssignmentCommand(
                            dest, ChironTAC.Num(0), temp, "-"
                        ),
                        1,
                    )
                )
        elif isinstance(expr, ChironAST.BinCondOp) and not (
            isinstance(expr, ChironAST.AND)
            or isinstance(expr, ChironAST.OR)
            or isinstance(expr, ChironAST.NOT)
        ):
            left = None
            right = None
            if isinstance(expr.lexpr, ChironAST.Num):
                left = ChironTAC.Num(expr.lexpr.val)
            elif isinstance(expr.lexpr, ChironAST.Var):
                left = ChironTAC.Var(expr.lexpr.varname)
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                left = temp
                self.parseExpresssion(expr.lexpr, temp)

            if isinstance(expr.rexpr, ChironAST.Num):
                right = ChironTAC.Num(expr.rexpr.val)
            elif isinstance(expr.rexpr, ChironAST.Var):
                right = ChironTAC.Var(expr.rexpr.varname)
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                right = temp
                self.parseExpresssion(expr.rexpr, temp)

            self.line += 1
            self.tac.append(
                (ChironTAC.AssignmentCommand(dest, left, right, expr.symbol), 1)
            )
        elif isinstance(expr, ChironAST.AND) or isinstance(expr, ChironAST.OR):
            left = None
            right = None
            if isinstance(expr.lexpr, ChironAST.BoolTrue):
                left = ChironTAC.BoolTrue()
            elif isinstance(expr.lexpr, ChironAST.BoolFalse):
                left = ChironTAC.BoolFalse()
            elif isinstance(expr.lexpr, ChironAST.Var):
                left = ChironTAC.Var(expr.lexpr.varname)
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                left = temp
                self.parseExpresssion(expr.lexpr, temp)

            if isinstance(expr.rexpr, ChironAST.BoolTrue):
                right = ChironTAC.BoolTrue()
            elif isinstance(expr.rexpr, ChironAST.BoolFalse):
                right = ChironTAC.BoolFalse()
            elif isinstance(expr.rexpr, ChironAST.Var):
                right = ChironTAC.Var(expr.rexpr.varname)
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                right = temp
                self.parseExpresssion(expr.rexpr, temp)

            self.line += 1
            self.tac.append(
                (ChironTAC.AssignmentCommand(dest, left, right, expr.symbol), 1)
            )
        elif isinstance(expr, ChironAST.NOT):
            if isinstance(expr.expr, ChironAST.BoolTrue):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.AssignmentCommand(
                            dest,
                            ChironTAC.Unused(),
                            ChironTAC.BoolTrue(),
                            "not",
                        ),
                        1,
                    )
                )
            elif isinstance(expr.expr, ChironAST.BoolFalse):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.AssignmentCommand(
                            dest,
                            ChironTAC.Unused(),
                            ChironTAC.BoolFalse(),
                            "not",
                        ),
                        1,
                    )
                )
            elif isinstance(expr.expr, ChironAST.Var):
                self.line += 1
                self.tac.append(
                    (
                        ChironTAC.AssignmentCommand(
                            dest,
                            ChironTAC.Unused(),
                            ChironTAC.Var(expr.expr.varname),
                            "not",
                        ),
                        1,
                    )
                )
            else:
                temp = ChironTAC.Var(f":__temp_{self.tempCount}")
                self.tempCount += 1
                self.parseExpresssion(expr.expr, temp)
                self.line += 1
                self.tac.append(
                    (ChironTAC.AssignmentCommand(dest, None, temp, "not"), 1)
                )
        elif isinstance(expr, ChironAST.Var):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.AssignmentCommand(
                        dest, ChironTAC.Num(0), ChironTAC.Var(expr.varname), "+"
                    ),
                    1,
                )
            )
        elif isinstance(expr, ChironAST.Num):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.AssignmentCommand(
                        dest, ChironTAC.Num(0), ChironTAC.Num(expr.val), "+"
                    ),
                    1,
                )
            )
        elif isinstance(expr, ChironAST.BoolTrue):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.AssignmentCommand(
                        dest, ChironTAC.Unused(), ChironTAC.BoolTrue(), ""
                    ),
                    1,
                )
            )
        elif isinstance(expr, ChironAST.BoolFalse):
            self.line += 1
            self.tac.append(
                (
                    ChironTAC.AssignmentCommand(
                        dest, ChironTAC.Unused(), ChironTAC.BoolFalse(), ""
                    ),
                    1,
                )
            )
        else:
            raise NotImplementedError(
                "Unknown expression: %s, %s." % (type(expr), expr)
            )

    def generateTAC(self):
        line_number = 0
        for stmt, tgt in self.ir:
            self.ast_to_tac_line[line_number] = self.line
            line_number += 1

            if isinstance(stmt, ChironAST.AssignmentCommand):
                self.parseExpresssion(stmt.rexpr, ChironTAC.Var(stmt.lvar.varname))

            elif isinstance(stmt, ChironAST.ConditionCommand):
                branchvar = None
                if isinstance(stmt.cond, ChironAST.BoolTrue):
                    branchvar = ChironTAC.BoolTrue()
                elif isinstance(stmt.cond, ChironAST.BoolFalse):
                    branchvar = ChironTAC.BoolFalse()
                elif isinstance(stmt.cond, ChironAST.Var):
                    branchvar = ChironTAC.Var(stmt.cond.varname)
                else:
                    branchvar = ChironTAC.Var(f":__branch_{self.branchCount}")
                    self.branchCount += 1
                    self.parseExpresssion(stmt.cond, branchvar)
                newtgt = line_number - 1 + tgt  # Adjusted later
                self.line += 1
                self.tac.append((ChironTAC.ConditionCommand(branchvar), newtgt))
            
            elif isinstance(stmt, ChironAST.AssertCommand):
                assertvar = ChironTAC.Var(f":__assert_{self.assertCount}")
                self.assertCount += 1
                self.parseExpresssion(stmt.cond, assertvar)
                self.line += 1
                self.tac.append((ChironTAC.AssertCommand(assertvar), 1))
            
            elif isinstance(stmt, ChironAST.MoveCommand):
                movevar = None
                if isinstance(stmt.expr, ChironAST.Num):
                    movevar = ChironTAC.Num(stmt.expr.val)
                elif isinstance(stmt.expr, ChironAST.Var):
                    movevar = ChironTAC.Var(stmt.expr.varname)
                else:
                    movevar = ChironTAC.Var(f":__move_{self.moveCount}")
                    self.moveCount += 1
                    self.parseExpresssion(stmt.expr, movevar)
                
                if (stmt.direction == "forward" or stmt.direction == "backward"):
                    self.line += 6
                    self.tac.append((ChironTAC.CosCommand(ChironTAC.Var(":__cos_theta"), ChironTAC.Var(":turtleThetaDeg")), 1))
                    self.tac.append((ChironTAC.SinCommand(ChironTAC.Var(":__sin_theta"), ChironTAC.Var(":turtleThetaDeg")), 1))
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":__delta_x"), movevar, ChironTAC.Var(":__cos_theta"), "*"), 1))
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":__delta_y"), movevar, ChironTAC.Var(":__sin_theta"), "*"), 1))
                    if (stmt.direction == "forward"):
                        self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleX"), ChironTAC.Var(":turtleX"), ChironTAC.Var(":__delta_x"), "+"), 1))
                        self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleY"), ChironTAC.Var(":turtleY"), ChironTAC.Var(":__delta_y"), "+"), 1))
                    elif (stmt.direction == "backward"):
                        self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleX"), ChironTAC.Var(":turtleX"), ChironTAC.Var(":__delta_x"), "-"), 1))
                        self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleY"), ChironTAC.Var(":turtleY"), ChironTAC.Var(":__delta_y"), "-"), 1))
                elif (stmt.direction == "left"):
                    self.line += 2
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Var(":turtleThetaDeg"), movevar, "-"), 1))
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Num(360), "%"), 1))
                elif (stmt.direction == "right"):
                    self.line += 2
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Var(":turtleThetaDeg"), movevar, "+"), 1))
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Num(360), "%"), 1))
                else:
                    raise NotImplementedError("Unknown move direction: %s, %s." % (type(stmt), stmt))
                
                self.line += 1
                self.tac.append((ChironTAC.MoveCommand(stmt.direction, movevar), 1))
            
            elif isinstance(stmt, ChironAST.PenCommand):
                self.line += 2
                if (stmt.status == "penup"):
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtlePen"), ChironTAC.Num(1), ChironTAC.Num(0), "+"), 1))
                elif (stmt.status == "pendown"):
                    self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtlePen"), ChironTAC.Num(0), ChironTAC.Num(0), "+"), 1))
                else:
                    raise NotImplementedError("Unknown pen status: %s, %s." % (type(stmt), stmt))
                self.tac.append((ChironTAC.PenCommand(stmt.status), 1))
            
            elif isinstance(stmt, ChironAST.GotoCommand):
                xvar = None
                yvar = None
                if isinstance(stmt.xcor, ChironAST.Num):
                    xvar = ChironTAC.Num(stmt.xcor.val)
                elif isinstance(stmt.xcor, ChironAST.Var):
                    xvar = ChironTAC.Var(stmt.xcor.varname)
                else:
                    xvar = ChironTAC.Var(f":__x_{self.gotoCount}")
                    self.gotoCount += 1
                    self.parseExpresssion(stmt.xcor, xvar)
                if isinstance(stmt.ycor, ChironAST.Num):
                    yvar = ChironTAC.Num(stmt.ycor.val)
                elif isinstance(stmt.ycor, ChironAST.Var):
                    yvar = ChironTAC.Var(stmt.ycor.varname)
                else:
                    yvar = ChironTAC.Var(f":__y_{self.gotoCount}")
                    self.gotoCount += 1
                    self.parseExpresssion(stmt.ycor, yvar)
                self.line += 3
                self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleX"), xvar, ChironTAC.Num(0), "+"), 1))
                self.tac.append((ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleY"), yvar, ChironTAC.Num(0), "+"), 1))
                self.tac.append((ChironTAC.GotoCommand(xvar, yvar), 1))
            
            elif isinstance(stmt, ChironAST.NoOpCommand):
                self.line += 1
                self.tac.append((ChironTAC.NoOpCommand(), 1))
            
            elif isinstance(stmt, ChironAST.PauseCommand):
                self.line += 1
                self.tac.append((ChironTAC.PauseCommand(), 1))
            
            else:
                raise NotImplementedError(
                    "Unknown instruction: %s, %s." % (type(stmt), stmt)
                )

        self.ast_to_tac_line[line_number] = self.line

        for i in range(len(self.tac)):
            stmt, tgt = self.tac[i]
            if isinstance(stmt, ChironTAC.ConditionCommand):
                newtgt = self.ast_to_tac_line[tgt] - i
                self.tac[i] = (stmt, newtgt)

        self.handleMoveVariables()
        self.handleFreeVariables()

    def handleFreeVariables(self):
        self.freeVars = self.getFreeVariables()

        for var in self.freeVars:
            self.tac.insert(0, (ChironTAC.AssignmentCommand(ChironTAC.Var(var), ChironTAC.Unused(), ChironTAC.Unused(), ""), 1))
    
    def handleMoveVariables(self):
        self.tac.insert(0, (ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleX"), ChironTAC.Num(0), ChironTAC.Num(0), "+"), 1))
        self.tac.insert(0, (ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleY"), ChironTAC.Num(0), ChironTAC.Num(0), "+"), 1))
        self.tac.insert(0, (ChironTAC.AssignmentCommand(ChironTAC.Var(":turtleThetaDeg"), ChironTAC.Num(0), ChironTAC.Num(0), "+"), 1))
        self.tac.insert(0, (ChironTAC.AssignmentCommand(ChironTAC.Var(":turtlePen"), ChironTAC.Num(0), ChironTAC.Num(0), "+"), 1)) # 0->down 1->up
        
    def getFreeVariables(self):
        """
        Returns free variables in TAC.
        """
        if len(self.freeVars) > 0:
            return self.freeVars

        boundVars = set()
        for (stmt, _), _ in zip(self.tac, range(len(self.tac))):
            if isinstance(stmt, ChironTAC.AssignmentCommand):
                if isinstance(stmt.rvar1, ChironTAC.Var) and stmt.rvar1.__str__() not in boundVars:
                    self.freeVars.add(stmt.rvar1.__str__())
                if isinstance(stmt.rvar2, ChironTAC.Var) and stmt.rvar2.__str__() not in boundVars:
                    self.freeVars.add(stmt.rvar2.__str__())
                boundVars.add(stmt.lvar.__str__())
            elif isinstance(stmt, ChironTAC.ConditionCommand):
                if isinstance(stmt.cond, ChironTAC.Var) and stmt.cond.__str__() not in boundVars:
                    self.freeVars.add(stmt.cond.__str__())
            elif isinstance(stmt, ChironTAC.AssertCommand):
                if isinstance(stmt.cond, ChironTAC.Var) and stmt.cond.__str__() not in boundVars:
                    self.freeVars.add(stmt.cond.__str__())
            elif isinstance(stmt, ChironTAC.MoveCommand):
                if isinstance(stmt.var, ChironTAC.Var) and stmt.var.__str__() not in boundVars:
                    self.freeVars.add(stmt.var.__str__())
            elif isinstance(stmt, ChironTAC.GotoCommand):
                if isinstance(stmt.xcor, ChironTAC.Var) and stmt.xcor.__str__() not in boundVars:
                    self.freeVars.add(stmt.xcor.__str__())
                if isinstance(stmt.ycor, ChironTAC.Var) and stmt.ycor.__str__() not in boundVars:
                    self.freeVars.add(stmt.ycor.__str__())
            elif isinstance(stmt, ChironTAC.SinCommand):
                if isinstance(stmt.rvar, ChironTAC.Var) and stmt.rvar.__str__() not in boundVars:
                    self.freeVars.add(stmt.rvar.__str__())
                boundVars.add(stmt.lvar.__str__())
            elif isinstance(stmt, ChironTAC.CosCommand):
                if isinstance(stmt.rvar, ChironTAC.Var) and stmt.rvar.__str__() not in boundVars:
                    self.freeVars.add(stmt.rvar.__str__())
                boundVars.add(stmt.lvar.__str__())
    
        return self.freeVars


    def printTAC(self):
        for (stmt, tgt), line in zip(self.tac, range(len(self.tac))):
            print(f"[L{line}]".rjust(5), stmt, f"[{tgt}]")
