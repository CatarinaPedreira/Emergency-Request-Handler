import datetime


class Emergency:

    def __init__(self, control_tower, location, emer_type, num_patients, gravity, type_vehicle, description):
        # Maybe change date later
        self.date = datetime.datetime.now()
        self.controlTower = control_tower
        self.location = location
        self.type = emer_type
        self.numPatients = num_patients
        self.gravity = gravity
        self.typeVehicle = type_vehicle
        self.description = description

    def get_date(self):
        return self.date

    def get_control_tower(self):
        return self.controlTower

    def get_location(self):
        return self.location

    def get_type(self):
        return self.type

    def get_num_patients(self):
        return self.numPatients

    def get_gravity(self):
        return self.gravity

    def get_type_vehicle(self):
        return self.typeVehicle

    def get_description(self):
        return self.description

    def set_control_tower(self, control_tower):
        self.controlTower = control_tower
