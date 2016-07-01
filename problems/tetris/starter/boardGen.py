# boardGen.py
# Script for generating board files
from random import choice
import sys

if len(sys.argv) > 1:
	maxNum = int(sys.argv[1])
else:
	maxNum = 40

piecesList = ['I', 'J', 'L', 'O', 'S', 'Z', 'T']

outputString = ''

for i in range(0, maxNum):
	outputString += choice(piecesList)

print(outputString)
