import time
import random


def equal_locations(list_location, tuple_location):
    return list_location[0] == tuple_location[0] and list_location[1] == tuple_location[1]


class MedicalVehicle:
    def __init__(self, ident, type_vehicle, hospital_base):
        self.id = ident
        self.type_vehicle = type_vehicle
        self.fuel = self.max_fuel = 2000
        self.medicine = self.max_medicine = 200
        self.status = "Available"    # (Available, Assigned, Rest, Replenish)
        self.hospital_base = hospital_base
        self.hospital_curr = hospital_base
        self.location = list(hospital_base.get_location())
        self.minMedicine = 30
        self.minFuel = 200
        self.emLocation = None
        self.emHospital = None
        self.work_km = 0
        self.max_km = 4000
        self.rest = 1000

    def get_type_vehicle(self):
        return self.type_vehicle

    def get_fuel(self):
        return self.fuel

    def get_medicine(self):
        return self.medicine

    def get_hospital_base(self):
        return self.hospital_base

    def get_current_hospital(self):
        return self.hospital_curr

    def get_min_medicine(self):
        return self.minMedicine

    def get_min_fuel(self):
        return self.minFuel

    def decrease_fuel(self, amount):
        self.fuel -= amount
        if self.fuel <= self.minFuel:
            self.change_status("Replenish")

    def decrease_medicine(self, gravity, emer_type):
        # gravity varies on a scale of 1 to 10; type can be LT or non-LT
        if emer_type == "Life-threatening":
            e_type = 2
        else:
            e_type = random.randint(0, 1)

        amount = random.randint(e_type * gravity, e_type * gravity + 10) # medicine needed will be, at max, 30

        self.medicine = self.medicine - amount
        if self.medicine <= self.minMedicine:
            self.change_status("Replenish")

    # In case the vehicle changes zone and is now controlled by another hospital
    def change_hospital(self, current):
        self.hospital_curr = current

    def get_status(self):
        return self.status

    def change_status(self, status):
        self.status = status

    def check_vehicle_status(self):     # TODO nao deveria ser algo chamado a cada tik que fizesse update? Rever como descer o rest
        if self.status == 'Rest':
            if self.rest > 0:
                self.rest -= 1
            else:
                self.status = 'Available'
                self.rest = 1000
                self.work_km = 0

    def get_location(self):
        return self.location

    def get_em_location(self):
        return self.emLocation

    def get_em_hospital(self):
        return self.emHospital

    def set_em_location(self, location):
        self.emLocation = location

    def set_em_hospital(self, hospital):
        self.emHospital = hospital

    def update_work_km(self, amount):
        self.work_km += amount

    def get_work_km(self):
        return self.work_km

    def get_max_km(self):
        return self.max_km

    def get_rest(self):
        return self.rest

    #  Step/Cycle
    def update_location(self, start, dest):
        if start[0] < dest[0]:
            start[0] += 1
        elif start[0] > dest[0]:
            start[0] -= 1
        if start[1] < dest[1]:
            start[1] += 1
        elif start[1] > dest[1]:
            start[1] -= 1

        self.location = start
        self.decrease_fuel(1)
        self.update_work_km(1)

    def move(self, cycle_time):
        self.change_status("Assigned")

        # Move from location to emergency
        while not equal_locations(self.location, self.emLocation):
            self.update_location(self.location, self.emLocation)
            time.sleep(cycle_time / 1000)

        print(self.type_vehicle, "vehicle", self.id, "arrived to the emergency")

        # Move from emergency location to emergency's hospital
        while not equal_locations(self.location, self.emHospital.get_location()):
            self.update_location(self.location, self.emHospital.get_location())
            time.sleep(cycle_time / 1000)

        print(self.type_vehicle, "vehicle", self.id, "safely dropped the patient at the hospital")

        # TODO se move deixar de ser atomico, atualizacao de estado tem que passar para depois da chamada do move
        if self.status == 'Replenish':
            self.replenish()
            print(self.type_vehicle, "vehicle", self.id, "replenished fuel and medicine at the hospital")

        elif self.status == 'Assigned':
            self.change_status('Available')

        if self.work_km >= self.max_km:
            self.change_status('Rest')
            print(self.type_vehicle, "vehicle", self.id, "entered Rest mode")

        print('\n')


    def replenish(self):
        self.fuel = self.max_fuel
        self.medicine = self.max_medicine
        self.change_status("Available")
