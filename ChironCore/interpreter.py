
from ChironAST import ChironAST
from ChironHooks import Chironhooks
import turtle
import re
Release = "Chiron v5.3"


def addContext(s):
    s = re.sub(r'(?<!\.):', 'self.prg.', str(s).strip())
    s = str(s).strip().replace(":", "")

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
        self.trtl.speed(1)  # TODO: Make it user friendly

        if params is not None:
            self.args = params
        else:
            self.args = None

        turtle.title(Release)
        turtle.bgcolor("white")
        turtle.hideturtle()

    def handleAssignment(self, stmt, tgt):
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
                raise ValueError(
                    "Improper relative jump for non-conditional instruction", str(stmt), tgt)

    def interpret(self):
        pass

    def initProgramContext(self, params):
        pass


class ProgramContext:
    pass


class ClassList:
    pass

# TODO: move to a different file


class ConcreteInterpreter(Interpreter):
    # Ref: https://realpython.com/beginners-guide-python-turtle
    cond_eval = None  # used as a temporary variable within the embedded program interpreter
    prg = None
    # virtual argument register
    argument = None
    # virtual return value register
    return_value = None
    # list of user-defined classes
    class_list = None

    # map from name of functions to their pc
    function_addresses = {}
    # stack for handling function calls
    call_stack = []

    def __init__(self, irHandler, params):
        super().__init__(irHandler, params)
        self.prg = ProgramContext()
        self.class_list = ClassList()
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
        elif isinstance(stmt, ChironAST.ReadReturnCommand):
            ntgt = self.handleReturnRead(stmt, tgt)

        else:
            raise NotImplementedError(
                "Unknown instruction: %s, %s." % (type(stmt), stmt))

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
        for key, val in params.items():
            var = key.replace(":", "")
            exec("setattr(self.prg,\"%s\",%s)" % (var, val))

    def handleFunctionDeclaration(self, stmt, tgt):
        # mangle the name of private method as _ClassName__methodName
        if "@" in stmt.name and stmt.name.split("@")[1].startswith("__"):
            class_name, method_name = stmt.name.split("@")
            function_name = class_name+ "@" + "_" + class_name.replace(":","") + method_name
        else:
            function_name = stmt.name

        self.function_addresses[function_name + "_" + str(len(stmt.params))] = self.pc + 1 # body of the function starts from next instruction
        return tgt

    def handleFunctionCall(self, stmt, tgt):
        # Handling call stack
        # Save the return address on the call stack
        self.call_stack.append(self.pc + 1)
        # Save the current program context on the call stack
        self.call_stack.append(self.prg)
        # Save the arguments on the call stack
        for arg in stmt.args:
            arg_value = addContext(arg)
            exec(f"self.argument = {arg_value}")
            self.call_stack.append(self.argument)
        # Jump to the function address
        # If the function is a method, the name will be in the form of "caller@method"
        if stmt.caller:
            caller_class = eval(addContext(stmt.caller)).__class__.__name__
            method_name = ":" + str(caller_class) + "@" + str(stmt.name) +  "_" + str(len(stmt.args))
            self.pc = self.function_addresses[method_name]   
        else:
            self.pc = self.function_addresses[stmt.name + "_" + str(len(stmt.args))]
        # Initialize a new program context for the new activation record
        self.prg = ProgramContext()
        return 0

    # Copying the return values in their respective placeholders
    def handleReturnRead(self, stmt, tgt):
        for rval in reversed(stmt.returnValues):
            rval = str(rval).replace(":", "")
            exec(f"self.prg.{rval} = self.call_stack.pop()")
        return 1

    def handleFunctionReturn(self, stmt, tgt):
        # Restore the previous program context
        rval_list = []
        for rval in stmt.returnValues:
            rval_value = addContext(rval)
            exec(f"self.return_value = {rval_value}")
            rval_list.append(self.return_value)
        self.prg = self.call_stack.pop()
        self.pc = self.call_stack.pop()
        self.call_stack.extend(rval_list)
        return 0

    # Copying the parameters in their respective placeholders
    def handleParametersPassing(self, stmt, tgt):
        for param in reversed(stmt.params):
            param = str(param).replace(":", "")
            param_value = self.call_stack.pop()
            setattr(self.prg, param, param_value)
        return 1

    def handleClassDeclaration(self, stmt, tgt):
        className = stmt.className.replace(":", "")
        attributes = stmt.attributes  # List of attribute assignments
        # Handle inheritance if base classes exist
        if hasattr(stmt, "baseClasses") and stmt.baseClasses:
            base_classes = [getattr(self.class_list, str(
                b).replace(":", "")) for b in stmt.baseClasses]
            base_str = ", ".join([b.__name__ for b in base_classes])
            class_header = f"class {className}({base_str}):\n"
        else:
            class_header = f"class {className}:\n"
        class_def = class_header
        init_method = "    def __init__(self"  # Start of __init__
        init_body = "        super().__init__()\n"
        # Handle normal attributes (non-object attributes)
        for attr in attributes:
            attr, target = attr
            attr_name = str(attr.lvar).replace(":", "")
            attr_value = addContext(attr.rexpr) if attr.rexpr else "None"
            init_body += f"        self.{attr_name} = {attr_value}\n"
        # Handle object attributes
        for objectAttr in stmt.objectAttributes:
            objectAttr, target = objectAttr
            lhs = str(objectAttr.target).replace(":", "")
            init_body += f"        self.{lhs} = None\n"
        init_method += "):\n"  # Close the __init__ method signature
        class_def += init_method
        class_def += init_body 
        # Step 1: Execute the class definition (store it inside self.class_list)
        exec(class_def, globals(), self.class_list.__dict__)
        # Step 2: Assign object attributes after class creation
        for objectAttr in stmt.objectAttributes:
            objectAttr, target = objectAttr
            lhs = str(objectAttr.target).replace(":", "")
            rhs = addContext(objectAttr.class_name).replace(
                "self.prg.", "self.class_list.")
            exec(f"self.class_list.{className}.{lhs} = {rhs}()")
        # Inherit methods from base classes 
        inherited_function_addresses = {}
        if stmt.baseClasses:
            for function_name, address in self.function_addresses.items():
                class_name, method_name = function_name.split("@")
                if class_name in reversed(stmt.baseClasses):
                    new_function_name = f"{stmt.className}@{method_name}"
                    inherited_function_addresses[new_function_name] = address
            self.function_addresses.update(inherited_function_addresses)
        return 1

    def handleObjectInstantiation(self, stmt, tgt):
        lhs = str(stmt.target).replace(":", "")
        rhs = addContext(stmt.class_name).replace(
            "self.prg.", "self.class_list.")
        exec(f"self.prg.{lhs} = {rhs}()")
        return 1

    def handleAssignment(self, stmt, tgt):
        print("  Assignment Statement")
        lhs = str(stmt.lvar).replace(":", "")
        rhs = addContext(stmt.rexpr)
        print(lhs, rhs, "Assignment")
        # exec("setattr(self.prg,\"%s\",%s)" % (lhs,rhs))
        exec(f"self.prg.{lhs} = {rhs}")
        return 1

    def handlePrint(self, stmt, tgt):
        print(" PrintCommand")
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
        exec("self.trtl.%s(%s)" % (stmt.direction, addContext(stmt.expr)))
        return 1

    def handleNoOpCommand(self, stmt, tgt):
        print("  No-Op Command")
        return 1

    def handlePen(self, stmt, tgt):
        print("  PenCommand")
        exec("self.trtl.%s()" % (stmt.status))
        return 1

    def handleGotoCommand(self, stmt, tgt):
        print(" GotoCommand")
        xcor = addContext(stmt.xcor)
        ycor = addContext(stmt.ycor)
        exec("self.trtl.goto(%s, %s)" % (xcor, ycor))
        return 1
