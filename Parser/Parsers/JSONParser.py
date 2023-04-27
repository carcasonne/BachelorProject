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

        dynamicContractDays = True

        self.fullTimeContract = None
        self.halfTimeContract = None
        self.pastTimeContract = None
        for jsonContract in nursesJson["contracts"]:
            # The json describes number of shifts to be covered in a month, while we only consider a single week
            days = jsonContract["maximumNumberOfAssignments"] // 4
            nights = days - 1
            contract = Contract(days, nights)

            contract.minConsecutiveDays = jsonContract["minimumNumberOfConsecutiveWorkingDays"]
            contract.maxConsecutiveDays = jsonContract["maximumNumberOfConsecutiveWorkingDays"]
            contract.minConsecutiveDaysOff = jsonContract["minimumNumberOfConsecutiveDaysOff"]
            contract.maxConsecutiveDaysOff = jsonContract["maximumNumberOfConsecutiveDaysOff"]
            completeWeekend = jsonContract["completeWeekends"]

            bWeekend = False if int(completeWeekend) == 0 else True
            contract.completeWeekend = bWeekend

            #contract.completeWeekend = False

            if jsonContract["id"] == "FullTime":
                if not dynamicContractDays:
                    contract.days = 5
                    contract.nights = 4
                self.fullTimeContract = contract
            elif jsonContract["id"] == "PartTime":
                if not dynamicContractDays:
                    contract.days = 4
                    contract.nights = 3
                self.halfTimeContract = contract
            elif jsonContract["id"] == "HalfTime":
                if not dynamicContractDays:
                    contract.days = 3
                    contract.nights = 2
                self.pastTimeContract = contract
            
            print(f"Contract working: {contract.days} days, {contract.nights} nights")

        # Ignored fields are:
            # numberOfWeeks
            # skills
            # shiftTypes (soft constraints?)
            # forbiddenShiftTypeSucessions (hard constraints?)
            # contracts
        for nurse in nursesJson["nurses"]:
            rawId = nurse["id"]
            rawContract = nurse["contract"]
            contract = self.getContract(rawContract)

            rawId = self.getIdAndGrade(rawId)
            grade = rawId[0]
            id = rawId[1]

            nurse = Nurse(id, grade, contract)
            nurses.append(nurse)

        # This looks at the shifts each nurse has requested to not work
        # shiftsOffRequirements =  workdaysJson["shiftOffRequests"]
        shiftsRequirements = workdaysJson["requirements"]
        shiftsDict = {}

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

        # Soft constraints

        history = historyJson
        shiftOfRequests = workdaysJson["shiftOffRequests"]

        for request in shiftOfRequests:
            nurseId = int(request["nurse"].split("_")[1])
            undesiredShifts = nurses[nurseId].undesiredShifts
            day = self.strToDay(request["day"])
            # Manipulates given list undesiredShifts
            self.setUndesiredShifts(request["shiftType"], day, undesiredShifts)
            
        return Schedule(shifts, nurses)
    
    # nurseShifts: # List of 3 lists: Early shifts, late shifts, night shifts
    def setUndesiredShifts(self, shiftReq, day:Days, nurseShifts):
        dayIndex = day.value - 1
        match shiftReq:
            case "Early": 
                nurseShifts[0][dayIndex] = 1
            case "Late":
                nurseShifts[1][dayIndex] = 1
            case "Day":
                nurseShifts[0][dayIndex] = 1
                nurseShifts[1][dayIndex] = 1
            case "Night":
                nurseShifts[2][dayIndex] = 1
            case "Any":
                nurseShifts[0][dayIndex] = 1
                nurseShifts[1][dayIndex] = 1
                nurseShifts[2][dayIndex] = 1
            case _:
                raise ValueError(f'{shiftReq} not recognized')
        
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

    def getContract(self, contractStr):
        match contractStr:
            case "FullTime":
                return self.fullTimeContract
            case "PartTime":
                return self.pastTimeContract
            case "HalfTime":
                return self.halfTimeContract
            case _:
                raise ValueError(f'{contractStr} not recognized')
    
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
