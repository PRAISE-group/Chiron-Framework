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
        print("\n\n[Chiron] Interpreter is starting\n\n")

    # Override
    def ChironEndHook(self, interpreterObj):
        # What happens when interpreter ends. 
        print("\n\n[Chiron] Interpreter is ending\n\n")
