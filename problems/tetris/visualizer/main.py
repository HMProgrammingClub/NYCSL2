import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/starter/python")

from threading import Thread
from time import sleep

from Tetris import *
from tkinter import *

movesString = None
piecesString = None
frames = []
isRunning = False

def playFrames():
    global frame
    global frames
    global isRunning

    if piecesString is None or movesString is None:
        return

    isRunning = True

    for i in xrange(len(frames)):
        if not isRunning: return
        frame.set(i)
        visualizeFrame()
        sleep(0.5)

    isRunning = False

playThread = Thread(target=playFrames)

def play():
    global playThread
    isRunning = True
    playThread.start()

def generateFrames(piecesString,movesString):
    global frames
    global frameScale
    board = Board(data=piecesString)

    score = 0
    for char in movesString:
        string = str(board)
        score += board.makeMove(char)
        frames.append( (string,score) )

    frameScale.config(to=(len(frames)-1))

def updateFrame(self):
    global isRunning

    isRunning = False
    visualizeFrame()

def visualizeFrame():
    global score
    global canvas
    global frame
    global frames

    if piecesString is None or movesString is None:
        return

    score.set("Score: " + str(frames[frame.get()][1]))

    lines = [s[1:-1] for s in (frames[frame.get()][0].splitlines())[:-1]]

    for y in xrange(len(lines)):
        for x in xrange(len(lines[0])):
            BOX_SIZE = 30
            charToColor = {' ': '#000', 'X': "#0F0", '0': '#FFF'}
            color = charToColor[lines[y][x]]
            canvas.create_polygon(x*BOX_SIZE,y*BOX_SIZE,x*BOX_SIZE+BOX_SIZE,y*BOX_SIZE,x*BOX_SIZE+BOX_SIZE,y*BOX_SIZE+BOX_SIZE,x*BOX_SIZE,y*BOX_SIZE+BOX_SIZE,fill=color)

def loadMovesFile():
    global movesString
    global piecesString
    global status

    filename = filedialog.askopenfilename()
    if not filename.endswith('.txt'):
        messagebox.showinfo("Visualizer error", "Filetype must be a .txt")
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
        messagebox.showinfo("Visualizer error", "Filetype must be a .txt")
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

score = StringVar()
scoreLabel = Label(rightMenu,textvariable=score)
scoreLabel.pack(side=TOP,pady=10)
score.set("Score: 0")

status = StringVar()
statusLabel = Label(rightMenu,textvariable=status)
statusLabel.pack(side=TOP,pady=10)
status.set("Pieces: Not Loaded\nMoves: Not Loaded")

loadPiecesBtn = Button(rightMenu,text="Load Pieces",command=loadPiecesFile)
loadPiecesBtn.pack(side=TOP,pady=10)

loadMovesBtn = Button(rightMenu,text="Load Moves",command=loadMovesFile)
loadMovesBtn.pack(side=TOP,pady=10)

playBtn = Button(rightMenu,command=play,text="Play")
playBtn.pack(side=TOP,pady=10)

bottomMenu = Frame(root)
bottomMenu.pack(side=BOTTOM,padx=10,pady=10)

frame = IntVar()
frameScale = Scale(bottomMenu,variable=frame,command=updateFrame,length=300,orient=HORIZONTAL)
frameScale.pack(side=LEFT)

canvas = Canvas(root,bg="#000",width=300,height=600)
canvas.pack(side=LEFT,padx=10,pady=10)

root.mainloop()
