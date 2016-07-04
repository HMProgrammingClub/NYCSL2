#include <iostream>
#include <stdlib.h>
#include <time.h>
#include "Tetris.h"

// A simple example bot which randomly chooses a move.

int main ()
{
    srand ( time(NULL) ); //initialize the random seed
    Board B("input.txt");

    const char possibleMoves[4] = {'L', 'R', 'X', ' '};
    int RandIndex;
    try {
        while (true) {
            RandIndex = rand() % 4;
            B.makeMove(possibleMoves[RandIndex]);
        }
    } catch (std::runtime_error e) {
        std::cout << "Error: " << e.what() << std::endl;
    }

    B.outputMovesToFile("output.txt");
    std::cout << "Output moves to file 'output.txt'" << std::endl;
    return 0;
}
