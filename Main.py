import tkinter
import sys

board = tkinter.Tk()
canvas = tkinter.Canvas(board, width=500, height=500)
canvas.pack()
# Code to add widgets will go here...
board.mainloop()


def create_zones():
    n_agents = int(sys.stdin.readline())

    zones = []


