import datetime


class Emergency:

    def __init__(self, e_id, location, emer_type, num_patients, gravity, type_vehicle):
        # Maybe change date later
        self.e_id = e_id
        self.location = location    # tuple (x,y)
        self.type = emer_type
        self.numPatients = num_patients
        self.gravity = gravity
        self.typeVehicle = type_vehicle     # is tuple with one or multiple vehicles
        self.controlTower = None

    def __repr__(self):
        return "Emergency Id: " + str(self.e_id) + "\nType: " + str(self.type) + "\nLocation: " + str(self.location) + "\nPatients: " + str(self.numPatients) + "\nType of vehicles: " + str(self.typeVehicle)

    def get_eid(self):
        return self.e_id

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

    def set_control_tower(self, tower):
        self.controlTower = tower

    def get_control_tower(self):
        return self.controlTower
