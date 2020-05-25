import copy
import os
import random
import signal
import subprocess
import sys
import time
import math
import numpy
from threading import Thread
from Agent import Agent
from Emergency import Emergency
from MedicalVehicle import MedicalVehicle
from Hospital import Hospital
from Patient import Patient

start = time.time()
PERIOD_OF_TIME = 300

zones = []
agents = []
hospital_groups = []
emergency_types = ("Life-threatening", "Non life-threatening")
vehicle_types = ("SBV", "VMER", "SIV")
emergency_id = 0
width = 1000
height = 1000
cycle_time = 0
zone_ids = [[]]
zone_id = 0
run = True
emergency_queue = []
flag_t = False
flag_ot = False
patients_dict = {}
patient_id = 0
agent_id = 0


# ---------------------------------------------INITIAL_VALUES_INPUT-----------------------------------------------------
def sanitize_integer_input(arg, val):
    s = "Invalid input. Please insert a positive integer (minimum value:" + str(val) + "): "
    while not arg.isdigit() or int(arg) < val:
        arg = input(s)
    return int(arg)


def setup():
    global zones, hospital_groups, agents, width, height, cycle_time, zone_ids, zone_id, agent_id

    print("-------------------Medical Emergencies Dispatcher System-------------------")
    n_agents = input("Number of Control Towers: ")
    n_agents = sanitize_integer_input(n_agents, 2)
    n_hospitals = input("Number of Hospitals per zone: ")
    n_hospitals = sanitize_integer_input(n_hospitals, 1)
    n_vehicles = input("Number of Medical Vehicles per hospital (minimum 3): ")
    n_vehicles = sanitize_integer_input(n_vehicles, 3)
    if not flag_ot:
        cycle_time = input("Frequency of Medical Emergencies (in seconds): ")
        cycle_time = sanitize_integer_input(cycle_time, 0)

    with open('plots/out11_0.txt', 'a') as file:
        print(n_vehicles, file=file)

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
        agent_id += 1
        agents += Agent(agent_id, zones[row][column], hospital_groups[i]),

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

        list_agents = copy.deepcopy(agents)
        del list_agents[i]
        agents[i].set_other_agents(list_agents)


# ----------------------------------------AUTOMATIC_EMERGENCY_CREATION--------------------------------------------------
def create_emergency(e_id):
    global patients_dict, patient_id

    if e_id != 1:
        time.sleep(cycle_time)

    e_type = random.choice(emergency_types)
    location = (random.randint(0, width), random.randint(0, height))
    gravity = random.randint(1, 10)

    patients = 100     # just a big number
    while patients > 20:
        patients = round(random.lognormvariate(0, 4)) + 1
    for i in range(patients):
        patient_id += 1
        patients_dict[patient_id] = Patient(patient_id, e_id, gravity)

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
    return emergency


# -----------------------------------------AGENT_ALLOCATION-------------------------------------------------------------
def get_agent_from_hospital(hosp):
    for agent in agents:
        for hospital in agent.hospitals:
            if hosp == hospital:
                return agent


def decide_frontier_agent(a_possibilities, emer):
    min_distance = math.inf
    min_vehicle = None
    for agent in a_possibilities:
        for hospital in agent.get_hospitals():
            for vehicle in hospital.get_medical_vehicles():
                dist = agent.manhattan_distance(vehicle, emer)
                if dist < min_distance:
                    min_distance = dist
                    min_vehicle = vehicle

    agent = get_agent_from_hospital(min_vehicle.get_hospital_base())   # Curr hospital because with collaboration this vehicle may not be within its initial zone
    return agent


def allocate_to_agent(emergency):
    global patients_dict

    emergency_agents = []
    indexes = []

    for i in range(len(zones)):
        for j in range(len(zones[i])):
            if zones[i][j][0][0] <= emergency.location[0] <= zones[i][j][2][0] and zones[i][j][0][1] <= emergency.location[1] <= zones[i][j][1][1]:
                for agent in agents:
                    if agent.get_area() == zones[i][j]:
                        emergency_agents.append(agent)
                        indexes.append((i, j))
                        break
                break

    if len(emergency_agents) > 1:
        agent = decide_frontier_agent(emergency_agents, emergency)
    else:  # Len will never be 0 given the boundaries we give to the locations of emergencies
        agent = emergency_agents[0]
    emergency.set_control_tower(agent)

    print("Emergency nº", emergency_id, "allocated to control tower from zone",
          zone_ids[(indexes[emergency_agents.index(agent)][0])][(indexes[emergency_agents.index(agent)][1])])  # zone_ids[row,column]

    agent.allocate_emergency(emergency, emergency.get_num_patients(), patients_dict, False, None)


def perceive_emergencies():
    global emergency_id, emergency_queue, patients_dict, patient_id
    while run:
        emergency_id += 1
        emergency = None
        while emergency is None:
            if len(emergency_queue) != 0:
                emergency = emergency_queue.pop(0)
                emergency.set_eid(emergency_id)
                for i in range(emergency.get_num_patients()):
                    patient_id += 1
                    patients_dict[patient_id] = Patient(patient_id, emergency.get_eid(), emergency.get_gravity())
            else:
                if not flag_ot:
                    emergency = create_emergency(emergency_id)
        print("-------------------------------New Emergency-------------------------------")
        print(emergency)
        allocate_to_agent(emergency)
        if time.time() > start + PERIOD_OF_TIME:
            print("Finished")
            break

# --------------------------------------------CHECK_UPDATES-------------------------------------------------------------
def global_check_and_update():
    global run, patients_dict

    patient_del = []
    while run:
        # Decreases rest time of ambulances
        for agent in agents:
            for hospital in agent.get_hospitals():
                for vehicle in hospital.get_medical_vehicles():
                    vehicle.check_vehicle_status()

        # Remove patient from hospital
        for key in patients_dict:
            p_time = patients_dict[key].check_admission_time()
            if p_time == 0:
                patients_dict[key].get_p_hospital().update_curr_capacity(-1)
                patient_del.append(key)
        for pat in patient_del:
            del patients_dict[pat]
        patient_del = []
        # 0.36s <=> 1 hour in real-life time
        time.sleep(0.36)  # wait to decrease ambulances rest and patient's remaining time in hospital.


thread_updates = Thread(target=global_check_and_update)


# ---------------------------------------RECEIVE_INPUT_FROM_TERMINAL----------------------------------------------------
def check_new_input():
    global emergency_queue, p
    while run:
        args = str(width) + "," + str(height)
        code = 'start /wait python -c \"from Input import setup; setup(' + args + ')\"'
        p = subprocess.Popen(code, shell=True)
        p.wait()
        if os.path.exists("temp.txt"):
            f = open("temp.txt", "r")
            for line in f:
                if line.startswith("Location:"):
                    location = line.split(": ")[1].replace('\n', '').replace(')', '').replace('(', '').replace(' ', '')
                    location = location.split(",")
                    location[0] = int(location[0])
                    location[1] = int(location[1])
                    location = tuple(location)
                elif line.startswith("Type:"):
                    e_type = line.split(": ")[1].replace('\n', '')
                elif line.startswith("Patients:"):
                    patients = int(line.split(": ")[1].replace('\n', ''))
                elif line.startswith("Gravity:"):
                    gravity = int(line.split(": ")[1].replace('\n', ''))
                elif line.startswith("Type of vehicles:"):
                    vehicle_type = []
                    vehicles = line.split(": ")[1].replace('\n', '').replace(']', '').replace('[', '').replace(' ', '').replace('\'', '')
                    vehicles = vehicles.split(",")
                    for v in vehicles:
                        vehicle_type.append(v)
            f.close()
            os.remove("temp.txt")
            e = Emergency(-1, location, e_type, patients, gravity, vehicle_type)
            emergency_queue.append(e)


thread_input = Thread(target=check_new_input)


# -----------------------------------------------SIGNAL_HANDLER---------------------------------------------------------
def signal_handler(signal, frame):
    global run, thread_updates, p
    run = False
    if thread_updates.is_alive():
        thread_updates.join()
    if thread_input.is_alive():
        string = "Taskkill /PID " + str(p.pid) + " /F"
        subprocess.check_output(string)
        thread_input.join()
    print('\nThe simulation has ended')
    sys.exit()


# -----------------------------------------------RUNNING_CODE-----------------------------------------------------------
signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) > 1:
    if sys.argv[1] == "-t":
        flag_t = True
    elif sys.argv[1] == "-ot":
        flag_ot = True

setup()
# to open with terminal input use flag -t or -ot (to only receive emergencies from terminal): py Main.py -t
if flag_t:
    thread_input.start()
elif flag_ot:
    thread_input.start()
thread_updates.start()
perceive_emergencies()
thread_updates.join()
