import random
import sys
import time
import math
# from threading import Thread
# import keyboard
import numpy
from Agent import Agent
from Emergency import Emergency
from MedicalVehicle import MedicalVehicle
from Hospital import Hospital

zones = []
agents = []
hospital_groups = []
emergency_types = ("Life-threatening", "Non life-threatening")
vehicle_types = ("SBV", "VMER", "SIV")
emergency_id = 0
width = 0
height = 0
cycle_time = 1
zone_ids = [[]]
zone_id = 0
# quit_switch = False


def setup():
    global zones, hospital_groups, agents, width, height, cycle_time, zone_ids, zone_id

    print("-------------------Medical Emergencies Dispatcher System-------------------")
    area = eval(input("Area size (as width,height): "))
    n_agents = eval(input("Number of Control Towers: "))
    n_hospitals = eval(input("Number of Hospitals per zone: "))
    n_vehicles = eval(input("Number of Medical Vehicles per hospital: "))
    cycle_time = eval(input("Frequency of Medical Emergencies (in seconds): "))

    width = area[0]
    height = area[1]
    n_rows = 0
    n_columns = 0

    # calculate zones in accordance with number of agents (towers)
    for i in range(int(math.sqrt(n_agents)), 0, -1):
        if n_agents % i == 0:
            n_rows = i
            n_columns = n_agents//i
            for m in range(n_rows):
                zones += [],
                zone_ids += [],
                for n in range(n_columns):
                    zones[m] += [(), (), (), ()],
                    zone_ids[m] += [(), (), (), ()]
                    zones[m][n][0] = (height / n_rows * m, width / n_columns * n)
                    zones[m][n][1] = (height / n_rows * m, width / n_columns * (n + 1))
                    zones[m][n][2] = (height / n_rows * (m + 1), width / n_columns * n)
                    zones[m][n][3] = (height / n_rows * (m + 1), width / n_columns * (n + 1))
                    zone_ids[m][n] = zone_id
                    zone_id += 1
            break

    for i in range(n_agents):
        hospital_groups += [],
        for j in range(n_hospitals):
            hospital_groups[i] += Hospital(),
        column = i
        row = 0
        while column >= n_columns:
            row += 1
            column -= n_columns
        agents += Agent(zones[row][column], zones, hospital_groups[i], cycle_time),

    for i in range(n_agents):
        for hospital in agents[i].get_hospitals():
            location = (random.randint(agents[i].get_area()[0][0], agents[i].get_area()[2][0]), random.randint(agents[i].get_area()[0][1], agents[i].get_area()[1][1]))
            hospital.set_location(location)

    # Hardcoded minMedicine and minFuel on MedicalVehicles (30 ei 10), can change the values if u want
    # minMedicine, if changed, should be in accordance with MedicalVehicle.decrease_medicine(type, gravity)
    sbv_id = 0
    vmer_id = 0
    siv_id = 0
    for i in range(n_agents):
        for hosp in hospital_groups[i]:
            hosp.set_control_tower(agents[i])
            medical_vehicles = []
            d1 = math.ceil(n_vehicles * 0.8)
            for j in range(d1):
                sbv_id += 1
                medical_vehicles += MedicalVehicle(sbv_id, "SBV", hosp),
            d2 = math.ceil(n_vehicles * 0.15)
            for j in range(d2):
                vmer_id += 1
                medical_vehicles += MedicalVehicle(vmer_id, "VMER", hosp),
            for j in range(n_vehicles - d1 - d2):
                siv_id += 1
                medical_vehicles += MedicalVehicle(siv_id, "SIV", hosp),
            hosp.set_medical_vehicles(medical_vehicles)

    # cycle_time = 1 # Hardcoded, vamos receber do utilizador
    # zones = [[(0, 0), (500, 0), (0, 500), (500, 500)], [(500, 0), (1000, 0), (500, 500), (1000, 500)],
    #          [(0, 500), (500, 500), (0, 1000), (500, 1000)], [(500, 500), (1000, 500), (500, 1000), (1000, 1000)]]


        # Hardcoded to test, change to new version later (locations may collide, but it is extremely rare)
        # location1 = (random.randint(zones[i][0][0], zones[i][0][0] + 500), random.randint(zones[i][0][1], zones[i][0][1] + 500))
        # location2 = (random.randint(zones[i][0][0], zones[i][0][0] + 500), random.randint(zones[i][0][1], zones[i][0][1] + 500))
        # location3 = (random.randint(zones[i][0][0], zones[i][0][0] + 500), random.randint(zones[i][0][1], zones[i][0][1] + 500))
        # hospital_groups[i] = [Hospital(location1, 100, 10, None), Hospital(location2, 150, 10, None), Hospital(location3, 95, 10, None)]
        # agents[i] = Agent(zones[i], zones, hospital_groups[i], None, cycle_time)

    # Hardcoded minMedicine and minFuel on MedicalVehicles (30 e 10), can change the values if u want
    # minMedicine, if changed, should be in accordance with MedicalVehicle.decrease_medicine(type, gravity)
    # for i in range(4):
    #     for hosp in hospital_groups[i]:
    #         hosp.set_control_tower(agents[i])
    #         medical_vehicles = []
    #         for j in range(6):
    #             medical_vehicles.append(MedicalVehicle("SBV", 100, 100, hosp, list(hosp.get_location()), 30, 10))
    #         for j in range(4):
    #             medical_vehicles.append(MedicalVehicle("VMER", 100, 100, hosp, list(hosp.get_location()), 30, 10))
    #         for j in range(2):
    #             medical_vehicles.append(MedicalVehicle("SIV", 100, 100, hosp, list(hosp.get_location()), 30, 10))
    #         hosp.set_medical_vehicles(medical_vehicles)


def create_emergency(e_id):
    e_type = random.choice(emergency_types)

    patients = 100     # just a big number
    while patients > 20:
        patients = round(random.lognormvariate(0, 4)) + 1

    location = (random.randint(0, width), random.randint(0, height))
    gravity = random.randint(1, 10)

    vehicles = ["VMER"]
    if e_type == "Non life-threatening":
        vehicles = ["SBV"]
    else:
        if patients == 1:
            n = 1
        elif patients == 2:
            n = numpy.random.choice([1, 2], 1, p=[0.9, 0.1])
        else:
            n = numpy.random.choice([1, 2, 3], 1, p=[0.85, 0.10, 0.05])
        while "VMER" in vehicles and ("SBV" not in vehicles and "SIV" not in vehicles):     # because VMER can't be allocated alone
            vehicles = numpy.random.choice(vehicle_types, n, replace=False, p=[0.7, 0.20, 0.10])

    emergency = Emergency(e_id, location, e_type, patients, gravity, vehicles)
    print("-------------------------------New Emergency-------------------------------")
    print(emergency)
    return emergency


def allocate_to_agent(emer):
    # for i in range(len(zones)):
    #     if zones[i][0][0] <= emer.location[0] <= zones[i][1][0] and zones[i][0][1] <= emer.location[1] <= zones[i][2][1]:
    #         emer.set_control_tower(agents[i])
    #         break

    # this comment section is for when we start accepting input from the command line
    # TODO not tested yet, should be good tho NOP is always allocating to 1
    for i in range(len(zones)):
        for j in range(len(zones[i])):
            if zones[i][j][0][0] <= emer.location[0] <= zones[i][j][2][0] and zones[i][j][0][1] <= emer.location[1] <= zones[i][j][1][1]:
                for agent in agents:
                    if agent.get_area() == zones[i][j]:
                        emer.set_control_tower(agent)
                        print("Emergency nº", emergency_id, "allocated to control tower from zone", zone_ids[i][j])
                        break
                break

    emer.get_control_tower().allocate_emergency(emer)


def perceive_emergencies():

    while True:
        global emergency_id
        emergency_id += 1
        emergency = create_emergency(emergency_id)
        time.sleep(cycle_time)
        allocate_to_agent(emergency)


########################################################################################################################

setup()
perceive_emergencies()


# thread = Thread(target=check_quit)
# thread.start()
# thread.join()
# def check_quit():
#     global quit_switch
#     keyboard.wait("q")
#     quit_switch = True
#     print("Goodbye!")
# Na main, check se o quit_switch esta = True
