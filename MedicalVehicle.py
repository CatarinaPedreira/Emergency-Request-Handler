class MedicalVehicle:
    def __init__(self, type_vehicle, fuel_level, med_counter, status, hospital_base, location, min_medicine, min_fuel):
        self.type_vehicle = type_vehicle
        self.fuel = fuel_level
        self.medicine = med_counter
        self.status = status
        self.hospital_base = hospital_base
        self.hospital_curr = hospital_base
        self.location = location
        self.minMedicine = min_medicine
        self.minFuel = min_fuel
        self.emLocation = None
        self.emHospital = None
        self.workHours = 0
        self.maxHours = 8 # TODO change later, maybe pass as parameter
        self.rest = self.maxHours // 2

    def get_type_vehicle(self):
        return self.type_vehicle

    def set_type_vehicle(self, type_vehicle):
        self.type_vehicle = type_vehicle

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
        self.fuel = self.fuel - amount

    def decrease_medicine(self, amount): # TODO em vez de amount, receber gravity e type of emergency p/ calculo (gravity de 1-10 e type = 0/1/2)
        # amount = random.randint(type*gravity, type*gravity + 10)
        self.medicine = self.medicine - amount
        # TODO also according to medicine left, status pode ter que ser replenish

    # In case the vehicle changes zone and is now controlled by another hospital
    def change_hospital(self, current):
        self.hospital_curr = current

    def get_status(self):
        return self.status

    def change_status(self, status):
        self.status = status

    def check_vehicle_status(self):
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

    def update_work_hours(self): # should increase by one every time ambulance is assigned to an emergency
        self.workHours += 1

    def get_work_hours(self):
        return self.workHours

    def update_location(self, x, y):
        self.location[0] += x
        self.location[1] += y

    def move(self):
        # Ver como fazer isto c os tiks
        # Vai fazer update à location, 1 a 1, a cada tik
        # Movimentar-se até ao local da emergência
        # Movimentar-se da emergencia até ao hospital de destino
        pass
