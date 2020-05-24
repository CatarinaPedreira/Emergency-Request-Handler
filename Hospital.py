class Hospital:

    def __init__(self, h_id):
        self.h_id = h_id
        self.location = ()
        self.controlTower = None
        self.maxCapacity = 2
        self.currCapacity = 0
        self.medicalVehicles = []

    def get_id(self):
        return self.h_id

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_control_tower(self):
        return self.controlTower

    def get_max_capacity(self):
        return self.maxCapacity

    def get_medical_vehicles(self):
        return self.medicalVehicles

    def get_curr_capacity(self):
        return self.currCapacity

    def set_control_tower(self, control_tower):
        self.controlTower = control_tower

    def set_medical_vehicles(self, medical_vehicles):
        self.medicalVehicles = medical_vehicles

    def update_curr_capacity(self, amount):
        self.currCapacity += amount

    def is_full(self):
        return self.currCapacity >= self.maxCapacity

    def get_slots(self):
        return self.maxCapacity - self.currCapacity
