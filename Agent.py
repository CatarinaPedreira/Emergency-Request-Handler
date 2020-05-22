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
        self.failed_alloc_hospital = False
        self.failed_alloc_vehicles = False

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

    def add_emergency(self, emergency):
        self.emergencies.append(emergency)

    def help_hospital(self, emergency, patient_counter, agents):
        min_distance = math.inf
        min_hospital = None
        min_agent = None
        allocated_patients = 0
        for agent in agents:
            if agent.get_id() != self.get_id():
                for hospital in agent.hospitals:
                    if not hospital.is_full():
                        hospital_dist = self.manhattan_distance(hospital, emergency)
                        if hospital_dist <= min_distance:
                            min_distance = hospital_dist
                            min_hospital = hospital
                            min_agent = agent
                            allocated_patients = hospital.get_slots() - patient_counter

        return min_agent, min_hospital, allocated_patients

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

        agent = self.get_agent_from_hospital(min_vehicle.get_current_hospital(), agents)
        return agent

    def check_enough_medicine(self, vehicle, emergency):
        return vehicle.get_medicine() > vehicle.medicine_needed(emergency.get_gravity(), emergency.get_type())

    def check_enough_fuel(self, vehicle, emergency, hospital):
        return vehicle.get_fuel() > (self.manhattan_distance(vehicle, emergency) + self.manhattan_distance(emergency, hospital))

    def filter_medical_vehicles(self, emergency, min_hospital):
        possible_ambulances = []
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

    def check_closest_hospital(self, emergency, min_distance, patient_counter):
        min_hospital = None
        allocated_patients = 0
        for hospital in self.hospitals:
            hospital_dist = self.manhattan_distance(hospital, emergency)
            if hospital_dist <= min_distance and not hospital.is_full():
                min_distance = hospital_dist
                min_hospital = hospital
                allocated_patients = hospital.get_slots() - patient_counter

        if min_hospital is None:
            print("Couldn't get any free hospital. Will contact nearest zone(s) to ask for help")
            self.failed_alloc_hospital = True
            return None

        if allocated_patients >= 0:
            min_hospital.update_curr_capacity(patient_counter)  # TODO can only update when vehicles arrive to emergency
        else:
            min_hospital.update_curr_capacity(min_hospital.get_slots())

        return min_hospital, allocated_patients

    def activate_medical_vehicles(self, final_vehicles):
        threads = []
        for vehicle in final_vehicles:
            thread = Thread(target=vehicle.move)
            thread.start()
            threads.append(thread)

        wait_threads(threads)       # TODO Why is this here. This means that we have to wait to allocate the rest of the vehicles

    ###################
    # Agent's Decision#
    ###################

    # Not considering collaboration between agents yet
    # (When all hospitals don't have enough resources, ask help of another agent)
    def allocate_emergency(self, emergency, patient_counter, patients_dict, helping, helped_agent):
        patients = -1
        final_vehicles = []
        min_distance = math.inf
        min_vehicle = None
        patients_per_hosp = []
        min_hospital = []
        possible_ambulances = []
        # possible_ambulances[0] tem as ambulancias do min_hospital[0] e o
        # patients_per_hosp[0] tem os pacientes que ficaram no min_hospital[0]

        while patients < 0:
            result = self.check_closest_hospital(emergency, math.inf, patient_counter)
            if result is None:
                return patient_counter, patients_dict, self.failed_alloc_hospital, self.failed_alloc_vehicles
            min_hospital.append(result[0])
            patients = result[1]
            if patients >= 0:
                patients_per_hosp.append(patient_counter)  # quando todos os pacientes ficam no mesmo hospital
            else:
                patients_per_hosp.append(patient_counter + patients)  # quando apenas ficam alguns dos pacientes naquele hospital

        for i in range(len(patients_per_hosp)):
            for j in range(patients_per_hosp[i]):
                for patient in patients_dict.values():
                    if patient.get_e_id() == emergency.get_eid() and patient.get_p_hospital() is None:
                        patient.set_p_hospital(min_hospital[i])
                        break

        for hospital in min_hospital:
            possible_ambulances.append(self.filter_medical_vehicles(emergency, hospital))

        for i in range(len(patients_per_hosp)):
            if patient_counter == emergency.get_num_patients():
                print(patients_per_hosp[i], "patients are going to be taken to Hospital", min_hospital[i].get_id())
            for j in range(patients_per_hosp[i]):
                for h_possibilities in possible_ambulances:
                    for possibility in h_possibilities:

                        if len(emergency.get_type_vehicle()) == 1 and emergency.get_type_vehicle()[0] == possibility.get_type_vehicle():
                            manhattan_dist = self.manhattan_distance(possibility, emergency)
                            if manhattan_dist < min_distance:
                                min_distance = manhattan_dist
                                min_vehicle = possibility

                        elif len(emergency.get_type_vehicle()) > 1:
                            for type_v in emergency.get_type_vehicle():
                                if type_v == possibility.get_type_vehicle():
                                    manhattan_dist = self.manhattan_distance(possibility, emergency)
                                    if manhattan_dist < min_distance:
                                        min_distance = manhattan_dist
                                        min_vehicle = possibility

                    if min_vehicle is not None:
                        h_possibilities.remove(min_vehicle)
                        min_vehicle.decrease_medicine(emergency.get_gravity(), emergency.get_type())
                        min_vehicle.set_em_location(emergency.get_location())
                        min_vehicle.set_em_hospital(min_hospital[i])
                        min_vehicle.set_help_v(helping)
                        final_vehicles.append(min_vehicle)

                    min_distance = math.inf
                    min_vehicle = None

            if len(final_vehicles) == 0:
                print("Error: No vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
            else:
                if len(final_vehicles) == 1 and not helping:
                    print("1 vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
                elif len(final_vehicles) > 1 and not helping:
                    print(len(final_vehicles), "medical vehicles were allocated to deal with emergency nº", emergency.get_eid(), "\n")
                elif len(final_vehicles) == 1 and helping:
                    print("1 vehicle was allocated as backup to help deal with emergency nº", emergency.get_eid(),"from zone", helped_agent.get_id(), "\n")
                elif len(final_vehicles) > 1 and helping:
                    print(len(final_vehicles), "vehicles were allocated as backup to help deal with emergency nº", emergency.get_eid(), "from zone", helped_agent.get_id(), "\n")

                self.activate_medical_vehicles(final_vehicles)

                # TODO when collaboration is done, this can't be here
                for patient in patients_dict.values():
                    if patient.get_e_id() == emergency.get_eid() and patient.get_p_hospital() == min_hospital[i]:
                        patient.set_admission_time()

        patient_counter -= len(final_vehicles)
        if patient_counter < 0:
            patient_counter = 0
        elif patient_counter > 0:
            self.failed_alloc_vehicles = True
            print("Couldn't allocate any vehicle. Will contact nearest zone(s) to ask for help")
        return patient_counter, patients_dict, self.failed_alloc_hospital, self.failed_alloc_vehicles
