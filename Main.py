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
# quit_switch = False


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
    #            for j in range(math.ceil(nVehicles * 0.7)):
    #                medical_vehicles += MedicalVehicle("SBV", 100, 100, "Available", hosp, None), # ultimo none tem que ter valor!!!
    #            distribution = math.ceil(nVehicles * 0.7)
    #            for j in range(math.ceil(nVehicles * 0.2)):
    #                medical_vehicles += MedicalVehicle("VMER", 100, 100, "Available", hosp, None), # ultimo none tem que ter valor!!!
    #            distribution += math.ceil(nVehicles * 0.2)
    #            for j in range((nVehicles - distribution)):
    #                medical_vehicles += MedicalVehicle("SIV", 100, 100, "Available", hosp, None), # ultimo none tem que ter valor!!!
    #            hosp.set_medical_vehicles(medical_vehicles)

    zones = [[(0, 0), (500, 0), (0, 500), (500, 500)], [(500, 0), (1000, 0), (500, 500), (1000, 500)],
             [(0, 500), (500, 500), (0, 1000), (500, 1000)], [(500, 500), (1000, 500), (500, 1000), (1000, 1000)]]
    for i in range(4):
        # Hardcoded to test, change to new version later (locations may collide, but it is extremely rare)
        location1 = (random.randint(zones[i][0][0], zones[i][0][0] + 500), random.randint(zones[i][0][1], zones[i][0][1] + 500))
        location2 = (random.randint(zones[i][0][0], zones[i][0][0] + 500), random.randint(zones[i][0][1], zones[i][0][1] + 500))
        location3 = (random.randint(zones[i][0][0], zones[i][0][0] + 500), random.randint(zones[i][0][1], zones[i][0][1] + 500))
        hospital_groups[i] = [Hospital(location1, 100, 10, None), Hospital(location2, 150, 10, None),
                              Hospital(location3, 95, 10, None)]
        agents[i] = Agent(zones[i], zones, hospital_groups[i], None)

    # Hardcoded minMedicine and minFuel on MedicalVehicles (15 e 10), can change the values if u want
    for i in range(4):
        for hosp in hospital_groups[i]:
            hosp.set_control_tower(agents[i])
            medical_vehicles = []
            for j in range(6):
                medical_vehicles.append(MedicalVehicle("SBV", 100, 100, "Available", hosp, hosp.get_location(), 15, 10))
            for j in range(4):
                medical_vehicles.append(
                    MedicalVehicle("VMER", 100, 100, "Available", hosp, hosp.get_location(), 15, 10))
            for j in range(2):
                medical_vehicles.append(MedicalVehicle("SIV", 100, 100, "Available", hosp, hosp.get_location(), 15, 10))
            hosp.set_medical_vehicles(medical_vehicles)


# TODO Fix dar no máximo x tipos para x pacientes.
def create_emergency(e_id):
    for i in range(4):  # TODO 4 porque hardcoded, depois tera que ser range(nAgents)
        for hospital in hospital_groups[i]:
            for vehicle in hospital.get_medical_vehicles():
                vehicle.check_vehicle_status()

    e_type = random.choice(emergency_types)

    patients = 1000
    while patients > 100:
        patients = round(random.lognormvariate(0, 3)) + 1

    location = (random.randint(0, 1000), random.randint(0, 1000))
    gravity = random.randint(0, 10)

    if e_type == "Non life-threatening":
        vehicles = ["SBV"]
    elif patients == 1:
        vehicles = random.sample(vehicle_types, k=1)
    else:
        n = random.randint(1, 3)
        vehicles = numpy.random.choice(vehicle_types, n, replace=False, p=[0.5, 0.3, 0.2])

    print("New emergency arrived at the system.", "id:" + str(e_id), "type:" + str(e_type), "location:" + str(location), "num of patients:" + str(patients), "type of vehicles:" + str(vehicles))
    return Emergency(e_id, location, e_type, patients, gravity, vehicles)


def allocate_to_agent(emer):
    for i in range(len(zones)):
        if zones[i][0][0] <= emer.location[0] <= zones[i][1][0] and zones[i][0][1] <= emer.location[1] <= zones[i][2][1]:
            emer.set_control_tower(agents[i])
            break

    # this comment section is for when we start accepting input from the command line
    # TODO not tested yet, should be good tho
    # for i in range(len(zones)):
    #   for j in range(len(zones[i])):
    #       if zones[i][j][0][0] <= emer.location[0] <= zones[i][j][2][0] and zones[i][j][0][1] <= emer.location[0] <= zones[i][j][1][1]:
    #           for agent in agents:
    #               if agent.get_area() == zones[i][j]:
    #                   emer.set_control_tower(agent)
    #                   break
    #           break

    print("Emergency nº", emergency_id, "allocated to control tower from zone", i)
    emer.get_control_tower().allocate_emergency(emer)


# def check_quit():
#     global quit_switch
#     keyboard.wait("q")
#     quit_switch = True
#     print("Goodbye!")

def perceive_emergencies():
    # thread = Thread(target=check_quit)
    # thread.start()
    # thread.join()

    while True:
        # if quit_switch:
        #     break
        global emergency_id
        emergency_id += 1
        emergency = create_emergency(emergency_id)
        time.sleep(3)  # Creates an emergency each 3 seconds, later change for "frequency" received in input
        allocate_to_agent(emergency)


########################################################################################################################

setup()
perceive_emergencies()
