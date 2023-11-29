# Abstract Class.
class ChironHooks:
    params = None

    def __init__(self):
        pass

    def ChironStartHook(self, interpreterObj):
        pass

    def ChironEndHook(self, interpreterObj):
        pass


class ConcreteChironHooks(ChironHooks):

    def __init__(self):
        # rest of the initialization code.
        pass

    # Override
    def ChironStartHook(self, interpreterObj):
        # What happens when interpreter starts.
        print(f"\n\n[Chiron] Interpreter is starting, PC ->{interpreterObj.pc}.\n\n")

    # Override
    def ChironEndHook(self, interpreterObj):
        # What happens when interpreter ends. 
        print(f"\n\n[Chiron] Interpreter is ending, PC -> {interpreterObj.pc}.\n\n")
