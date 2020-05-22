import random


class Patient:

    def __init__(self, p_id, e_id, e_gravity):
        self.p_id = p_id
        self.e_id = e_id  # para saber que pacientes tem que distribuir nos hospitais de acordo com a emergencia
        self.p_hospital = None
        self.gravity = e_gravity

        self.admission_time = -1  # começa a negativo porque só começa a contar quando chega ao hospital

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

    def set_admission_time(self):
        self.admission_time = random.randint(self.gravity, self.gravity + 10)

    def check_admission_time(self):
        if self.admission_time > 0:
            self.admission_time -= 1
        return self.admission_time
