class Agent:
    def __init__(self, area_border, district_map, hospitals, emergencies):
        self.area = area_border
        self.map = district_map
        self.hospitals = hospitals
        self.emergencies = emergencies

    def add_emergency(self, emergency):
        self.emergencies.append(emergency)

    def allocate_emergency(self, emergency):
        #TODO
        pass
