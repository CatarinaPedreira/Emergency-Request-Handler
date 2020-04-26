import tkinter
import sys
import time
from threading import Thread

from AASMAProj.Agent import Agent
from AASMAProj.Emergency import Emergency
from AASMAProj.Hospital import Hospital
from AASMAProj.MedicalVehicle import MedicalVehicle

zones = []
agents = []
hospital_groups = []


def create_board():
    board = tkinter.Tk()
    canvas = tkinter.Canvas(board, width=500, height=500)
    #TODO create four shapes for agents, hospitals around them, lines to differentiate zones maybe?
    # Check how to draw cool baby ambulances
    canvas.pack()
    board.mainloop()


def setup():

    # Check again if points are correct, im sleepy
    zones[0] = [(0,0), (250,0), (250,250), (0,250)]
    zones[1] = [(250,0), (500,0), (250,250), (500,250)]
    zones[2] = [(0,250), (250,250), (250, 500), (0,500)]
    zones[3] = [(250,250), (500,250), (500,500), (250,500)]

    for i in range(4):
        # Hardcoded hospitals, we can change it later
        hospital_groups[i] = [Hospital(None, 100, 10), Hospital(None, 150, 10), Hospital(None, 95, 10)]
        agents[i] = Agent(zones[i], zones, hospital_groups[i], None)
        for group in hospital_groups:
            for hosp in group:
                hosp.set_control_tower(agents[i])
                medical_vehicles = [MedicalVehicle(100, 100, "available", hosp)] * 20  # enough? or too much?
                hosp.set_medical_vehicles(medical_vehicles)


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
