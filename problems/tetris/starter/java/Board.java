import java.util.LinkedList;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;

public class Board {
    // Constants for board width and height
    public static final int BOARD_WIDTH = 10;
    public static final int BOARD_HEIGHT = 10;

    // The 10x20 matrix of occupied spaces on the board, made up of settled pieces.
    public boolean[][] settled;

    // The piece currently being manipulated, not yet settled.
    public Piece moving;

    // The queue of pieces waiting to be put into loading.
    public LinkedList<Piece> queue;

    // The character list (or string) representing the moves made throughout
    // the game.  This string (when written to a file) is what is graded by
    // the NYCSL website for scoring.
    public String moves;

    // Initialize the game board from "input.txt" file.
    public Board() throws IOException {
        this(new File("input.txt"));
    }

    // Initialize the game board from a FileReader object.
    public Board(File file) throws IOException {
        this(new Scanner(file).nextLine());
    }

    // Initialize the game board from a string of pieces.
    public Board(String piecesString) {
        moves = new String();
        queue = new LinkedList<Piece>();
        settled = new boolean[BOARD_HEIGHT][BOARD_WIDTH];

        // deserialize input string and load into queue
        for (char c : piecesString.toCharArray()) queue.add(new Piece(c));
    }

    // Perform a move on the current piece, stepping forwards a turn in time. A
    // move can either be ' ' for no move, 'L' for left shift, 'R' for right shift,
    // or 'X' for rotate clockwise.
    // The method will return the points earned in the move.
    public int makeMove(char moveKey) {
        if (moving == null) moving = queue.remove();
        moves += moveKey;

        switch(moveKey) {
            case 'L': moving.x -= 1;
                      break;
            case 'R': moving.x += 1;
                      break;
            case 'X': moving.rotate();
                      break;
            case ' ': break;
            default : throw new RuntimeException("Invalid move character.");
        } if (checkOutOfBounds(moving)) throw new RuntimeException("Piece went out of bounds.");
        if (superimpose(moving,settled) == null) throw new RuntimeException("Piece collided with another piece.");

        moving.y += 1;

        boolean hitBottom = false;
        for (int r=moving.y+moving.matrix.length-BOARD_HEIGHT-1; r>=0; r--) {
            for (int i=0; i<moving.matrix.length; i++) {
                if (moving.matrix[moving.matrix.length-r-1][i]) hitBottom = true;
            }
        }

        if (superimpose(moving,settled) == null || hitBottom) { // if piece has landed
            moving.y -= 1;
            settled = superimpose(moving,settled);
            moving = null;
        }

        return tetris();
    }

    // Attempt to superimpose the piece on the given map. Return null
    // if they overlap, otherwise return the new map.
    private static boolean[][] superimpose(Piece piece, boolean[][] map) {
        boolean[][] newMap = new boolean[map.length][map[0].length];
        for (int i=0; i<map.length; i++) newMap[i] = map[i].clone();
        for (int c=piece.x; c<piece.x+piece.matrix.length; c++) {
            for (int r=piece.y; r<piece.y+piece.matrix.length; r++) {
                if (c >= 0 && c < BOARD_WIDTH && r >=0 && r < BOARD_HEIGHT) {
                    if (map[r][c] && piece.matrix[r-piece.y][c-piece.x]) return null;
                    else newMap[r][c] |= piece.matrix[r-piece.y][c-piece.x];
                }
            }
        } return newMap;
    }

    // Return whether the piece is out of bounds.
    private static boolean checkOutOfBounds(Piece piece) {
        for (int c=0; c<-piece.x; c++) {
            for (int i=0; i<piece.matrix.length; i++) {
                if (piece.matrix[i][c]) return true;
            }
        } for (int c=piece.x+piece.matrix.length-BOARD_WIDTH; c>0; c--) {
            for (int i=0; i<piece.matrix.length; i++) {
                if (piece.matrix[i][c]) return true;
            }
        } return false;
    }

    // Check the board for complete lines, return score earned.
    // This will also shift the board down if lines have been deleted.
    private int tetris() {
        int lines = 0;
        for (int r=settled.length-1; r>=0; r--) {
            boolean filled = true;
            for (boolean block : settled[r]) filled &= block;
            if (filled) {
                for (int i=r; i>0; i--) settled[r] = settled[r-1].clone();
                lines += 1; r += 1;
            }
        } return Math.round((float)Math.pow(1.189207115f,lines)*100*lines);
    }

    // Render the board as ASCII art, where Os represent settled blocks
    // and Xs represent blocks in active pieces. Good for printing and
    // debugging.
    public String toString() {
        if (moving == null) moving = queue.remove();
        char[][] newMap = new char[settled.length][settled[0].length];
        for (int r=0; r<settled.length; r++) for (int c=0; c<settled[0].length; c++)
            newMap[r][c] = settled[r][c]?'O':' ';
        for (int c=moving.x; c<moving.x+moving.matrix.length; c++) {
            for (int r=moving.y; r<moving.y+moving.matrix.length; r++) {
                if (c >= 0 && c < BOARD_WIDTH && r >=0 && r < BOARD_HEIGHT) {
                    if (!settled[r][c] && moving.matrix[r-moving.y][c-moving.x]) newMap[r][c] = 'X';
                }
            }
        }

        StringBuilder builder = new StringBuilder();
        for (char[] row : newMap) {
            builder.append('|');
            for (char i : row) builder.append(i);
            builder.append('|');
            builder.append('\n');
        } for (int i=0; i<BOARD_WIDTH+2; i++) builder.append('-');
        return builder.toString();
    }
}
