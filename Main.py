import random
import sys
import time
import math
from threading import Thread

import keyboard
import numpy
from Agent import Agent
from Emergency import Emergency
from MedicalVehicle import MedicalVehicle
from Hospital import Hospital

zones = []
agents = [None, None, None, None]
# agents = []
hospital_groups = [[None], [None], [None], [None]]
# hospital_groups=[]
# nRows = 0
# nColumns = 0
emergency_types = ("Life-threatening", "Non life-threatening")
vehicle_types = ("SBV", "VMER", "SIV")
emergency_id = 0
quit_switch = False


def setup():
    global zones
    #    global zones, hospital_groups, agents, nRows, nColumns

    # line = 'Agents=x Hospitals/zone=x Ambulances/zone=x Emergencies-frequency=x' - exemplo
    #    line = (sys.stdin.readline()).split(' ')
    #    nAgents = int(line[0])
    #    nHospitals = int(line[1])
    #    nVehicles = int(line[2])
    #    emer_frequency = int(line[3])

    #    for i in range(int(math.sqrt(nAgents)), 0, -1):
    #        if nAgents % i == 0:
    #            nRows = i
    #            nColumns = nAgents//i
    #            for m in range (nRows):
    #                zones += [],
    #                for n in range(nColumns):
    #                    zones[m] += [(), (), (), ()],
    #                    zones[m][n][0] = (1000/nRows*m, 1000/nColumns*n)
    #                    zones[m][n][1] = (1000/nRows*m, 1000/nColumns*(n+1))
    #                    zones[m][n][2] = (1000/nRows*(m+1), 1000/nColumns*n)
    #                    zones[m][n][3] = (1000/nRows*(m+1), 1000/nColumns*(n+1))
    #            break

    #    for i in range(nAgents):
    #        hospital_groups += [],
    #        for j in range(nHospitals):
    #            hospital_groups[i] += Hospital(None, None, 100, None), # primeiro none tem que ter valor!!!
    #        column = i
    #        row = 0
    #        while column >= nColumns:
    #            row += 1
    #            column -= nColumns
    #        agents += Agent(zones[row][column], zones, hospital_groups[i], None),

    #    for i in range(nAgents):
    #        for hosp in hospital_groups[i]:
    #            hosp.set_control_tower(agents[i])
    #            medical_vehicles = []
    #            for j in range(math.ceil(nVehicles * 0.8)):
    #                medical_vehicles += MedicalVehicle("SBV", 100, 100, "available", hosp, None), # ultimo none tem que ter valor!!!
    #            for j in range(math.floor(nVehicles * 0.2)):
    #                medical_vehicles += MedicalVehicle("VMER", 100, 100, "available", hosp, None), # ultimo none tem que ter valor!!!
    #            hosp.set_medical_vehicles(medical_vehicles)

    zones = [[(0, 0), (500, 0), (0, 500), (500,500)], [(500, 0), (1000, 0), (500, 500), (1000, 500)],
             [(0, 500), (500, 500), (0, 1000), (500, 1000)], [(500, 500), (1000, 500), (500, 1000), (1000, 1000)]]
    for i in range(4):
        # Hardcoded hospitals, we can change it later
        hospital_groups[i] = [Hospital(None, 100, 10, None), Hospital(None, 150, 10, None),
                              Hospital(None, 95, 10, None)]  # primeiro none (location) tem que ter valor!!!
        agents[i] = Agent(zones[i], zones, hospital_groups[i], None)

    for i in range(4):
        for hosp in hospital_groups[i]:
            hosp.set_control_tower(agents[i])
            medical_vehicles = []
            for j in range(4):
                medical_vehicles += MedicalVehicle("SBV", 100, 100, "available", hosp,
                                                   None),  # ultimo none tem que ter valor!!!
            medical_vehicles += MedicalVehicle("VMER", 100, 100, "available", hosp,
                                               None),  # ultimo none tem que ter valor!!!
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
        vehicles = ["SBV"]
    elif patients == 1:
        vehicles = random.sample(vehicle_types, k=1)
    else:
        n = random.randint(1, 3)
        vehicles = numpy.random.choice(vehicle_types, n, replace=False, p=[0.5, 0.3, 0.2])

    return Emergency(e_id, location, e_type, patients, gravity, vehicles, description)


def allocate_to_agent(emer):
    for i in range(len(zones)):
        if zones[i][0][0] <= emer.location[0] <= zones[i][1][0] and zones[i][0][1] <= emer.location[1] <= zones[i][2][1]:
            emer.set_control_tower(agents[i])
            print(emer.get_control_tower())

    # this comment section is for when we start accepting input from the command line
    #

    emer.get_control_tower().allocate_emergency(emer)
    print("Criei uma emergência!")


# def check_quit():
#     global quit_switch
#     keyboard.wait("q")
#     quit_switch = True
#     print("Goodbye!")


#######################################################################################################################

setup()
# thread = Thread(target=check_quit)
# thread.start()
# thread.join()

while True:
    if quit_switch:
        break
    emergency = create_emergency(emergency_id)
    allocate_to_agent(emergency)
    time.sleep(3) # Creates an emergency each 3 seconds, we can change
    thread = Thread(target=allocate_to_agent, args=(emergency,))
    thread.start()
    thread.join()
