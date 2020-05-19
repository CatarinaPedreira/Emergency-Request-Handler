import random
import signal
import sys
import time
import math
from threading import Thread
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
run = True


def check_if_comma(string):
    while "," not in string:
        string = input("Invalid input. Please insert two positive integer values (as width,height): ")
    return string.split(",")


# isnumeric () returns True if all characters in the string are numeric characters, so negative numbers are not accepted
# "" checks if enter was pressed
def sanitize_integer_input(arg):
    while not arg.isnumeric() or arg == "0" or arg == "":
        arg = input("Invalid input. Please insert a positive integer value: ")
    return int(arg)


def sanitize_area_input(area):
    area = check_if_comma(area)
    while (not area[0].isnumeric()) or (not area[1].isnumeric()) or area[0] == "0" or area[1] == "0":
        area = check_if_comma(area)

    area[0] = int(area[0])
    area[1] = int(area[1])
    return tuple(area)


def setup():
    global zones, hospital_groups, agents, width, height, cycle_time, zone_ids, zone_id

    print("-------------------Medical Emergencies Dispatcher System-------------------")
    area = input("Area size (as width,height): ")
    area = sanitize_area_input(area)
    n_agents = input("Number of Control Towers: ")
    n_agents = sanitize_integer_input(n_agents)
    n_hospitals = input("Number of Hospitals per zone: ")
    n_hospitals = sanitize_integer_input(n_hospitals)
    n_vehicles = input("Number of Medical Vehicles per hospital: ")
    n_vehicles = sanitize_integer_input(n_vehicles)
    cycle_time = input("Frequency of Medical Emergencies (in seconds): ")
    cycle_time = sanitize_integer_input(cycle_time)

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
                    zone_id += 1
                    zones[m][n][0] = (height / n_rows * m, width / n_columns * n)
                    zones[m][n][1] = (height / n_rows * m, width / n_columns * (n + 1))
                    zones[m][n][2] = (height / n_rows * (m + 1), width / n_columns * n)
                    zones[m][n][3] = (height / n_rows * (m + 1), width / n_columns * (n + 1))
                    zone_ids[m][n] = zone_id
            break

    hosp_id = 0
    for i in range(n_agents):
        hospital_groups += [],
        for j in range(n_hospitals):
            hosp_id += 1
            hospital_groups[i] += Hospital(hosp_id),
        column = i
        row = 0
        while column >= n_columns:
            row += 1
            column -= n_columns
        agents += Agent(zones[row][column], zones, hospital_groups[i], cycle_time),

    for i in range(n_agents):
        for hospital in agents[i].get_hospitals():
            location = (random.randint(math.ceil(agents[i].get_area()[0][0]), math.floor(agents[i].get_area()[2][0])), random.randint(math.ceil(agents[i].get_area()[0][1]), math.floor(agents[i].get_area()[1][1])))
            hospital.set_location(location)

    sbv_id = 0
    vmer_id = 0
    siv_id = 0
    for i in range(n_agents):
        for hosp in hospital_groups[i]:
            hosp.set_control_tower(agents[i])
            medical_vehicles = []
            d1 = math.ceil(n_vehicles * 0.05)
            for j in range(d1):
                sbv_id += 1
                medical_vehicles += MedicalVehicle(sbv_id, "SIV", hosp),
            d2 = math.ceil(n_vehicles * 0.15)
            for j in range(d2):
                vmer_id += 1
                medical_vehicles += MedicalVehicle(vmer_id, "VMER", hosp),
            for j in range(n_vehicles - d1 - d2):
                siv_id += 1
                medical_vehicles += MedicalVehicle(siv_id, "SBV", hosp),
            hosp.set_medical_vehicles(medical_vehicles)


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

    for i in range(len(zones)):
        for j in range(len(zones[i])):
            if zones[i][j][0][0] <= emer.location[0] <= zones[i][j][2][0] and zones[i][j][0][1] <= emer.location[1] <= zones[i][j][1][1]:
                for agent in agents:
                    if agent.get_area() == zones[i][j]:
                        emer.set_control_tower(agent)
                        print("Emergency nº", emergency_id, "allocated to control tower from zone", zone_ids[i][j])
                        break
                break
    patients = emer.get_num_patients()
    while patients > 0:
        patients = emer.get_control_tower().allocate_emergency(emer, patients)


def perceive_emergencies():

    while run:
        global emergency_id
        emergency_id += 1
        emergency = create_emergency(emergency_id)
        time.sleep(cycle_time)
        allocate_to_agent(emergency)


########################################################################################################################

def global_check_and_update():
    global run
    while run:
        for agent in agents:
            for hospital in agent.get_hospitals():
                for vehicle in hospital.get_medical_vehicles():
                    vehicle.check_vehicle_status()
        time.sleep(cycle_time / 100)


thread = Thread(target=global_check_and_update)


def signal_handler(signal, frame):
    global run, thread
    run = False
    print('\nThe simulation has ended')
    if thread.is_alive():
        thread.join()
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)

setup()
thread.start()
perceive_emergencies()
thread.join()
