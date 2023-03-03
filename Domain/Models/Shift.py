class Shift():
    def __init__(self, coverRequirements, nightShift):
        self.coverRequirements = coverRequirements
        self.nightShift = nightShift

    def isNightShift(self):
        return self.nightShift