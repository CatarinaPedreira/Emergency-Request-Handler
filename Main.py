import tkinter
import sys
import time
from threading import Thread

from AASMAProj.Agent import Agent
from AASMAProj.Emergency import Emergency
from AASMAProj.Hospital import Hospital

nAgents = int(sys.stdin.readline())
zones = []
agents = []
hospital_groups = []


def create_board():
    board = tkinter.Tk()
    canvas = tkinter.Canvas(board, width=500, height=500)
    canvas.pack()
    board.mainloop()


def setup():
    for i in range(nAgents):
        # Hardcoded, depois podemos mudar
        hospital_groups[i] = [Hospital(None, 100, 10), Hospital(None, 150, 10), Hospital(None, 95, 10)]
        zones[i] = [(), (), (), ()]  # todo fill this in
        agents[i] = Agent(zones[i], zones, hospital_groups[i], None)
        for group in hospital_groups:
            for j in range(len(group)):
                group[j].set_control_tower(agents[i])


def create_emergency():
    # TODO, create emergency in random coordinates (x,y)
    return Emergency(None, None, None, None, None, None, None)


def allocate_emergency(emer):
    emer.get_control_tower().allocate_emergency(emer)


#######################################################################################################################

create_board()
setup()

# while True:
#     emergency = create_emergency()
#     time.sleep(3)
#     thread = Thread(target=allocate_emergency, args=(emergency,))
#     thread.start()
#     thread.join()
