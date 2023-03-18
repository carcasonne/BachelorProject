from Domain.Models.Enums.Grade import Grade
from Domain.Models.Enums.Days import Days
from Domain.Models.Enums.ShiftType import ShiftType
from Domain.Models.Enums.Contract import Contract
from Domain.Models.Nurse import Nurse
from Domain.Models.Shift import Shift
from Domain.Models.Schedule import Schedule

import json
from itertools import chain


class JSONParser:
    def parseNRC(self, scenario, example=False):
        historyJson = None
        nursesJson = None
        workdaysJson = None
        try:
            folder = "Example/" if example else "NurseRosteringCompetition/" 
            historyFile = open("Data/" + folder + scenario + "/history.json")
            historyJson = json.load(historyFile)
            nursesFile = open("Data/" + folder + scenario + "/scenario.json")
            nursesJson = json.load(nursesFile)
            workdaysFile = open("Data/" + folder + scenario + "/workdays.json")
            workdaysJson = json.load(workdaysFile)
        except Exception as e:
            raise FileNotFoundError(str(e)) from e
        
        nurses = []
        shifts = []

        # Ignored fields are:
            # id
            # numberOfWeeks
            # skills
            # shiftTypes (soft constraints?)
            # forbiddenShiftTypeSucessions (hard constraints?)
            # contracts
        for nurse in nursesJson["nurses"]:
            rawId = nurse["id"]
            rawContract = nurse["contract"]
            contractDays = self.getContractDays(rawContract)
            contract = Contract(contractDays[0], contractDays[1])

            rawId = self.getIdAndGrade(rawId)
            grade = rawId[0]
            id = rawId[1]

            nurse = Nurse(id, grade, contract)
            nurses.append(nurse)

        # This looks at the shifts each nurse has requested to not work
        # shiftsOffRequirements =  workdaysJson["shiftOffRequests"]

        shiftsRequirements = workdaysJson["requirements"]
        shiftsDict = {}

        # Had trouble making for loops inside dictionary
        for day in Days:
            shiftsDict[day] = {
                ShiftType.EARLY: {
                    Grade.ONE: 0,
                    Grade.TWO: 0,
                    Grade.THREE: 0
                },
                ShiftType.LATE: {
                    Grade.ONE: 0,
                    Grade.TWO: 0,
                    Grade.THREE: 0
                },
                ShiftType.NIGHT: {
                    Grade.ONE: 0,
                    Grade.TWO: 0,
                    Grade.THREE: 0
                },
            }
        
        for i in chain(range(4), range(8,16)):
            skill = shiftsRequirements[i]["skill"]
            grade = self.skillToGrade(skill)
            shiftType = self.indexToShiftType(i)

            for day in shiftsRequirements[i]:
                # Only interested in day requirements
                if(day == "shiftType" or day == "skill"):
                    continue

                dayEnum = self.strToDay(day)

                min = shiftsRequirements[i][day]["minimum"]
                shiftsDict[dayEnum][shiftType][grade] += min
        
        # Special case for the "Day" ShiftType
        for i in range(4,8):
            skill = shiftsRequirements[i]["skill"]
            grade = self.skillToGrade(skill)

            for day in shiftsRequirements[i]:
                # Only interested in day requirements
                if(day == "shiftType" or day == "skill"):
                    continue
                
                dayEnum = self.strToDay(day)

                # Split the day requirements between EARLY and LATE
                # In case of odd number, make it even and add remainder to LATE shift
                min = shiftsRequirements[i][day]["minimum"]
                remainder = 0
                if(min % 2 != 0):
                    min -= 1
                    remainder += 1

                min //= 2
                
                shiftsDict[dayEnum][ShiftType.EARLY][grade] += min
                shiftsDict[dayEnum][ShiftType.LATE][grade] += min + remainder

        for day in Days:
            for shiftType in ShiftType: 
                gradeOne    = shiftsDict[day][shiftType][Grade.ONE]
                gradeTwo    = shiftsDict[day][shiftType][Grade.TWO]
                gradeThree  = shiftsDict[day][shiftType][Grade.THREE]

                # Create shift objects
                # Make cover requirements cumulative
                coverRequirements = {
                    Grade.ONE: gradeOne,
                    Grade.TWO: gradeOne + gradeTwo,
                    Grade.THREE: gradeOne + gradeTwo + gradeThree
                }

                shift = Shift(coverRequirements, shiftType, day)
                shifts.append(shift)

        return Schedule(shifts, nurses)
    
    # Combine caretakers and nurses into the same grade
    # Debatable
    def getIdAndGrade(self, rawId):
        rawId = rawId.split('_')
        grade = rawId[0]
        id = int(rawId[1])

        if grade == "HN":
            grade = Grade.ONE
        elif grade == "NU":
            grade = Grade.TWO
        elif grade == "CT":
            grade = Grade.TWO
        elif grade == "TR":
            grade = Grade.THREE
        return (grade, id)
     
    def skillToGrade(self, skill):
        match skill:
            case "HeadNurse":
                return Grade.ONE
            case "Nurse":
                return Grade.TWO
            case "Caretaker":
                return Grade.TWO
            case "Trainee":
                return Grade.THREE
            case _:
                raise ValueError(f'{skill} not recognized')

    def getContractDays(self, contract):
        match contract:
            case "FullTime":
                return (5,4)
            case "PartTime":
                return (4,3)
            case "HalfTime":
                return (3,2)
            case _:
                raise ValueError(f'{contract} not recognized')
    
    def indexToShiftType(self, i):
        match i:
            case 0 | 1 | 2 | 3:
                return ShiftType.EARLY
            case 8 | 9 | 10 | 11:
                return ShiftType.LATE
            case 12 | 13 | 14 | 15:
                return ShiftType.NIGHT
            case _:
                raise ValueError(f'{i} out of bounds')

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
            raise ValueError("Failed to parse json: " + str(e)) from e


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
            case "monday" | "requirementonmonday":
                return Days.MONDAY
            case "tuesday" | "requirementontuesday":
                return Days.TUESDAY 
            case "wednesday" | "requirementonwednesday":
                return Days.WEDNESDAY
            case "thursday" | "requirementonthursday":
                return Days.THURSDAY
            case "friday" | "requirementonfriday":
                return Days.FRIDAY
            case "saturday" | "requirementonsaturday":
                return Days.SATURDAY
            case "sunday" | "requirementonsunday":
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
