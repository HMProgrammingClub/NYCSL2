import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/starter/python")

from Tetris import *
from Tkinter import *

root = Tk()
root.title("NYCSL Tetris Visualizer")
frame = Frame(root)
frame.pack()

rightMenu = Frame(root)
rightMenu.pack(side=RIGHT,padx=10,pady=10)

loadPiecesBtn = Button(rightMenu,text="Load Pieces")
loadPiecesBtn.pack(side=TOP,pady=10)

loadMovesBtn = Button(rightMenu,text="Load Moves")
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
