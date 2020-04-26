class Hospital:

    def __init__(self, control_tower, max_capacity, medical_vehicles):
        self.controlTower = control_tower
        self.maxCapacity = max_capacity
        self.medicalVehicles = medical_vehicles
        self.currCapacity = max_capacity

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
