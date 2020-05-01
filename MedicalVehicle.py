class MedicalVehicle:
    def __init__(self, type_vehicle, fuel_level, med_counter, status, hospital_base, location):
        self.type_vehicle = type_vehicle
        self.fuel = fuel_level
        self.medicine = med_counter
        self.status = status
        self.hospital_base = hospital_base
        self.hospital_curr = hospital_base
        self.location = location

    def get_type_vehicle(self):
        return self.type_vehicle

    def set_type_vehicle(self, type_vehicle):
        self.type_vehicle = type_vehicle

    def get_fuel(self):
        return self.fuel

    def get_medicine(self):
        return self.medicine

    def get_status(self):
        return self.status

    def get_hospital_base(self):
        return self.hospital_base

    def get_current_hospital(self):
        return self.hospital_curr

    def decrease_fuel(self, amount):
        self.fuel = self.fuel - amount

    def decrease_medicine(self, amount):
        self.medicine = self.medicine - amount

    def change_status(self, status):
        self.status = status

    # In case the vehicle changes zone and is now controlled by another hospital
    def change_hospital(self, current):
        self.hospital_curr = current

    def get_location(self):
        return self.location

    def update_location(self):
        pass
