import math


class Agent:
    def __init__(self, area_border, district_map, hospitals, emergencies):
        self.area = area_border
        self.map = district_map
        self.hospitals = hospitals
        self.emergencies = emergencies

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

    # Not considering collaboration between agents yet
    def allocate_emergency(self, emergency):

        # Hardcoded values, change them later when we see medicine and fuel better
        min_medicine = 10
        min_fuel = 5
        min_distance = math.inf
        min_hospital = None
        possible_ambulances = []

        #  Filter the available ambulances and if they are suitable for that emergency
        for hospital in self.hospitals:
            hospital_dist = abs(hospital.get_location()[0] - emergency.get_location()[0]) + abs(hospital.get_location()[1] - emergency.get_location()[1])
            if hospital_dist < min_distance:
                min_distance = hospital_dist
                min_hospital = hospital

            for medical_vehicle in hospital.medicalVehicles:
                if medical_vehicle.get_status() == "Available" \
                        and medical_vehicle.get_fuel() >= min_fuel \
                        and medical_vehicle.get_medicine() >= min_medicine:
                    possible_ambulances.append(medical_vehicle)

        # Filter which ambulances are closer to the emergency, and correspond to the emergency's requirements
        final_ambulances = []
        min_distance = math.inf
        min_vehicle = None
        for i in range(emergency.get_num_patients()):
            for possibility in possible_ambulances:
                if emergency.get_type() == "Non life-threatening" and emergency.get_type_vehicle()[0] == possibility.get_type_vehicle() \
                        or emergency.get_type_vehicle()[i] == possibility.get_type_vehicle():
                    manhattan_dist = abs(possibility.get_location()[0] - emergency.get_location()[0]) + abs(possibility.get_location()[1] - emergency.get_location()[1])
                    if manhattan_dist < min_distance:
                        min_distance = manhattan_dist
                        min_vehicle = possibility

            if min_vehicle is not None:
                possible_ambulances.remove(min_vehicle)
                final_ambulances.append(min_vehicle)

        return final_ambulances, min_hospital
