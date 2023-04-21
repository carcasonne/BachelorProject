import unittest

from Domain.Models.Enums.Contract import Contract
from Domain.Models.Enums.Grade import Grade
from Domain.Models.Nurse import Nurse
from Domain.Models.ShiftPatterns.ShiftPattern import StandardShiftPattern, TabuShiftPattern
from Domain.Models.Tabu.TabuNurse import TabuNurse


class TestNurse(unittest.TestCase):
    def setUp(self) -> None:
        self.n0 = Nurse(0, Grade.ONE, Contract(5, 4))
        self.n1 = Nurse(0, Grade.THREE, Contract(3, 2))

    def tearDown(self) -> None:
        self.n0 = Nurse(0, Grade.ONE, Contract(5, 4))
        self.n1 = Nurse(0, Grade.THREE, Contract(3, 2))

    def test_init_is_assigned_correctly(self):
        self.assertEqual(0, self.n0.id)
        self.assertEqual(Grade.ONE, self.n0.grade)
        self.assertEqual(Contract(5, 4), self.n0.contract)

    def test_assign_shift_pattern_to_n0_assigns_the_correct_pattern(self):
        pattern = StandardShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.n0.assignShiftPattern(pattern)
        self.assertEqual(pattern, self.n0.assignedShiftPattern)

    def test_assign_shift_pattern_with_invalid_amount_of_shifts_per_day_pattern_raises_exception(self):
        pattern = StandardShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        with self.assertRaises(Exception) as context:
            self.n0.assignShiftPattern(pattern)
        self.assertEqual('Nurses can only be assigned to at most one shift per day', str(context.exception))

    def test_assign_shift_pattern_with_invalid_contract_pattern_raises_exception(self):
        pattern = StandardShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        with self.assertRaises(Exception) as context:
            self.n0.assignShiftPattern(pattern)
        self.assertEqual('Shift pattern infeasible according to the contract', str(context.exception))

    def test_calculate_penalty_undesired_shift_returns_10(self):
        self.n0.undesiredShifts = ([1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        pattern = StandardShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(10, self.n0.calculatePenalty(pattern))

    def test_calculate_penalty_undesired_shift_returns_30(self):
        self.n0.undesiredShifts = ([1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1])
        pattern = StandardShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(30, self.n0.calculatePenalty(pattern))

    def test_calculate_penalty_undesired_shift_returns_0(self):
        self.n0.undesiredShifts = ([0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1])
        pattern = StandardShiftPattern([1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(0, self.n0.calculatePenalty(pattern))

    def test_calculate_penalty_consecutive_days_off_returns_0(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDaysOff = 2
        contract.maxConsecutiveDaysOff = 2
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(0, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_consecutive_days_off_returns_30(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDaysOff = 2
        contract.maxConsecutiveDaysOff = 2
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(30, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_consecutive_days_off_returns_60(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDaysOff = 1
        contract.maxConsecutiveDaysOff = 2
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(60, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_consecutive_working_days_returns_30(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDays = 1
        contract.maxConsecutiveDays = 2
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(30, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_consecutive_working_days_returns_150(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDays = 1
        contract.maxConsecutiveDays = 2
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(150, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_complete_weekend_returns_0(self):
        contract = Contract(5, 4)
        contract.completeWeekend = True
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(0, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_complete_weekend_returns_30(self):
        contract = Contract(5, 4)
        contract.completeWeekend = True
        nurse = Nurse(0, Grade.ONE, contract)
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(30, nurse.calculatePenalty(pattern))

    def test_calculate_mixed_constraints_returns_140(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDays = 1
        contract.maxConsecutiveDays = 2
        contract.completeWeekend = True
        nurse = Nurse(0, Grade.ONE, contract)
        nurse.undesiredShifts = ([0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(140, nurse.calculatePenalty(pattern))

    def test_calculate_penalty_on_nurse_is_equal_to_calculate_penalty_on_tabu_nurse(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDays = 2
        contract.maxConsecutiveDays = 2
        contract.completeWeekend = True
        nurse = Nurse(0, Grade.ONE, contract)
        nurse.undesiredShifts = ([0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        pattern = StandardShiftPattern([1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        tabuPattern = TabuShiftPattern([1, 1, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        tabuNurse = TabuNurse(nurse)
        self.assertEqual(tabuNurse.calculatePenalty(tabuPattern), nurse.calculatePenalty(pattern))

    def test_calculate_penalty_on_nurse_not_working_undesired_shift_is_less_than_calculate_penalty_on_tabu_nurse(self):
        contract = Contract(5, 4)
        contract.minConsecutiveDays = 2
        contract.maxConsecutiveDays = 2
        contract.completeWeekend = True
        nurse = Nurse(0, Grade.ONE, contract)
        nurse.undesiredShifts = ([0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1])
        pattern = StandardShiftPattern([1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        tabuPattern = TabuShiftPattern([1, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0])
        tabuNurse = TabuNurse(nurse)
        resultTabu = tabuNurse.calculatePenalty(tabuPattern)
        result = nurse.calculatePenalty(pattern)
        self.assertTrue(resultTabu > result)
        self.assertNotEqual(resultTabu, result)





if __name__ == '__main__':
    unittest.main()
