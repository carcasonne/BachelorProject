import unittest

from Domain.Models.Schedule import Schedule


class Test_TabuSchedule(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_init(self):
        schedule = Schedule([])


if __name__ == '__main__':
    unittest.main()
