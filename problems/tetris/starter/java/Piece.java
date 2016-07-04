public class Piece {
    // The location of the origin (top left) of the matrix representing the peice.
    public int x, y;

    // The rotation, from 0-3 going clockwise from the starting position.
    public int rotation;

    // The matrix representing the piece in its current orientation.
    // This matrix can be a different size depending on the piece.
    public boolean[][] matrix;

    // The keycode of the piece.
    public char type;

    // Construct a piece from the key, aka IJLOSTZ.
    public Piece(char key) {
        type = key;
        switch (key) {
            case 'I': matrix = PIECES.I;
                      break;
            case 'J': matrix = PIECES.J;
                      break;
            case 'L': matrix = PIECES.L;
                      break;
            case 'O': matrix = PIECES.O;
                      break;
            case 'S': matrix = PIECES.S;
                      break;
            case 'Z': matrix = PIECES.Z;
                      break;
            case 'T': matrix = PIECES.T;
                      break;
            default : throw new RuntimeException("Invalid piece initialization character.");
        } rotation = x = y = 0; // intialize piece to orientation 0 at top left
    }

    // Rotate the piece 90 degrees clockwise.
    public void rotate() {
        final boolean[][] ret = new boolean[matrix.length][matrix.length];
        for (int x=0; x<ret.length; x++) for (int y=0; y<ret.length; y++) {
            ret[y][ret.length-1-x] = matrix[x][y];
        } matrix = ret; rotation += 1;
        if (rotation > 3) rotation -= 4;
    }

    // Set the piece to a specified orientation, 0-3 inclusive going clockwise from start.
    public void setRotation(int rotation) {
        if (rotation < 0 || rotation > 3)
            throw new RuntimeException("Rotation must be between 0 and 3 inclusive.");
        while (rotation != this.rotation) rotate();
    }

    // Templates for pieces IJLOSZT in their starting orientations.
    public static class PIECES {
        public static final boolean[][] I = {
            { false, false, false, false },
            { true,  true,  true,  true },
            { false, false, false, false },
            { false, false, false, false }
        };

        public static final boolean[][] J = {
            { true,  false, false },
            { true,  true,  true  },
            { false, false, false },
        };

        public static final boolean[][] L = {
            { false, false, true  },
            { true,  true,  true  },
            { false, false, false },
        };

        public static final boolean[][] O = {
            { true, true },
            { true, true }
        };

        public static final boolean[][] S = {
            { false, true,  true  },
            { true,  true,  false },
            { false, false, false },
        };

        public static final boolean[][] Z = {
            { true,  true,  false },
            { false, true,  true  },
            { false, false, false },
        };

        public static final boolean[][] T = {
            { false, true,  false },
            { true,  true,  true  },
            { false, false, false }
        };
    }

    public String toString() {
        StringBuilder builder = new StringBuilder();
        for (boolean[] row : matrix) {
            for (boolean is : row) builder.append(is?'X':'O');
            builder.append('\n');
        } return builder.toString();
    }
}
