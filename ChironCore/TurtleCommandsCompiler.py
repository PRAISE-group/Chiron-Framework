from ChironAST import ChironAST

class TurtleCommandsCompiler():
    def __init__(self):
        self.x  = ChironAST.Var(":__turtleX")
        self.y  = ChironAST.Var(":__turtleY")
        self.z  = ChironAST.Var(":__turtleZ")
        self.w  = ChironAST.Var(":__turtleW")
    def compile_move_command(self, command: ChironAST.MoveCommand):
        new_command = ChironAST.NoOpCommand()
        if(command.direction == "left"):
            lexpr = self.w
            rexpr = ChironAST.Sum(self.w, command.expr)
            num = ChironAST.Num(360)
            rexpr = ChironAST.Mod(rexpr, num)
            new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
            
        
        if(command.direction == "right"):
            lexpr = self.w
            rexpr = ChironAST.Diff(self.w, command.expr)
            num = ChironAST.Num(360)
            rexpr = ChironAST.Mod(rexpr, num)
            new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
            
        if(command.direction == "forward"):
            commands = []

            # x = x + forw_amt*((1-(n%2))*(1-2*(n//2)))
            # y = y + forw_amt*((n%2)*(1-2*(n//2)))

            n = ChironAST.Div(self.w, ChironAST.Num(90))
            n_mod2 = ChironAST.Mod(n, ChironAST.Num(2))
            n_div2 = ChironAST.Div(n, ChironAST.Num(2))
            term2 = ChironAST.Diff(ChironAST.Num(1), ChironAST.Mult(ChironAST.Num(2), n_div2))
            term1 = ChironAST.Diff(ChironAST.Num(1), n_mod2)
            commands.append(
                ChironAST.AssignmentCommand(
                    self.x,
                    ChironAST.Sum(
                        self.x,
                        ChironAST.Mult(command.expr, ChironAST.Mult(term1, term2))
                    )
                )
            )
            commands.append(
                ChironAST.AssignmentCommand(
                    self.y,
                    ChironAST.Sum(
                        self.y,
                        ChironAST.Mult(command.expr, ChironAST.Mult(n_mod2, term2))
                    )
                )
            )
            return commands

        if(command.direction == "backward"):
            commands = []
            n = ChironAST.Div(self.w, ChironAST.Num(90))
            n_mod2 = ChironAST.Mod(n, ChironAST.Num(2))
            n_div2 = ChironAST.Div(n, ChironAST.Num(2))
            term2 = ChironAST.Diff(ChironAST.Mult(ChironAST.Num(2), n_div2), ChironAST.Num(1))
            term1 = ChironAST.Diff(ChironAST.Num(1), n_mod2)
            commands.append(
                ChironAST.AssignmentCommand(
                    self.x,
                    ChironAST.Sum(
                        self.x,
                        ChironAST.Mult(command.expr, ChironAST.Mult(term1, term2))
                    )
                )
            )
            commands.append(
                ChironAST.AssignmentCommand(
                    self.y,
                    ChironAST.Sum(
                        self.y,
                        ChironAST.Mult(command.expr, ChironAST.Mult(n_mod2, term2))
                    )
                )
            )
            return commands
        
        return [new_command]
        
    def compile_goto_command(self, command: ChironAST.GotoCommand):
        new_command1 = ChironAST.AssignmentCommand(self.x, command.xcor)
        new_command2 = ChironAST.AssignmentCommand(self.y, command.ycor)
        return [new_command1, new_command2]
    
    def compile_pen_command(self, command: ChironAST.PenCommand):
        new_penstat = 0 if command.status == 'pendown' else 1 
        new_penstat = ChironAST.Num(new_penstat)
        new_command = ChironAST.AssignmentCommand(self.z, new_penstat)
        return [new_command]
    
    def compile(self, command):
        # print(command)
        if(type(command) == ChironAST.MoveCommand):
            return self.compile_move_command(command)
        if(type(command) == ChironAST.GotoCommand):
            return self.compile_goto_command(command)
        if(type(command) == ChironAST.PenCommand):
            return self.compile_pen_command(command)
        return [command]
