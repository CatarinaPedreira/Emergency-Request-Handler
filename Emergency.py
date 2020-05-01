import datetime


class Emergency:

    def __init__(self, e_id, location, emer_type, num_patients, gravity, type_vehicle, description):
        # Maybe change date later
        self.e_id = e_id
        self.location = location
        self.type = emer_type
        self.numPatients = num_patients
        self.gravity = gravity
        self.typeVehicle = type_vehicle
        self.description = description

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
