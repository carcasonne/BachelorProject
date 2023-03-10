from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Nurse import Nurse
from Domain.Models.Shift import Shift
from Domain.Models.Schedule import Schedule

class JSONParser:
    def parse(self, jsonData):
        nurses = []
        shifts = []

        try:
            startDate = jsonData["StartDate"]
            duration = jsonData["DurationWeeks"]

            for rawNurse in jsonData["Nurses"]:
                id = rawNurse["Id"]
                intGrade = rawNurse["Grade"]
                grade = self.intToGrade(intGrade)

                # Snak om hvad der er smartest at implementere ift. kontrakt
                contract = None

                # Preferences bliver bare sprunget over nu

                nurse = Nurse(id, grade, contract)
                nurses.append(nurse)
            
            for days in jsonData["Shifts"]:
                dayName = None
                for name in days:
                    dayName = name
                 
                day = list(days.values())[0]
                for rawShift in day:
                    strShiftType    = rawShift["ShiftType"]
                    noGradeOne      = rawShift["Grade1"]
                    noGradeTwo      = rawShift["Grade2"]
                    noGradeThree    = rawShift["Grade3"]

                    shiftType   = self.strToShiftType(strShiftType)
                    dayType     = self.strToDay(dayName)

                    coverRequirements = {
                        Grade.ONE: noGradeOne,
                        Grade.TWO: noGradeTwo,
                        Grade.THREE: noGradeThree 
                    }

                    shift = Shift(coverRequirements, shiftType, dayType)
                    shifts.append(shift)

            return Schedule(shifts, nurses)
        except Exception as e:
            raise ValueError("Failed to parse json: " + str(e))


    def intToGrade(self, i):
        match i:
            case 1:
                return Grade.ONE
            case 2:
                return Grade.TWO 
            case 3:
                return Grade.THREE
            case _:
                raise ValueError("A grade must be either 1,2, or 3")
    
    def strToDay(self, day):
        day = day.lower()
        match day:
            case "monday":
                return Days.MONDAY
            case "tuesday":
                return Days.TUESDAY 
            case "wednesday":
                return Days.WEDNESDAY
            case "thursday":
                return Days.THURSDAY
            case "friday":
                return Days.FRIDAY
            case "saturday":
                return Days.SATURDAY
            case "sunday":
                return Days.SUNDAY
            case _:
                raise ValueError(f'{day} not recognized as a day')
    
    def strToShiftType(self, shift):
        shift = shift.lower()
        match shift:
            case "early":
                return ShiftType.EARLY
            case "late":
                return ShiftType.LATE 
            case "night":
                return ShiftType.NIGHT
            case _:
                raise ValueError(f'{shift} has to be either early, late, or night')
