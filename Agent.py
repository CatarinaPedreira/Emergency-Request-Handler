class Agent:
    def __init__(self, area_border, district_map, hospitals, emergencies):
        self.area = area_border
        self.map = district_map
        self.hospitals = hospitals
        self.emergencies = emergencies

    def get_area(self):
        return self.area

    def get_map(self):
        return self.map

    def get_hospitals(self):
        return self.hospitals

    def get_emergencies(self):
        return self.emergencies

    def add_emergency(self, emergency):
        self.emergencies.append(emergency)

    def allocate_emergency(self, emergency):

        if emergency.emer_type() == "Life-threatening":

        elif emergency.emer_type() == "Non-life-threatening":

        elif emergency.emer_type() == "Contagious":

        #  Ver ambulancias da zona que estão disponíveis

        for hospital in self.hospitals:
            for medical_vehicle in hospital.medicalVehicles:
                if medical_vehicle == "Life-threatening"





    #  Manhattan distance formula, for (x1,x2) and (y1, y2):
        # |x1 - x2| + |y1 - y2|