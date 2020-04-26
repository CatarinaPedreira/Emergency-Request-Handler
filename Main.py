import tkinter
import sys

from AASMAProj.Agent import Agent
from AASMAProj.Hospital import Hospital

nAgents = int(sys.stdin.readline())


def create_board():
    board = tkinter.Tk()
    canvas = tkinter.Canvas(board, width=500, height=500)
    canvas.pack()
    board.mainloop()


def setup():
    n_agents = int(sys.stdin.readline())
    zones = []
    agents = []
    hospitals = []

    for i in range(nAgents):
        zones[i] = [(), (), (), ()] # todo fill this in
        hospitals[i] = Hospital(None, 100, 10)
        #temos de ter 2 fors e criar os agentes no for a seguir, porque senao os hospitais nao vao estar cheios para cada agente

