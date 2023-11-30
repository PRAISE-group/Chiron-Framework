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
        #print(f"\n\n[Chiron] Interpreter is starting, PC ->{interpreterObj.trtl.pos()}.\n\n")
        #print(f"\n\n[Chiron] Interpreter is starting, PC ->{interpreterObj.trtl.speed()}.\n\n")

        tur = interpreterObj.trtl
        tur.hideturtle()
        tur.speed(100)
        curr_color = tur.color()
        tur.color(curr_color[0],'yellow')
        tur.begin_fill()
        tur.penup()
        tur.goto(250, 200)
        tur.pendown()
        tur.goto(250, 300)
        tur.goto(300, 350)
        tur.goto(350, 300)
        tur.goto(350, 200)
        tur.goto(250, 200)
        tur.end_fill()
        tur.penup()

        tur.goto(170,200)
        tur.write("(250, 200)",font=("Verdana", 10, "bold"))
        tur.goto(170,300)
        tur.write("(250, 300)",font=("Verdana", 10, "bold"))
        tur.goto(270,360)
        tur.write("(300, 350)",font=("Verdana", 10, "bold"))
        tur.goto(370,300)
        tur.write("(350, 300)",font=("Verdana", 10, "bold"))
        tur.goto(370,200)
        tur.write("(350, 200)",font=("Verdana", 10, "bold"))
        tur.goto(260, 175)
        tur.write("Kachuapur",font=("Arial", 10, "bold"))

        tur.goto(0,0)
        tur.pendown()
        tur.speed(1)
        tur.color(*curr_color)
        tur.showturtle()

    # Override
    def ChironEndHook(self, interpreterObj):
        # What happens when interpreter ends. 
        #print(f"\n\n[Chiron] Interpreter is ending, PC -> {interpreterObj.trtl.pos()}.\n\n")
        pos = interpreterObj.trtl.pos()
        x = pos[0]
        y = pos[1]
        if (100 * x - 35000 <= 0):
            if (100 * y - 20000 >= 0):
                if (-100 * x + 25000 <= 0):
                    if (50 * x - 50 * y + 2500>=0):
                        if (50 * x + 50 * y - 32500 <= 0):
                            interpreterObj.t_screen.bgpic('./ChironHooks/tenor.gif')
                            
