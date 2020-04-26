class Hospital:

    def __init__(self, control_tower, max_capacity, medical_vehicles):
        self.controlTower = control_tower
        self.maxCapacity = max_capacity
        self.medicalVehicles = medical_vehicles
        self.currCapacity = 0