
from ChironAST import ChironAST
from ChironHooks import Chironhooks
import turtle
import re
Release="Chiron v5.3"

def addContext(s):
    s= re.sub(r'(?<!\.):', 'self.prg.', str(s).strip())
    s= str(s).strip().replace(":", "")
    return s


class Interpreter:
    # Turtle program should not contain variable with names "ir", "pc", "t_screen"
    ir = None
    pc = None
    t_screen = None
    trtl = None

    def __init__(self, irHandler, params):
        self.ir = irHandler.ir
        self.cfg = irHandler.cfg
        self.pc = 0
        self.t_screen = turtle.getscreen()
        self.trtl = turtle.Turtle()
        self.trtl.shape("turtle")
        self.trtl.color("blue", "yellow")
        self.trtl.fillcolor("green")
        self.trtl.begin_fill()
        self.trtl.pensize(4)
        self.trtl.speed(1) # TODO: Make it user friendly

        if params is not None:
            self.args = params
        else:
            self.args = None

        turtle.title(Release)
        turtle.bgcolor("white")
        turtle.hideturtle()

    def handleAssignment(self, stmt,tgt):
        raise NotImplementedError('Assignments are not handled!')

    def handleCondition(self, stmt, tgt):
        raise NotImplementedError('Conditions are not handled!')

    def handleMove(self, stmt, tgt):
        raise NotImplementedError('Moves are not handled!')

    def handlePen(self, stmt, tgt):
        raise NotImplementedError('Pens are not handled!')

    def handleGotoCommand(self, stmt, tgt):
        raise NotImplementedError('Gotos are not handled!')

    def handleNoOpCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def handlePauseCommand(self, stmt, tgt):
        raise NotImplementedError('No-Ops are not handled!')

    def sanityCheck(self, irInstr):
        stmt, tgt = irInstr
        # if not a condition command, rel. jump can't be anything but 1
        if not isinstance(stmt, ChironAST.ConditionCommand) and not isinstance(stmt, ChironAST.FunctionDeclarationCommand):
            if tgt != 1:
                raise ValueError("Improper relative jump for non-conditional instruction", str(stmt), tgt)
    
    def interpret(self):
        pass

    def initProgramContext(self, params):
        pass

class ProgramContext:
    pass

# TODO: move to a different file
class ConcreteInterpreter(Interpreter):
    # Ref: https://realpython.com/beginners-guide-python-turtle
    cond_eval = None # used as a temporary variable within the embedded program interpreter
    prg = None
    argument = None

    # map of function name to their pc in the IR
    function_addresses = {}
    #stack for handling function calls
    call_stack = []

    def __init__(self, irHandler, params):
        super().__init__(irHandler, params)
        self.prg = ProgramContext()
        # Hooks Object:
        if self.args is not None and self.args.hooks:
            self.chironhook = Chironhooks.ConcreteChironHooks()
        self.pc = 0

    def interpret(self):
        print("Program counter : ", self.pc)
        stmt, tgt = self.ir[self.pc]
        print(stmt, stmt.__class__.__name__, tgt)

        self.sanityCheck(self.ir[self.pc])

        if isinstance(stmt, ChironAST.AssignmentCommand):
            ntgt = self.handleAssignment(stmt, tgt)
        elif isinstance(stmt, ChironAST.PrintCommand):
            ntgt = self.handlePrint(stmt, tgt)
        elif isinstance(stmt, ChironAST.ConditionCommand):
            ntgt = self.handleCondition(stmt, tgt)
        elif isinstance(stmt, ChironAST.MoveCommand):
            ntgt = self.handleMove(stmt, tgt)
        elif isinstance(stmt, ChironAST.PenCommand):
            ntgt = self.handlePen(stmt, tgt)
        elif isinstance(stmt, ChironAST.GotoCommand):
            ntgt = self.handleGotoCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.NoOpCommand):
            ntgt = self.handleNoOpCommand(stmt, tgt)
        elif isinstance(stmt, ChironAST.ClassDeclarationCommand):
            ntgt = self.handleClassDeclaration(stmt, tgt)
        elif isinstance(stmt, ChironAST.ObjectInstantiationCommand):
            ntgt = self.handleObjectInstantiation(stmt, tgt)
        elif isinstance(stmt, ChironAST.FunctionDeclarationCommand):
            ntgt = self.handleFunctionDeclaration(stmt, tgt)
        elif isinstance(stmt, ChironAST.FunctionCallCommand):
            ntgt = self.handleFunctionCall(stmt, tgt)
        elif isinstance(stmt, ChironAST.ReturnCommand):
            ntgt = self.handleFunctionReturn(stmt, tgt)
        elif isinstance(stmt, ChironAST.ParametersPassingCommand):
            ntgt = self.handleParametersPassing(stmt, tgt)
             
        else:
            raise NotImplementedError("Unknown instruction: %s, %s."%(type(stmt), stmt))

        # TODO: handle statement
        self.pc += ntgt

        if self.pc >= len(self.ir):
            # This is the ending of the interpreter.
            self.trtl.write("End, Press ESC", font=("Arial", 15, "bold"))
            if self.args is not None and self.args.hooks:
                self.chironhook.ChironEndHook(self)
            return True
        else:
            return False
    
    def initProgramContext(self, params):
        # This is the starting of the interpreter at setup stage.
        if self.args is not None and self.args.hooks:
            self.chironhook.ChironStartHook(self)
        self.trtl.write("Start", font=("Arial", 15, "bold"))
        for key,val in params.items():
            var = key.replace(":","")
            exec("setattr(self.prg,\"%s\",%s)" % (var, val))
    
    def handleFunctionDeclaration(self, stmt, tgt):
        print(f"Function Declaration: {stmt.name}")
        self.function_addresses[stmt.name] = self.pc + 1
        return tgt
    
    def handleFunctionCall(self, stmt, tgt):
        print(f"Function Call: {stmt.name}")
        self.call_stack.append(self.pc + 1)
        # Save the current program context
        self.call_stack.append(self.prg)
        # Initialize a new program context for the function call
        for arg in stmt.args:
            arg_value = addContext(arg)
            exec(f"self.argument = {arg_value}")
            self.call_stack.append(self.argument)
        self.prg = ProgramContext()
        self.pc = self.function_addresses[stmt.name]
        return 0

    def handleFunctionReturn(self, stmt, tgt):
        print(f"Function Return: {stmt}")
        # Restore the previous program context
        self.prg = self.call_stack.pop()
        self.pc = self.call_stack.pop()
        return 0

    def handleParametersPassing(self, stmt, tgt):
        print(f"Parameters Passing: {stmt.params}")
        for param in reversed(stmt.params):
            param = str(param).replace(":", "")
            param_value = self.call_stack.pop()
            exec(f"self.prg.{param} = {param_value}")
        return 1

    def handleClassDeclaration(self, stmt, tgt):
        print(f"  Class Declaration: {stmt.className}")

        className = stmt.className.replace(":","")
        attributes = stmt.attributes  # List of attribute assignments

        class_def = f"class {className}:\n"

        for attr in attributes:
            attr, target= attr
            attr_name = str(attr.lvar).replace(":", "")
            attr_value = addContext(attr.rexpr) if attr.rexpr else None
            class_def += f"    {attr_name} = {attr_value}\n"

        print(class_def, "Class Definition")

        exec(class_def, globals(), self.prg.__dict__)  # Define class dynamically

        return 1        


    def handleObjectInstantiation(self, stmt, tgt):
        print(f"Creating new instance of {stmt.class_name} for {stmt.target}")

        x= self.prg.a()
        print(x)


        lhs = str(stmt.target).replace(":","")
        rhs = addContext(stmt.class_name)

        # Generate and execute Python class instantiation dynamically
        instance_code = f"{lhs} = {rhs}()"
        print(instance_code)
        # exec(instance_code, globals(), self.prg.__dict__)  # Store in self.prg
        exec(f"self.prg.{lhs} = {rhs}()")

        return 1

    
    
    def handleAssignment(self, stmt, tgt):
        print("  Assignment Statement")
        lhs = str(stmt.lvar).replace(":","")
        rhs = addContext(stmt.rexpr)
        print(lhs,rhs,"Assignment")
        # exec("setattr(self.prg,\"%s\",%s)" % (lhs,rhs))
        exec(f"self.prg.{lhs} = {rhs}")
        return 1
    
    def handlePrint(self,stmt,tgt):
        print( " PrintCommand")
        expr = addContext(stmt.expr)
        print("Executing print with expression:", expr)
        exec("print(%s)" % expr)
        return 1

    def handleCondition(self, stmt, tgt):
        print("  Branch Instruction")
        condstr = addContext(stmt)
        exec("self.cond_eval = %s" % (condstr))
        return 1 if self.cond_eval else tgt

    def handleMove(self, stmt, tgt):
        print("  MoveCommand")
        exec("self.trtl.%s(%s)" % (stmt.direction,addContext(stmt.expr)))
        return 1
    


    def handleNoOpCommand(self, stmt, tgt):
        print("  No-Op Command")
        return 1

    def handlePen(self, stmt, tgt):
        print("  PenCommand")
        exec("self.trtl.%s()"%(stmt.status))
        return 1

    def handleGotoCommand(self, stmt, tgt):
        print(" GotoCommand")
        xcor = addContext(stmt.xcor)
        ycor = addContext(stmt.ycor)
        exec("self.trtl.goto(%s, %s)" % (xcor, ycor))
        return 1
