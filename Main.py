import tkinter
from PIL import ImageTk, Image
import sys
import time
import math
from threading import Thread

from Agent import Agent
from Emergency import Emergency
from Hospital import Hospital
from MedicalVehicle import MedicalVehicle

canvas = None
zones = []
agents = [None, None, None, None]
hospital_groups = [[None], [None], [None], [None]]


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
    # line = 'Agents=x Hospitals/zone=x Ambulances/zone=x Emergencies-frequency=x'
    #line = (sys.stdin.readline()).split(' ')
    #nAgents = int(line[0])
    #nHospitals = int(line[1])
    #medical_vehicles = int(line[2])
    #emer_frequency = int(line[3])

    global zones

    #for i in range(int(math.sqrt(nAgents)), 0, -1):
    #    if nAgents % i == 0:
    #        nRows = i
    #        nColumns = nAgents//i
    #        for m in range (nRows):
    #            zones += [],
    #            for n in range(nColumns):
    #                zones[m] += [(), (), (), ()],
    #                zones[m][n][0] = (1000/nRows*m, 1000/nColumns*n)
    #                zones[m][n][1] = (1000/nRows*m, 1000/nColumns*(n+1))
    #                zones[m][n][2] = (1000/nRows*(m+1), 1000/nColumns*n)
    #                zones[m][n][3] = (1000/nRows*(m+1), 1000/nColumns*(n+1))
    #        break




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
