import math


def manhattan_distance(a, b):
    return abs(a.get_location()[0] - b.get_location()[0]) + abs(a.get_location()[1] - b.get_location()[1])


class Agent:
    def __init__(self, area_border, district_map, hospitals, cycle_time):
        self.area = area_border
        self.map = district_map
        self.hospitals = hospitals
        self.emergencies = []
        self.cycleTime = cycle_time

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

    def check_enough_medicine(self, vehicle, emergency):
        return vehicle.get_medicine() > vehicle.medicine_needed(emergency.get_gravity(), emergency.get_type())

    def check_enough_fuel(self, vehicle, emergency, hospital):
        return vehicle.get_fuel() > (manhattan_distance(vehicle, emergency) + manhattan_distance(emergency, hospital))

    def filter_medical_vehicles(self, emergency, min_hospital):
        possible_ambulances = []
        for hospital in self.hospitals:
            for medical_vehicle in hospital.medicalVehicles:
                if medical_vehicle.get_status() == "Available"\
                        and self.check_enough_medicine(medical_vehicle, emergency)\
                        and self.check_enough_fuel(medical_vehicle, emergency, min_hospital):
                    possible_ambulances.append(medical_vehicle)

        return possible_ambulances

    def check_closest_hospital(self, emergency, min_distance, patient_counter):
        min_hospital = None
        allocated_patients = 0
        for hospital in self.hospitals:
            hospital_dist = manhattan_distance(hospital, emergency)
            if hospital_dist < min_distance and not hospital.is_full():
                min_distance = hospital_dist
                min_hospital = hospital
                allocated_patients = hospital.get_slots() - patient_counter

        if allocated_patients >= 0:
            min_hospital.update_curr_capacity(patient_counter)
        else:
            min_hospital.update_curr_capacity(min_hospital.get_slots())

        return min_hospital, allocated_patients

    def activate_medical_vehicles(self, final_vehicles):
        for vehicle in final_vehicles:
            # TODO Maybe create new thread here, before the vehicle moves?
            vehicle.move(self.cycleTime)

    ###################
    # Agent's Decision#
    ###################

    # Not considering collaboration between agents yet
    # (When all hospitals don't have enough resources, ask help of another agent)
    def allocate_emergency(self, emergency, patient_counter):
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
            min_hospital.append(result[0])
            patients = result[1]
            if patients >= 0:
                patients_per_hosp.append(patient_counter)  # quando todos os pacientes ficam no mesmo hospital
            else:
                patients_per_hosp.append(patient_counter + patients)  # quando apenas ficam alguns dos pacientes naquele hospital

        for hospital in min_hospital:
            possible_ambulances.append(self.filter_medical_vehicles(emergency, hospital))

        for i in range(len(patients_per_hosp)):
            if patient_counter == emergency.get_num_patients():
                print(patients_per_hosp[i], "patients are going to be taken to Hospital", min_hospital[i].get_id())
            for j in range(patients_per_hosp[i]):
                for h_possibilities in possible_ambulances:
                    for possibility in h_possibilities:

                        if len(emergency.get_type_vehicle()) == 1 and emergency.get_type_vehicle()[0] == possibility.get_type_vehicle():
                            manhattan_dist = manhattan_distance(possibility, emergency)
                            if manhattan_dist < min_distance:
                                min_distance = manhattan_dist
                                min_vehicle = possibility

                        elif len(emergency.get_type_vehicle()) > 1:
                            for type_v in emergency.get_type_vehicle():
                                if type_v == possibility.get_type_vehicle():
                                    manhattan_dist = manhattan_distance(possibility, emergency)
                                    if manhattan_dist < min_distance:
                                        min_distance = manhattan_dist
                                        min_vehicle = possibility

                    if min_vehicle is not None:
                        h_possibilities.remove(min_vehicle)
                        min_vehicle.decrease_medicine(emergency.get_gravity(), emergency.get_type())
                        min_vehicle.set_em_location(emergency.get_location())
                        min_vehicle.set_em_hospital(min_hospital[i])
                        final_vehicles.append(min_vehicle)

                    min_distance = math.inf
                    min_vehicle = None

            if len(final_vehicles) == 1:
                print("1 medical vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
            else:
                print(len(final_vehicles), "medical vehicles were allocated to deal with emergency nº", emergency.get_eid(), "\n")

            self.activate_medical_vehicles(final_vehicles)
        patient_counter -= len(final_vehicles)
        if patient_counter < 0:
            patient_counter = 0
        return patient_counter
