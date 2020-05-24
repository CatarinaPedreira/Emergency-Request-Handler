import copy
import time
import math
from threading import Thread


def wait_threads(threads):
    for thread in threads:
        if thread.is_alive():
            thread.join()


class Agent:
    def __init__(self, agent_id, area_border, district_map, hospitals):
        self.agent_id = agent_id
        self.area = area_border
        self.map = district_map
        self.hospitals = hospitals
        self.emergencies = []
        self.other_agents = None

    def manhattan_distance(self, a, b):
        return abs(a.get_location()[0] - b.get_location()[0]) + abs(a.get_location()[1] - b.get_location()[1])

    def get_id(self):
        return self.agent_id

    def get_area(self):
        return self.area

    def get_map(self):
        return self.map

    def get_hospitals(self):
        return self.hospitals

    def get_emergencies(self):
        return self.emergencies

    def set_other_agents(self, agents):
        self.other_agents = agents

    def add_emergency(self, emergency):
        self.emergencies.append(emergency)

    def help_hospital(self, emergency, agents):
        min_distance = math.inf
        min_agent = None
        for agent in agents:
            for hospital in agent.get_hospitals():
                if not hospital.is_full():
                    hospital_dist = self.manhattan_distance(hospital, emergency)
                    if hospital_dist <= min_distance:
                        min_distance = hospital_dist
                        min_agent = agent

        return min_agent

    def get_agent_from_hospital(self, hosp, agents):
        for agent in agents:
            for hospital in agent.hospitals:
                if hosp == hospital:
                    return agent

    def help_vehicle(self, emergency, agents):
        min_distance = math.inf
        min_vehicle = None
        for agent in agents:
            if agent.get_id() != self.get_id():
                for hospital in agent.get_hospitals():
                    for vehicle in hospital.get_medical_vehicles():
                        dist = agent.manhattan_distance(vehicle, emergency)
                        if dist < min_distance:
                            min_distance = dist
                            min_vehicle = vehicle

        if min_vehicle is not None:
            agent = self.get_agent_from_hospital(min_vehicle.get_current_hospital(), agents)
            return agent
        else:
            return None

    def check_enough_medicine(self, vehicle, emergency):
        return vehicle.get_medicine() > vehicle.medicine_needed(emergency.get_gravity(), emergency.get_type())

    def check_enough_fuel(self, vehicle, emergency, hospital):
        return vehicle.get_fuel() > (self.manhattan_distance(vehicle, emergency) + self.manhattan_distance(emergency, hospital))

    def filter_medical_vehicles(self, emergency, min_hospital, possible_ambulances):
        for hospital in self.hospitals:
            for medical_vehicle in hospital.medicalVehicles:
                if medical_vehicle.get_status() == "Available"\
                        and self.check_enough_medicine(medical_vehicle, emergency)\
                        and self.check_enough_fuel(medical_vehicle, emergency, min_hospital):
                    possible_ambulances.append(medical_vehicle)
                elif (not self.check_enough_medicine(medical_vehicle, emergency)) or (not self.check_enough_fuel(medical_vehicle, emergency, min_hospital)):
                    medical_vehicle.change_status("Replenish")
                    medical_vehicle.replenish()  # This way, on the next iteration he will always have enough medicine
                    print(medical_vehicle.type_vehicle, "vehicle", medical_vehicle.id,
                          "replenished fuel and medicine at the hospital")

        return possible_ambulances

    def check_closest_hospital(self, emergency, patient_counter):
        min_distance = math.inf
        min_hospital = None
        allocated_patients = -1
        for hospital in self.hospitals:
            hospital_dist = self.manhattan_distance(hospital, emergency)
            if hospital_dist <= min_distance and not hospital.is_full():
                min_distance = hospital_dist
                min_hospital = hospital
                allocated_patients = hospital.get_slots() - patient_counter
        if min_hospital is not None:
            if allocated_patients >= 0:     # when all patients stay in the same hospital
                allocated_patients = patient_counter
            else:                           # when only some patients stay in the same hospital
                allocated_patients = min_hospital.get_slots()
            min_hospital.update_curr_capacity(allocated_patients)   # TODO can only update when vehicles arrive to emergency
        else:
            allocated_patients = 0

        return min_hospital, allocated_patients

    def activate_medical_vehicles(self, final_vehicles, emergency):
        threads = []
        for vehicle in final_vehicles:
            thread = Thread(target=vehicle.move, args=(emergency,))
            thread.start()
            threads.append(thread)

        wait_threads(threads)  # TODO Why is this here. This means that we have to wait to allocate the rest of the vehicles

    def calculate_possibilities(self, available_ambulances, emergency, final_vehicles, min_hospital, help_flag, hosp_vehicles):
        min_distance = math.inf
        min_vehicle = None
        for possibility in available_ambulances:
            for type_v in emergency.get_type_vehicle():
                if type_v == possibility.get_type_vehicle() and possibility.get_status() == "Available":
                    manhattan_dist = self.manhattan_distance(possibility, emergency)
                    if manhattan_dist < min_distance:
                        min_distance = manhattan_dist
                        min_vehicle = possibility

        if min_vehicle is not None:
            available_ambulances.remove(min_vehicle)
            min_vehicle.change_status("Assigned")
            min_vehicle.set_em_location(emergency.get_location())
            min_vehicle.set_em_hospital(min_hospital)
            min_vehicle.set_help_v(help_flag)
            final_vehicles.append(min_vehicle)
            hosp_vehicles.append(min_vehicle)
        else:
            agent = self.help_vehicle(emergency, self.other_agents)
            if agent is None:
                print("Agent:", self.agent_id, "-All vehicles are unavailable or insufficient, emergency not completed!BU")
                return -1
            possible_ambulances = []
            agent.filter_medical_vehicles(emergency, min_hospital, possible_ambulances)
            agent.calculate_possibilities(possible_ambulances, emergency, final_vehicles, min_hospital, True, hosp_vehicles)

    ###################
    # Agent's Decision#
    ###################

    def allocate_emergency(self, emergency, patient_counter, patients_dict, help_flag, helped_agent):
        patients_left = patient_counter
        final_vehicles = []
        hosp_vehicles = []
        min_hospital = []
        patients_per_hosp = []      # patients_per_hosp[0] has patients that stayed in min_hospital[0]
        possible_ambulances = []    # possible_ambulances[0] has vehicles from min_hospital[0]
        first = True
        while patients_left > 0:
            result = self.check_closest_hospital(emergency, patients_left)
            if result[0] is None:
                if first:
                    first = False
                    print("Agent", self.agent_id, "-All zone hospitals are incapable of allocating all patients to attend.\n"
                                                  "Will contact nearest zone(s) to ask for help")
                agent_help_hospital = self.help_hospital(emergency, self.other_agents)
                if agent_help_hospital is None:
                    print("Agent", self.agent_id, "-Error: All hospitals are full, emergency failed!")
                    return
                else:
                    result = agent_help_hospital.check_closest_hospital(emergency, patients_left)

            min_hospital.append(result[0])
            allocated_patients = result[1]
            patients_left -= allocated_patients
            patients_per_hosp.append(allocated_patients)

        for i in range(len(patients_per_hosp)):
            for j in range(patients_per_hosp[i]):
                for patient in patients_dict.values():
                    if patient.get_e_id() == emergency.get_eid() and patient.get_p_hospital() is None:
                        patient.set_p_hospital(min_hospital[i])
                        break

        for hospital in min_hospital:
            possible_ambulances.append(self.filter_medical_vehicles(emergency, hospital, []))

        error = True
        for i in range(len(patients_per_hosp)):
            if len(possible_ambulances[i]) < patients_per_hosp[i]:
                if error:
                    error = False
                    print("Agent", self.agent_id, "-Not enough zone vehicles to deal with emergency nº", emergency.get_eid(), "\n",
                          "Will contact nearest zone(s) to ask for help")

                agent_help_vehicle = self.help_vehicle(emergency, self.other_agents)
                if agent_help_vehicle is None:
                    print("Agent", self.agent_id, "-Error: All vehicles are unavailable or insufficient, emergency not completed!")
                    return
                else:
                    for hospital in min_hospital:
                        agent_help_vehicle.filter_medical_vehicles(emergency, hospital, possible_ambulances[i])

        for i in range(len(patients_per_hosp)):
            for j in range(patients_per_hosp[i]):
                output = self.calculate_possibilities(possible_ambulances[i], emergency, final_vehicles, min_hospital[i], help_flag, hosp_vehicles)
                if output == -1:
                    return
            if patients_per_hosp[i] > len(hosp_vehicles):
                number_patients = len(hosp_vehicles)
            else:
                number_patients = patients_per_hosp[i]
            hosp_vehicles = []
            if number_patients == 1:
                print(number_patients, "patient is going to be taken to Hospital", min_hospital[i].get_id())
            elif number_patients > 1:
                print(number_patients, "patients are going to be taken to Hospital", min_hospital[i].get_id())

            if number_patients > 0:
                for patient in patients_dict.values():
                    if patient.get_e_id() == emergency.get_eid() and patient.get_p_hospital() == min_hospital[i] and not patient.get_checked_in():
                        patient.set_admission_time()

        if len(final_vehicles) == 1 and not help_flag:
            print("1 vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
        elif len(final_vehicles) > 1 and not help_flag:
            print(len(final_vehicles), "medical vehicles were allocated to deal with emergency nº", emergency.get_eid(), "\n")
        elif len(final_vehicles) == 1 and help_flag:
            print("1 vehicle was allocated as backup to help deal with emergency nº", emergency.get_eid(), "from zone", helped_agent, "\n")
            with open('out.txt', 'a') as f:
                print('+ 1', file=f)
        elif len(final_vehicles) > 1 and help_flag:
            with open('out.txt', 'a') as f:
                print('+', len(final_vehicles), file=f)
            print(len(final_vehicles), "vehicles were allocated as backup to help deal with emergency nº", emergency.get_eid(), "from zone", helped_agent, "\n")

        self.activate_medical_vehicles(final_vehicles, emergency)

        return patient_counter, patients_dict
