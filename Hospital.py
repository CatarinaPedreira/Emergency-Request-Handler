class Hospital:

    def __init__(self):
        self.location = ()
        self.controlTower = None
        self.maxCapacity = self.currCapacity = 100
        self.medicalVehicles = []

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
        self.currCapacity = self.currCapacity + amount
