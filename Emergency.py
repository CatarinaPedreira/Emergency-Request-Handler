import datetime


class Emergency:

    def __init__(self, control_tower, location, emer_type, num_patients, gravity, type_vehicle, description):
        # Maybe change this later
        self.date = datetime.datetime.now()
        self.controlTower = control_tower
        self.location = location
        self.type = emer_type
        self.numPatients = num_patients
        self.gravity = gravity
        self.typeVehicle = type_vehicle
        self.description = description
