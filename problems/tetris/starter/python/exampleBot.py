import Tetris
from random import choice

possibleMoves = [' ', 'L', 'R', 'X']

# A simple example bot that moves randomly
filename = input('Board filename: ')
B = Tetris.Board(filename)
try:
	while True:
		B.makeMove(choice(possibleMoves))
except Exception as e:
	pass
B.outputMovesToFile('output.txt')
print('Output moves to output.txt')
