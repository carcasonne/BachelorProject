class Nurse():
    def __init__(self, id, grade):
        self.id = id
        self.grade = grade

    def print(self):
        print(str(self.id) + " is of grade: " + self.grade)