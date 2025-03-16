#include "CTurtle.hpp"

cturtle::TurtleScreen scr;
cturtle::Turtle turtle(scr);

extern "C" __attribute__((used)) void init() {
    turtle.speed(cturtle::TS_SLOWEST);
    turtle.pencolor({"blue"});
}

extern "C" __attribute__((used)) void handleGoTo(int x, int y) {
    turtle.goTo(x, y);
}

extern "C" __attribute__((used)) void handleForward(int x) {
    turtle.forward(x);
}

extern "C" __attribute__((used)) void handleBackward(int x) {
    turtle.backward(x);
}

extern "C" __attribute__((used)) void handleRight(int x) {
    turtle.right(x);
}

extern "C" __attribute__((used)) void handleLeft(int x) {
    turtle.left(x);
}

extern "C" __attribute__((used)) void handlePenUp() {
    turtle.penup();
}

extern "C" __attribute__((used)) void handlePenDown() {
    turtle.pendown();
}

extern "C" __attribute__((used)) void finish() {
    scr.exitonclick();
}