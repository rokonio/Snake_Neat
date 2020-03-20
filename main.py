# -*- coding: utf-8 -*-
from tkinter import *
from snake import *

snake = Snake()

fen = Tk()
fen.title("Snake")
fen.resizable(False, False)

can = Canvas(fen,height=400,width=400,bg="red")
can.pack()

can.bind("<Up>",snake.up)
can.bind("<Down>",snake.down)
can.bind("<Right>",snake.right)
can.bind("<Left>",snake.left)
fen.bind("<Escape>",quit)

fen.mainloop()