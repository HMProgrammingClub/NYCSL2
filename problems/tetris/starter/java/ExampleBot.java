import java.util.Random;
import java.io.IOException;


public class ExampleBot {
	public static final char[] possibleMoves = {'X', 'L', 'R', ' '};

	public static void main(String[] args) {
		try {
			Board B = new Board();
			Random generator = new Random();
			int index;
			try {
				while (true) {
					index = generator.nextInt(possibleMoves.length);
					B.makeMove(possibleMoves[index]);
				}
			} catch (RuntimeException e) {
				System.out.println(e);
			}
			B.outputMovesToFile("output.txt");
			System.out.println("Output moves to 'output.txt'");
		} catch (IOException e) {
			System.out.println("Could not find input file input.txt");
		}
	}
}
