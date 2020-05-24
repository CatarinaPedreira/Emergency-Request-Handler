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
        # min_hospital = None
        min_agent = None
        allocated_patients = 0
        for agent in agents:
            if agent.get_id() != self.get_id():
                for hospital in agent.hospitals:
                    if not hospital.is_full():
                        hospital_dist = self.manhattan_distance(hospital, emergency)
                        if hospital_dist <= min_distance:
                            min_distance = hospital_dist
                            # min_hospital = hospital
                            min_agent = agent
                            #allocated_patients = hospital.get_slots() - patient_counter

        return min_agent  # allocated_patients

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
            # print("I am hospital", hospital.get_id(), "and I have", hospital.get_slots(), "free slots right now.")
            # print("Patient counter is: ", patient_counter)
            hospital_dist = self.manhattan_distance(hospital, emergency)
            if hospital_dist <= min_distance and not hospital.is_full():
                min_distance = hospital_dist
                min_hospital = hospital
                allocated_patients = hospital.get_slots() - patient_counter

        if min_hospital is None:
            return None

        if allocated_patients >= 0:
            min_hospital.update_curr_capacity(patient_counter)  # TODO can only update when vehicles arrive to emergency
        else:
            min_hospital.update_curr_capacity(min_hospital.get_slots())
            # print("HOSPITALLLLLL ", min_hospital.get_id(), " has ", min_hospital.get_slots(), " free slots")

        return min_hospital, allocated_patients

    def activate_medical_vehicles(self, final_vehicles, eid):
        threads = []
        for vehicle in final_vehicles:
            thread = Thread(target=vehicle.move, args=(eid,))
            thread.start()
            threads.append(thread)

        wait_threads(threads)  # TODO Why is this here. This means that we have to wait to allocate the rest of the vehicles

    ###################
    # Agent's Decision#
    ###################

    # Not considering collaboration between agents yet
    # (When all hospitals don't have enough resources, ask help of another agent)
    def allocate_emergency(self, emergency, patient_counter, patients_dict, helping_v, helped_agent):
        patients = -1
        final_vehicles = []
        min_distance = math.inf
        min_vehicle = None
        patients_per_hosp = []
        min_hospital = []
        possible_ambulances = []
        result = None
        # possible_ambulances[0] tem as ambulancias do min_hospital[0] e o
        # patients_per_hosp[0] tem os pacientes que ficaram no min_hospital[0]

        while patients < 0:
            result = self.check_closest_hospital(emergency, math.inf, patient_counter)
            if result is None:
                print("All hospitals are full and there are still patients to attend.\n"
                      "Will contact nearest zone(s) to ask for help")
                self.failed_alloc_hospital = True
                break
            min_hospital.append(result[0])
            patients = result[1]
            if patients >= 0:
                patients_per_hosp.append(patient_counter)  # when all patients stay in the same hospital
            else:
                patients_per_hosp.append(patient_counter + patients)  # when only some patients stay in the same hospital

        for i in range(len(patients_per_hosp)):
            for j in range(patients_per_hosp[i]):
                for patient in patients_dict.values():
                    if patient.get_e_id() == emergency.get_eid() and patient.get_p_hospital() is None:
                        patient.set_p_hospital(min_hospital[i])
                        break

        for hospital in min_hospital:
            possible_ambulances.append(self.filter_medical_vehicles(emergency, hospital))

        # for i in range(len(patients_per_hosp)):  #debug
        #     print(patients_per_hosp[i], "patients to hospital", i)

        for i in range(len(patients_per_hosp)):
            print(patients_per_hosp[i], "patients are going to be taken to Hospital", min_hospital[i].get_id())
            for j in range(patients_per_hosp[i]):
                # print("Patient number", j)
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
                        min_vehicle.set_help_v(helping_v)
                        final_vehicles.append(min_vehicle)

                    min_distance = math.inf
                    min_vehicle = None

            if len(final_vehicles) == 0:
                print("Error: No vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
            else:
                if len(final_vehicles) == 1 and not helping_v:
                    print("1 vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
                elif len(final_vehicles) > 1 and not helping_v:
                    print(len(final_vehicles), "medical vehicles were allocated to deal with emergency nº", emergency.get_eid(), "\n")
                elif len(final_vehicles) == 1 and helping_v:
                    print("1 vehicle was allocated as backup to help deal with emergency nº", emergency.get_eid(),"from zone", helped_agent.get_id(), "\n")
                    with open('out.txt', 'a') as f:
                        print('+ 1', file=f)
                elif len(final_vehicles) > 1 and helping_v:
                    with open('out.txt', 'a') as f:
                        print('+', len(final_vehicles), file=f)
                    print(len(final_vehicles), "vehicles were allocated as backup to help deal with emergency nº", emergency.get_eid(), "from zone", helped_agent.get_id(), "\n")

                self.activate_medical_vehicles(final_vehicles, emergency.get_eid())

                # TODO when collaboration is done, this can't be here
                for patient in patients_dict.values():
                    if patient.get_e_id() == emergency.get_eid() and patient.get_p_hospital() == min_hospital[i] and not patient.get_checked_in():
                        patient.set_admission_time()

        patient_counter -= len(final_vehicles)
        if patient_counter < 0:
            patient_counter = 0
        elif patient_counter > 0:
            self.failed_alloc_vehicles = True
            print("More vehicles are needed. Will check if there are other zones and, if so, ask for help")  # To also cover the edge case of 1 zone
        return patient_counter, patients_dict, self.failed_alloc_hospital, self.failed_alloc_vehicles
