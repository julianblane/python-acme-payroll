import unittest


class TestAcmePayroll(unittest.TestCase):
    """test schedules load and payroll outputs"""
    def setUp(self) -> None:
        pass

    def test_parse_employee_schedule(self):
        """successful parse"""
        raise NotImplementedError

    def test_parse_employee_schedule_invalid_format(self):
        """invalid format"""
        raise NotImplementedError

    def test_parse_employee_schedule_invalid_day(self):
        """invalid data"""
        raise NotImplementedError

    def test_parse_employee_schedule_invalid_time(self):
        """invalid time input"""
        raise NotImplementedError

    def test_parse_employee_schedule_invalid_schedule(self):
        """invalid time range"""
        raise NotImplementedError

    def test_parse_schedules(self):
        """successful schedules parse"""
        raise NotImplementedError

    def test_parse_schedules_invalid_format(self):
        """invalid schedule input"""
        raise NotImplementedError
