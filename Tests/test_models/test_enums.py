import unittest

from Domain.Models.Enums.Grade import Grade

class TestGrade(unittest.TestCase):
    def test_grade_2_less_than_grade_3(self):
        grade_3 = Grade.THREE
        grade_2 = Grade.TWO
        self.assertLess(grade_2, grade_3)
    
    def test_grade_1_less_than_grade_2(self):
        grade_2 = Grade.TWO
        grade_1 = Grade.ONE
        self.assertLess(grade_1, grade_2)
    
    def test_grade_2_not_less_than_grade_2(self):
        grade_2_1 = Grade.TWO
        grade_2_2 = Grade.TWO
        lessThan = grade_2_1 < grade_2_2
        self.assertFalse(lessThan)
        

if __name__ == '__main__':
    unittest.main()