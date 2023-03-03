class Schedule():
    def __init__(self, shifts, nurses):
        if len(shifts) != 21:
            raise Exception("Must be exactly 21 shifts")

        self.shifts = shifts
        self.nurses = nurses
