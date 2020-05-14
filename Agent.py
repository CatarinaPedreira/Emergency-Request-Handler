import math


def manhattan_distance(a, b):
    return abs(a.get_location()[0] - b.get_location()[0]) + abs(a.get_location()[1] - b.get_location()[1])


def check_availability_vehicle(medical_vehicle, min_fuel, min_medicine):
    return medical_vehicle.get_status() == "Available" \
           and medical_vehicle.get_fuel() >= min_fuel \
           and medical_vehicle.get_medicine() >= min_medicine


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

    def available_ambulances(self):
        available = []
        for hosp in self.hospitals:
            for mv in hosp.medicalVehicles:
                if mv.get_status() == "Available":
                    available.append(mv)
        return available

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
            hospital_dist = manhattan_distance(hospital, emergency)
            if hospital_dist < min_distance:
                min_distance = hospital_dist
                min_hospital = hospital

            for medical_vehicle in hospital.medicalVehicles:
                if check_availability_vehicle(medical_vehicle, min_fuel, min_medicine):
                    possible_ambulances.append(medical_vehicle)

        # Filter which ambulances are closer to the emergency, and correspond to the emergency's requirements
        final_ambulances = []
        min_distance = math.inf
        min_vehicle = None
        for i in range(emergency.get_num_patients()):
            for possibility in possible_ambulances:
                if len(emergency.get_type_vehicle()) == 1 and emergency.get_type_vehicle()[0] == possibility.get_type_vehicle() \
                        or len(emergency.get_type_vehicle()) > 1 and emergency.get_type_vehicle()[i] == possibility.get_type_vehicle():
                    manhattan_dist = manhattan_distance(possibility, emergency)
                    if manhattan_dist < min_distance:
                        min_distance = manhattan_dist
                        min_vehicle = possibility

            if min_vehicle is not None:
                possible_ambulances.remove(min_vehicle)
                final_ambulances.append(min_vehicle)

        # Se ja n houver recursos suficientes num hospital ver qual e o 2 mais proximo
        #  Mudar o status de todas as final ambulances para unavailable
        #  Alterar o return para fazer em vez disto fazer set à location da emergencia e do hospital no medical vehicle
        return final_ambulances, min_hospital
