from ChironAST import ChironAST

class TurtleCommandsCompiler():
    def __init__(self):
        self.x  = ChironAST.Var(":__x")
        self.y  = ChironAST.Var(":__y")
        self.z  = ChironAST.Var(":__z")
        self.w  = ChironAST.Var(":__w")
    def compile_move_command(self, command: ChironAST.MoveCommand):
        new_command = ChironAST.NoOpCommand()
        if(command.direction == "left"):
            lexpr = self.w
            rexpr = ChironAST.Sum(self.w, command.expr)
            new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
            
        
        if(command.direction == "right"):
            lexpr = self.w
            rexpr = ChironAST.Diff(self.w, command.expr)
            new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
            
        # if(command.direction == "forward"):
        #     if(self.w%360 == 0):
        #         lexpr = self.x
        #         rexpr = ChironAST.Sum(self.x, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
                
        #     if(self.w%360 == 90):
        #         lexpr = self.y
        #         rexpr = ChironAST.Sum(self.y, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
                
        #     if(self.w%360 == 180):
        #         lexpr = self.x
        #         rexpr = ChironAST.Diff(self.x, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
                
        #     if(self.w%360 == 270):
        #         lexpr = self.y
        #         rexpr = ChironAST.Diff(self.y, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
        
        # if(command.direction == "backward"):
        #     if(self.w%360 == 0):
        #         lexpr = self.x
        #         rexpr = ChironAST.Diff(self.x, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
                
        #     if(self.w%360 == 90):
        #         lexpr = self.y
        #         rexpr = ChironAST.Diff(self.y, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
                
        #     if(self.w%360 == 180):
        #         lexpr = self.x
        #         rexpr = ChironAST.Sum(self.x, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
                
        #     if(self.w%360 == 270):
        #         lexpr = self.y
        #         rexpr = ChironAST.Sum(self.y, command.expr)
        #         new_command = ChironAST.AssignmentCommand(lexpr, rexpr)
        
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
        print(command)
        if(type(command) == ChironAST.MoveCommand):
            return self.compile_move_command(command)
        if(type(command) == ChironAST.GotoCommand):
            return self.compile_goto_command(command)
        if(type(command) == ChironAST.PenCommand):
            return self.compile_pen_command(command)
        return [command]
    