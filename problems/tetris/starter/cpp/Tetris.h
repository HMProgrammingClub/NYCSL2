#include <queue>
#include <string>
#include <iostream>
#include <fstream>
#include <math.h>
#include <array>
#include <exception>

const std::array<bool,20> falseX20 = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
const std::array< std::array<bool, 20>, 10> nullarray = { falseX20, falseX20, falseX20, falseX20, falseX20, falseX20, falseX20, falseX20, falseX20, falseX20};

class Piece {
public:
    // The location of the origin (top left) of the matrix representing the peice.
    int x, y;

    // The rotation, from 0-3 going clockwise from the starting position.
    int rotation;

    // The matrix representing the piece in its current orientation.
    // This matrix can be a different size depending on the piece.
    std::vector< std::vector<bool> > matrix;

    // The keycode of the piece.
    char type;

    // Construct a piece from the key, aka IJLOSTZ.
    Piece(char key) {
        type = key;
        switch (key) {
            case 'I': matrix = {
                { false, false, false, false },
                { true,  true,  true,  true },
                { false, false, false, false },
                { false, false, false, false }
            };
                      break;
            case 'J': matrix = {
                { true,  false, false },
                { true,  true,  true  },
                { false, false, false },
            };
                      break;
            case 'L': matrix = {
                { false, false, true  },
                { true,  true,  true  },
                { false, false, false },
            };
                      break;
            case 'O': matrix = {
                { true, true },
                { true, true }
            };
                      break;
            case 'S': matrix = {
                { false, true,  true  },
                { true,  true,  false },
                { false, false, false },
            };
                      break;
            case 'Z': matrix = {
                { true,  true,  false },
                { false, true,  true  },
                { false, false, false },
            };
                      break;
            case 'T': matrix = {
                { false, true,  false },
                { true,  true,  true  },
                { false, false, false }
            };
                      break;
            case '0': matrix = {{}};
                      break;
            default : throw std::runtime_error("Invalid piece initialization character.");
        } rotation = x = y = 0; // intialize piece to orientation 0 at top left
    }

    // Rotate the piece 90 degrees clockwise.
    void rotate() {
        std::vector< std::vector<bool> > ret;
        for (int x=0; x<ret.size(); x++) for (int y=0; y<ret.size(); y++) {
            ret[y][ret.size()-1-x] = matrix[x][y];
        } matrix = ret; rotation += 1;
        if (rotation > 3) rotation -= 4;
    }

    // Set the piece to a specified orientation, 0-3 inclusive going clockwise from start.
    void setRotation(int rotation) {
        if (rotation < 0 || rotation > 3)
            throw new std::runtime_error("Rotation must be between 0 and 3 inclusive.");
        while (rotation != this->rotation) rotate();
    }

    friend std::ostream &operator<<(std::ostream &output, const Piece & P) {
        std::string finalString;
        for (auto row : P.matrix) {
            for (bool is : row) finalString += is?'X':'O';
            finalString += '\n';
        }
        output << finalString;
        return output;
    }
};

class Board {
    public:
        // Constant for board width and height
        static const int BOARD_WIDTH = 10;
        static const int BOARD_HEIGHT = 20;

        // The 10x20 matrix of occupied spaces on the board, made up of settled pieces.
        // bool settled[BOARD_WIDTH][BOARD_HEIGHT];
        std::array< std::array<bool, BOARD_HEIGHT>, BOARD_WIDTH> settled;

        // The piece currently being manipulated, not yet settled.
        Piece moving = Piece('0');

        // The queue of pieces waiting to be put into loading.
        std::queue<Piece> queue;

        // The character list (or string) representing the moves made throughout
        // the game.  This string (when written to a file) is what is graded by
        // the NYCSL website for scoring.
        std::string moves;

        // Initialize the game board from "input.txt" file.
        Board() {
            Board("input.txt");
        }


        // Initialize the game board from a filename.
        Board(std::string filename) {
            std::string piecesString;
            std::ifstream boardFile;
            boardFile.open(filename);
            if(boardFile.is_open()) {
                getline(boardFile,piecesString);
                    boardFile.close();
                }
            else {
                throw "Unable to open file";
            }
            // deserialize input string and load into queue
            for (char c : piecesString) {
                if (c != '\0' && c != '\n') {
                    queue.push(Piece(c));
                }
            }
        }

        // Perform a move on the current piece, stepping forwards a turn in time. A
        // move can either be ' ' for no move, 'L' for left shift, 'R' for right shift,
        // or 'X' for rotate clockwise.
        // The method will return the points earned in the move.
        int makeMove(char moveKey) {
            if (moving.type == '0') {
                if (queue.empty()) {
                    throw std::runtime_error("Used all the pieces");
                }
                moving = queue.front();
                queue.pop();
            }

            moves += moveKey;

            switch(moveKey) {
                case 'L': moving.x -= 1;
                          break;
                case 'R': moving.x += 1;
                          break;
                case 'X': moving.rotate();
                          break;
                case ' ': break;
                default : throw std::runtime_error("Invalid move character.");
            } if (checkOutOfBounds(moving)) throw  std::runtime_error("Piece went out of bounds.");
            if (superimpose(moving, settled) == nullarray) throw std::runtime_error("Piece collided with another piece.");

            moving.y += 1;

            bool hitBottom = false;
            for (int r=moving.y+moving.matrix.size()-BOARD_HEIGHT-1; r>=0; r--) {
                for (int i=0; i<moving.matrix.size(); i++) {
                    if (moving.matrix[moving.matrix.size()-r-1][i]) hitBottom = true;
                }
            }

            if (superimpose(moving,settled) == nullarray || hitBottom) { // if piece has landed
                moving.y -= 1;
                settled = superimpose(moving,settled);
                moving = Piece('0');
            }

            return tetris();
        }

        // Attempt to superimpose the piece on the given map. Return null
        // if they overlap, otherwise return the new map.
        static std::array< std::array<bool, BOARD_HEIGHT>, BOARD_WIDTH> superimpose(Piece piece, std::array< std::array<bool, BOARD_HEIGHT>, BOARD_WIDTH> map) {
            std::array< std::array<bool, BOARD_HEIGHT>, BOARD_WIDTH> newMap = map;
            for (int c=piece.x; c<piece.x+piece.matrix.size(); c++) {
                for (int r=piece.y; r<piece.y+piece.matrix.size(); r++) {
                    if (c >= 0 && c < BOARD_WIDTH && r >=0 && r < BOARD_HEIGHT) {
                        if (map[r][c] && piece.matrix[r-piece.y][c-piece.x]) return /* how do i express this */ nullarray;
                        else newMap[r][c] |= piece.matrix[r-piece.y][c-piece.x];
                    }
                }
            } return newMap;
        }

        // Return whether the piece is out of bounds.
        static bool checkOutOfBounds(Piece piece) {
            for (int c=0; c<-piece.x; c++) {
                for (int i=0; i<piece.matrix.size(); i++) {
                    if (piece.matrix[i][c]) return true;
                }
            } for (int c=piece.x+piece.matrix.size()-BOARD_WIDTH; c>0; c--) {
                for (int i=0; i<piece.matrix.size(); i++) {
                    if (piece.matrix[i][c]) return true;
                }
            } return false;
        }

        // Output the taken moves to a text file with the given file name, ex: output.txt.
        void outputMovesToFile(std::string filename) {
            std::ofstream ofile (filename, std::ios::out);
            if(ofile.is_open()) {
                ofile << moves;
                ofile.close();
            }
        }

        // Render the board as ASCII art, where Os represent settled blocks
        // and Xs represent blocks in active pieces. Good for printing and
        // debugging.
        friend std::ostream &operator<<(std::ostream &output, Board & B) {
            if (B.moving.type == '0') B.moving = B.queue.front();
            B.queue.pop();
            char newMap[BOARD_WIDTH][BOARD_HEIGHT];
            for (int r=0; r< BOARD_WIDTH; r++) for (int c=0; c<BOARD_HEIGHT; c++)
                newMap[r][c] = B.settled[r][c]?'O':' ';
            for (int c=B.moving.x; c<B.moving.x+B.moving.matrix.size(); c++) {
                for (int r=B.moving.y; r<B.moving.y+B.moving.matrix.size(); r++) {
                    if (c >= 0 && c < BOARD_WIDTH && r >=0 && r < BOARD_HEIGHT) {
                        if (!B.settled[r][c] && B.moving.matrix[r-B.moving.y][c-B.moving.x]) newMap[r][c] = 'X';
                    }
                }
            }

            std::string finalString;
            for (int j = 0; j < BOARD_WIDTH; j++) {
                finalString += '|';
                for (int i = 0; i < BOARD_HEIGHT; i++) finalString += newMap[j][i];
                finalString += '|';
                finalString += '\n';
            } for (int i=0; i<BOARD_WIDTH+2; i++) finalString += '-';
            output << finalString;
            return output;
        }

    private:
        // Check the board for complete lines, return score earned.
        // This will also shift the board down if lines have been deleted.
        int tetris() {
            int lines = 0;
            for (int r = BOARD_WIDTH-1; r>=0; r--) {
                bool filled = true;
                for (bool block : settled[r]) filled &= block;
                if (filled) {
                    for (int i=r; i>0; i--) settled[r] = settled[r-1];
                    lines += 1; r += 1;
                }
            } return round((float)pow(1.189207115f,lines)*100*lines);
        }
};
