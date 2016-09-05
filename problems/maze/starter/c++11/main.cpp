#include <time.h> //Needed to get the time so that we can seed our random number generator.
#include "maze.hpp" //Contains the core maze utils, such as consts, typedefs, and the >> overload.

int main() {
    srand(time(NULL)); //Seeds random number generator with the time so that output is always different.
    Maze m;
    while(true) {
        std::cin >> m; //Gets the present maze.
        std::cout << rand() % 4; //Sends a random direction back. Directions are ints as defined in maze.hpp
    }
}
