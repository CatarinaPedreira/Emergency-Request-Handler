import random


class Patient:

    def __init__(self, p_id, e_id, e_gravity):
        self.p_id = p_id
        self.e_id = e_id  # To know which patients have to be distributed in the hospitals according to the emergency
        self.p_hospital = None
        self.gravity = e_gravity
        self.checked_in = 0

        self.admission_time = -1  # Starts negative because it only starts counting once it reaches the hospital

    def get_p_id(self):
        return self.p_id

    def get_e_id(self):
        return self.e_id

    def set_p_hospital(self, hospital):
        self.p_hospital = hospital

    def get_p_hospital(self):
        return self.p_hospital

    def get_admission_time(self):
        return self.admission_time

    def get_checked_in(self):
        return self.checked_in

    def set_admission_time(self):
        self.admission_time = random.randint(self.gravity * 4, self.gravity * 4 + 10)
        self.checked_in = 1

    def check_admission_time(self):
        if self.admission_time > 0:
            self.admission_time -= 1
        return self.admission_time
