public class Piece {
    // The top left of the matrix representing the peice.
    public int originX, originY;

    // The rotation, from 0-3 going clockwise from the starting position.
    public int rotation;

    // The matrix representing the piece in its current orientation.
    // This matrix can be a different size depending on the piece.
    boolean[][] pieceMatrix;

    // Construct a piece from the key, aka IJLOSTZ.
    public Piece(char key) {

    }

    // Rotate the piece 90 degrees clockwise.
    public void rotate() {

    }

    // Set the piece to a specified orientation, 0-3.
    public void setRotation(int _rotation) {

    }

    // Templates for pieces IJLOSTZ in their starting orientations.
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
}
