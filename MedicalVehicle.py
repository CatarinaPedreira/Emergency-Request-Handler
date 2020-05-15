import time


def equal_locations(list_location, tuple_location):
    return list_location[0] == tuple_location[0] and list_location[1] == tuple_location[1]


class MedicalVehicle:
    def __init__(self, type_vehicle, fuel_level, med_counter, hospital_base, location, min_medicine, min_fuel):
        self.type_vehicle = type_vehicle
        self.fuel = fuel_level
        self.medicine = med_counter
        self.max_fuel = fuel_level
        self.max_medicine = med_counter
        self.status = "Available"    # (Available, Assigned, Rest, Replenish)
        self.hospital_base = hospital_base
        self.hospital_curr = hospital_base
        self.location = location
        self.minMedicine = min_medicine
        self.minFuel = min_fuel     # maybe big enough para ir de uma ponta a outra da area de controlo
        self.emLocation = None
        self.emHospital = None
        self.workHours = 0
        self.maxHours = 8   # TODO change later, maybe pass as parameter
        self.rest = self.maxHours // 2
        self.id = 0  # Only for the prints

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

    def decrease_medicine(self, amount):    # TODO em vez de amount, receber gravity e type of emergency p/ calculo (gravity de 1-10 e type = 0/1/2) Contas do amount nunca vão puder dar superior ao valor minimo
        # amount = random.randint(type*gravity, type*gravity + 10)
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
        return self.status

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

    def update_work_hours(self):  # should increase by one every time ambulance is assigned to an emergency
        self.workHours += 1

    def get_work_hours(self):
        return self.workHours

    def set_id(self, number):
        self.id = number

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

        self.change_status("Available")
        print(self.type_vehicle, "vehicle", self.id, "safely dropped the patient at the hospital", "\n")

    def replenish(self):
        self.fuel = self.max_fuel
        self.medicine = self.max_medicine
        self.change_status("Available")

