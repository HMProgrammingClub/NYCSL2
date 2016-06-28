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


x = Board()
print x.queue[0]
