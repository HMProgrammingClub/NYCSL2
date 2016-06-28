import copy

class Piece:
    def __init__(self, key):
        # The location of the origin (top left) of the matrix representing the peice.
        self.x = 0
        self.y = 0

        # The rotation, from 0-3 going clockwise from the starting position.
        self.rotation = 0

        if key in {'I', 'J', 'L', 'O', 'S', 'Z', 'T'}:
            self.matrix = copy.deepcopy(getattr(self,key))
            self.type = key
        else:
            raise RuntimeError('Invalid piece initialization character.')

    # Rotate the piece 90 degrees clockwise.
    def rotate(self):
        ret = copy.deepcopy(self.matrix)
        for x in range(0,len(ret)):
            for y in range (0,len(ret)):
                ret[y][len(ret)-1-x] = self.matrix[x][y];
        self.matrix = ret
        self.rotation += 1
        if self.rotation > 3: self.rotation -= 4

    # Set the piece to a specified orientation, 0-3 inclusive going clockwise from start.
    def setRotation(self, rotation):
        if self.rotation < 0 or self.rotation > 3:
            raise RuntimeError('Rotation must be between 0 and 3 inclusive')
        while self.rotation != rotation:
            self.rotate()


    # Templates for pieces IJLOSZT in their starting orientations.
    I = [[ False, False, False, False ],
         [ True,  True,  True,  True ],
         [ False, False, False, False ],
         [ False, False, False, False ]
    ]

    J = [[ True,  False, False ],
         [ True,  True,  True  ],
         [ False, False, False ],
    ]

    L = [[ False, False, True  ],
         [ True,  True,  True  ],
         [ False, False, False ],
    ]

    O = [[ True, True ],
         [ True, True ]
    ]

    S = [[ False, True,  True  ],
         [ True,  True,  False ],
         [ False, False, False ],
    ]

    Z = [[ True,  True,  False ],
         [ False, True,  True  ],
         [ False, False, False ],
    ]

    T = [[ False, True,  False ],
         [ True,  True,  True  ],
         [ False, False, False ]
    ]

    def __str__(self):
        outstring = ''
        for row in self.matrix:
            for val in row:
                outstring += 'X' if val else 'O'
            outstring += '\n'
        return outstring


class Board:
    # Constants for board width and height
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    def __init__(self, filename='input.txt'):
        # The 10x20 matrix of occupied spaces on the board, made up of settled pieces.
        self.settled = [[False for x in range(self.BOARD_WIDTH)] for y in range(self.BOARD_HEIGHT)]

        # The piece currently being manipulated, not yet settled.
        self.moving = None

        # The queue of pieces waiting to be put into loading.
        self.queue = []

        # The character list (or string) representing the moves made throughout
        # the game.  This string (when written to a file) is what is graded by
        # the NYCSL website for scoring.
        self.moves = ''

        with open(filename, 'r') as infile:
            data = infile.read().replace('\n', '')

        for char in data:
            self.queue.append(Piece(char))

    # Perform a move on the current piece, stepping forwards a turn in time. A
    # move can either be ' ' for no move, 'L' for left shift, 'R' for right shift,
    # or 'X' for rotate clockwise.
    # The method will return the points earned in the move.
    def makeMove(self, moveKey):
        if self.moving == None: self.moving = self.queue.pop(0)
        self.moves += moveKey

        if moveKey == 'L':
            self.moving.x -= 1
        elif moveKey == 'R':
            self.moving.x += 1
        elif moveKey == 'X':
            self.moving.rotate()
        elif moveKey == ' ':
            pass
        else: raise RuntimeError('Invalid move character.')

        if self.checkOutOfBounds(self.moving):
            raise RuntimeError('Piece went out of bounds.')
        if self.superimpose(self.moving,self.settled) == None:
            raise RuntimeError('Piece collided with another piece.')

        self.moving.y += 1

        hitBottom = False
        for r in sorted(range(self.moving.y+len(self.moving.matrix)-self.BOARD_HEIGHT),reverse=True):
            for i in range(len(self.moving.matrix)):
                if self.moving.matrix[len(self.moving.matrix)-r-1][i]: hitBottom = True

        if self.superimpose(self.moving,self.settled) == None or hitBottom:
            self.moving.y -= 1
            self.settled = self.superimpose(self.moving,self.settled)
            self.moving = None

        return self.__tetris()

    def checkOutOfBounds(self,piece):
        for c in range(-piece.x):
            for i in range(len(piece.matrix)):
                if (piece.matrix[i][c]): return True

        for c in range(piece.x+piece.matrix.length-self.BOARD_WIDTH,0,-1):
            for i in range(len(piece.matrix)):
                if (piece.matrix[i][c]): return True

        return False

    def superimpose(self,piece,map):
        newMap = copy.deepcopy(map)
        for c in range(piece.x,piece.x+len(piece.matrix)):
            for r in range(piece.y,piece.y+len(piece.matrix)):
                if c>=0 and c<self.BOARD_WIDTH and r>=0 and r<self.BOARD_HEIGHT:
                    if map[r][c] and piece.matrix[r-piece.y][c-piece.x]: return None
                    else: newMap[r][c] |= piece.matrix[r-piece.y][c-piece.x]
        return newMap

    def __tetris(self):
        lines = 0
        r = len(self.settled)-1
        while r >= 0:
            filled = True
            for block in self.settled[r]: filled &= block
            if filled:
                for i in range(r,0,-1): self.settled[r] = copy.copy(self.settled[r-1])
                lines += 1
                r += 1
            r -= 1
        return round(1.189207115**lines * 100 * lines)

    def ouputMovesToFile(self, filename='output.txt'):
        with open(filename, "w") as out:
            out.write(self.moves)

    def __str__(self):
        if self.moving == None: self.moving = self.queue.pop(0)
        newMap = [[' ' for x in range(self.BOARD_WIDTH)] for y in range(self.BOARD_HEIGHT)]
        for r in range(self.BOARD_HEIGHT):
            for c in range(self.BOARD_WIDTH):
                if self.settled[r][c]: newMap[r][c] = 'O'
        for c in range(self.moving.x,self.moving.x+len(self.moving.matrix)):
            for r in range(self.moving.y,self.moving.y+len(self.moving.matrix)):
                if c >= 0 and c < self.BOARD_WIDTH and r >=0 and r < self.BOARD_HEIGHT:
                    if not self.settled[r][c] and self.moving.matrix[r-self.moving.y][c-self.moving.x]:
                        newMap[r][c] = 'X'

        builder = ''
        for row in newMap:
            builder += '|'
            for i in row: builder += i
            builder += '|\n'
        for i in range(self.BOARD_WIDTH+2): builder += '-'
        return builder
