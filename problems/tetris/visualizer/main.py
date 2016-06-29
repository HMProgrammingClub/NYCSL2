import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/starter/python")

from Tetris import *
from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox

movesString = None
piecesString = None
frames = []

def generateFrames(piecesString,movesString):
    board = Board(data=piecesString)

    for char in movesString:
        string = str(board)
        points = board.makeMove(char)
        frames.append( (string,points) )

def loadMovesFile():
    global movesString
    global piecesString
    global status

    filename = askopenfilename()
    if not filename.endswith('.txt'):
        tkMessageBox.showinfo("Visualizer error", "Filetype must be a .txt")
    else:
        with open(filename, 'r') as infile:
            movesString = infile.read().replace('\n', '')
        if piecesString is not None and movesString is not None:
            status.set("Pieces: Loaded\nMoves: Loaded")
            generateFrames(piecesString,movesString)
        elif piecesString is None:
            status.set("Pieces: Not Loaded\nMoves: Loaded")


def loadPiecesFile():
    global movesString
    global piecesString
    global status

    filename = askopenfilename()
    if not filename.endswith('.txt'):
        tkMessageBox.showinfo("Visualizer error", "Filetype must be a .txt")
    else:
        with open(filename, 'r') as infile:
            piecesString = infile.read().replace('\n', '')
        if piecesString is not None and movesString is not None:
            status.set("Pieces: Loaded\nMoves: Loaded")
            generateFrames(piecesString,movesString)
        elif movesString is None:
            status.set("Pieces: Loaded\nMoves: Not Loaded")

root = Tk()
root.title("NYCSL Tetris Visualizer")
root.resizable(0,0)

frame = Frame(root)
frame.pack()

rightMenu = Frame(root)
rightMenu.pack(side=RIGHT,padx=10,pady=10)

scoreLabel = Label(rightMenu,text="Score: 500")
scoreLabel.pack(side=TOP,pady=10)

status = StringVar()
statusLabel = Label(rightMenu,textvariable=status)
statusLabel.pack(side=TOP,pady=10)
status.set("Pieces: Not Loaded\nMoves: Not Loaded")

loadPiecesBtn = Button(rightMenu,text="Load Pieces",command=loadPiecesFile)
loadPiecesBtn.pack(side=TOP,pady=10)

loadMovesBtn = Button(rightMenu,text="Load Moves",command=loadMovesFile)
loadMovesBtn.pack(side=TOP,pady=10)

playBtn = Button(rightMenu,text="Play")
playBtn.pack(side=TOP,pady=10)

bottomMenu = Frame(root)
bottomMenu.pack(side=BOTTOM,padx=10,pady=10)

frameScale = Scale(bottomMenu,length=300, orient=HORIZONTAL)
frameScale.pack(side=LEFT)

canvas = Canvas(root,bg="#000",width=300,height=600)
canvas.pack(side=LEFT,padx=10,pady=10)

root.mainloop()
