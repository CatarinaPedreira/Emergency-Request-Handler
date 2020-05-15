import math


def manhattan_distance(a, b):
    return abs(a.get_location()[0] - b.get_location()[0]) + abs(a.get_location()[1] - b.get_location()[1])


def check_availability_vehicle(medical_vehicle, min_medicine, min_fuel):
    return medical_vehicle.check_vehicle_status() == "Available" and medical_vehicle.get_fuel() >= min_fuel and medical_vehicle.get_medicine() >= min_medicine


class Agent:
    def __init__(self, area_border, district_map, hospitals, emergencies, cycle_time):
        self.area = area_border
        self.map = district_map
        self.hospitals = hospitals
        self.emergencies = emergencies
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

    def filter_medical_vehicles(self):
        possible_ambulances = []
        for hospital in self.hospitals:
            for medical_vehicle in hospital.medicalVehicles:
                if check_availability_vehicle(medical_vehicle, medical_vehicle.get_min_medicine(), medical_vehicle.get_min_fuel()):
                    possible_ambulances.append(medical_vehicle)

        return possible_ambulances

    def check_closest_hospital(self, emergency, min_distance):
        min_hospital = None
        for hospital in self.hospitals:
            hospital_dist = manhattan_distance(hospital, emergency)
            if hospital_dist < min_distance:
                min_distance = hospital_dist
                min_hospital = hospital

        return min_hospital

    def activate_medical_vehicles(self, final_vehicles):
        for vehicle in final_vehicles:
            vehicle.move(self.cycleTime)

    ###############################
    ###### Agent's Decision #######
    ###############################

    # Not considering collaboration between agents yet
    # (When all hospitals don't have enough resources, ask help of another agent)
    def allocate_emergency(self, emergency):

        id_number = 0
        final_vehicles = []
        min_distance = math.inf
        min_vehicle = None

        min_hospital = self.check_closest_hospital(emergency, math.inf)
        possible_ambulances = self.filter_medical_vehicles()

        for i in range(emergency.get_num_patients()):
            for possibility in possible_ambulances:

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
                possible_ambulances.remove(min_vehicle)
                min_vehicle.change_status("Unavailable")
                min_vehicle.update_work_hours()
                #  min_vehicle.decrease_medicine(emergency.get_gravity(), emergency.get_type())
                min_vehicle.set_em_location(emergency.get_location())
                min_vehicle.set_em_hospital(min_hospital)
                min_vehicle.set_id(id_number)
                id_number += 1
                final_vehicles.append(min_vehicle)

            min_distance = math.inf
            min_vehicle = None

        if len(final_vehicles) == 1:
            print(1, "medical vehicle was allocated to deal with emergency nº", emergency.get_eid(), "\n")
        else:
            print(len(final_vehicles), "medical vehicles were allocated to deal with emergency nº", emergency.get_eid(), "\n")
        self.activate_medical_vehicles(final_vehicles)
