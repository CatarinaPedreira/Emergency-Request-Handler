import tkinter
from PIL import ImageTk, Image
import random
import numpy as np
import sys
import time
from threading import Thread

from Agent import Agent
from Emergency import Emergency
from Hospital import Hospital
from MedicalVehicle import MedicalVehicle

canvas = None
zones = []
agents = [None, None, None, None]
hospital_groups = [[None], [None], [None], [None]]
emergency_types = ("Life-threatening", "Non life-threatening")
vehicle_types = ("SBV", "VMER", "SIV")
emergency_id = 0


def create_board():
    global canvas
    canvas_width = 500
    canvas_height = 500
    board = tkinter.Tk()
    canvas = tkinter.Canvas(board, width=canvas_width, height=canvas_height)
    canvas.create_line(250, 0, 250, 500, fill="black")
    canvas.create_line(0, 250, 500, 250, fill="black")

    # Setting it up
    image = Image.open("imgs/ambula-02.png")
    image = image.resize((50, 50), Image.ANTIALIAS)  # The (250, 250) is (height, width)
    img = ImageTk.PhotoImage(image)
    canvas.create_image(60, 20, image=img)

    # Displaying it
    #tkinter.Label(canvas, image=img).grid(row=1, column=1)

# TODO create shapes for agents in each zone, hospitals around them
    # Check how to draw cool baby ambulances!
    canvas.pack()
    board.mainloop()


def setup():
    global zones
    zones = [[(0, 0), (250, 0), (0, 250), (250, 250)], [(250, 0), (500, 0), (250, 250), (500, 250)],
             [(0, 250), (250, 250), (0, 500), (250, 500)], [(250, 250), (500, 250), (250, 500), (500, 500)]]
    for i in range(4):
        # Hardcoded hospitals, we can change it later
        hospital_groups[i] = [Hospital(None, 100, 10), Hospital(None, 150, 10), Hospital(None, 95, 10)]
        agents[i] = Agent(zones[i], zones, hospital_groups[i], None)

    for i in range(4):
        for group in hospital_groups:
            for hosp in group:
                hosp.set_control_tower(agents[i])
                medical_vehicles = [MedicalVehicle(100, 100, "available", hosp)] * 5  # enough?
                hosp.set_medical_vehicles(medical_vehicles)


def create_emergency(e_id):
    e_id += 1
    e_type = random.choice(emergency_types)

    patients = 1000
    while patients > 100:
        patients = round(random.lognormvariate(0, 3)) + 1

    location = (random.randint(0, 1000), random.randint(0, 1000))
    gravity = random.randint(0, 10)
    description = "emergency description"

    if e_type == "Non life-threatening":
        vehicles = tuple("SBV")
    elif patients == 1:
        vehicles = random.sample(vehicle_types, k=1)
    else:
        n = random.randint(1, 3)
        vehicles = np.random.choice(vehicle_types, n, replace=False, p=[0.5, 0.3, 0.2])

    return Emergency(e_id, location, e_type, patients, gravity, vehicles, description)


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
