from ChironAST import ChironAST

class TurtleCommandsCompiler():
    """
    A compiler for Turtle commands that translates high-level commands into low-level
    ChironAST commands for execution.

    Attributes:
        x (ChironAST.Var): Represents the x-coordinate of the turtle.
        y (ChironAST.Var): Represents the y-coordinate of the turtle.
        z (ChironAST.Var): Represents the pen status of the turtle (up or down).
        w (ChironAST.Var): Represents the direction/angle of the turtle.
    """

    def __init__(self):
        """
        Initializes the TurtleCommandsCompiler with variables representing the turtle's state.
        """
        self.x  = ChironAST.Var(":__turtleX")
        self.y  = ChironAST.Var(":__turtleY")
        self.z  = ChironAST.Var(":__turtleZ")
        self.w  = ChironAST.Var(":__turtleW")

    def compile_move_command(self, command: ChironAST.MoveCommand):
        """
        Compiles a MoveCommand into ChironAST commands.

        Args:
            command (ChironAST.MoveCommand): The move command to compile.

        Returns:
            list: A list of ChironAST commands representing the move operation.
        """
        new_command = ChironAST.NoOpCommand()  # Default to a no-op command

        # Handle left turn
        if(command.direction == "left"):
            lexpr = self.w
            rexpr = ChironAST.Sum(self.w, command.expr)
            num = ChironAST.Num(360)
            rexpr = ChironAST.Mod(rexpr, num)  # Ensure the angle stays within 0-360
            new_command = ChironAST.AssignmentCommand(lexpr, rexpr)

        # Handle right turn
        if(command.direction == "right"):
            lexpr = self.w
            rexpr = ChironAST.Diff(self.w, command.expr)
            num = ChironAST.Num(360)
            rexpr = ChironAST.Mod(rexpr, num)  # Ensure the angle stays within 0-360
            new_command = ChironAST.AssignmentCommand(lexpr, rexpr)

        # Handle forward movement
        if(command.direction == "forward"):
            commands = []

            # Calculate the new x and y coordinates based on the direction
            n = ChironAST.Div(self.w, ChironAST.Num(90))  # Determine the quadrant
            n_mod2 = ChironAST.Mod(n, ChironAST.Num(2))
            n_div2 = ChironAST.Div(n, ChironAST.Num(2))
            term2 = ChironAST.Diff(ChironAST.Num(1), ChironAST.Mult(ChironAST.Num(2), n_div2))
            term1 = ChironAST.Diff(ChironAST.Num(1), n_mod2)

            # Update x-coordinate
            commands.append(
                ChironAST.AssignmentCommand(
                    self.x,
                    ChironAST.Sum(
                        self.x,
                        ChironAST.Mult(command.expr, ChironAST.Mult(term1, term2))
                    )
                )
            )

            # Update y-coordinate
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

        # Handle backward movement
        if(command.direction == "backward"):
            commands = []

            # Calculate the new x and y coordinates based on the direction
            n = ChironAST.Div(self.w, ChironAST.Num(90))  # Determine the quadrant
            n_mod2 = ChironAST.Mod(n, ChironAST.Num(2))
            n_div2 = ChironAST.Div(n, ChironAST.Num(2))
            term2 = ChironAST.Diff(ChironAST.Mult(ChironAST.Num(2), n_div2), ChironAST.Num(1))
            term1 = ChironAST.Diff(ChironAST.Num(1), n_mod2)

            # Update x-coordinate
            commands.append(
                ChironAST.AssignmentCommand(
                    self.x,
                    ChironAST.Sum(
                        self.x,
                        ChironAST.Mult(command.expr, ChironAST.Mult(term1, term2))
                    )
                )
            )

            # Update y-coordinate
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
        """
        Compiles a GotoCommand into ChironAST commands.

        Args:
            command (ChironAST.GotoCommand): The goto command to compile.

        Returns:
            list: A list of ChironAST commands to set the turtle's x and y coordinates.
        """
        new_command1 = ChironAST.AssignmentCommand(self.x, command.xcor)  # Set x-coordinate
        new_command2 = ChironAST.AssignmentCommand(self.y, command.ycor)  # Set y-coordinate
        return [new_command1, new_command2]

    def compile_pen_command(self, command: ChironAST.PenCommand):
        """
        Compiles a PenCommand into ChironAST commands.

        Args:
            command (ChironAST.PenCommand): The pen command to compile.

        Returns:
            list: A list of ChironAST commands to update the pen status.
        """
        new_penstat = 0 if command.status == 'pendown' else 1  # Map pen status to 0 or 1
        new_penstat = ChironAST.Num(new_penstat)
        new_command = ChironAST.AssignmentCommand(self.z, new_penstat)  # Update pen status
        return [new_command]

    def compile(self, command):
        """
        Compiles a generic command into ChironAST commands.

        Args:
            command: The command to compile.

        Returns:
            list: A list of ChironAST commands representing the compiled command.
        """
        # Handle NoOpCommand
        if (type(command) == ChironAST.NoOpCommand):
            return []

        # Handle MoveCommand
        if(type(command) == ChironAST.MoveCommand):
            return self.compile_move_command(command)

        # Handle GotoCommand
        if(type(command) == ChironAST.GotoCommand):
            return self.compile_goto_command(command)

        # Handle PenCommand
        if(type(command) == ChironAST.PenCommand):
            return self.compile_pen_command(command)

        # Return the command as-is if no specific compilation is required
        return [command]
