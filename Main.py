import tkinter
import sys
import time
from threading import Thread

from Agent import Agent
from Emergency import Emergency
from Hospital import Hospital

nAgents = int(sys.stdin.readline()) # =4
zones = []
agents = [None, None, None, None]
hospital_groups = [None, None, None, None]


def create_board():
    board = tkinter.Tk()
    canvas = tkinter.Canvas(board, width=500, height=500)
    canvas.pack()
    board.mainloop()


def setup():
    zones = [[(0,0), (250, 0), (0,250), (250,250)], [(250,0), (500, 0), (250,250), (500,250)], [(0,250), (250, 250), (0,500), (250,500)], [(250,250), (500, 250), (250,500), (500,500)]]
    for i in range(nAgents):
        # Hardcoded, depois podemos mudar
        hospital_groups[i] = [Hospital(None, 100, 10), Hospital(None, 150, 10), Hospital(None, 95, 10)]
        agents[i] = Agent(zones[i], zones, hospital_groups[i], None)

    for i in range(nAgents):
        for group in hospital_groups:
            for j in range(len(group)):
                group[j].set_control_tower(agents[i])


def create_emergency():
    # TODO
    return Emergency(None, None, None, None, None, None, None)


def allocate_emergency(emer):
    emer.get_control_tower().allocate_emergency(emer)


#########################################################################################################

create_board()
setup()

# while True:
#     emergency = create_emergency()
#     time.sleep(3)
#     thread = Thread(target=allocate_emergency, args=(emergency,))
#     thread.start()
#     thread.join()
