import unittest


class TestPayroll(unittest.TestCase):
    """Test payroll setup and calculation"""
    def setUp(self) -> None:
        pass

    def test_setup(self):
        """correct class initialization"""
        raise NotImplementedError

    def test_add_employee_schedule_success(self):
        """adds a new employee schedule"""
        raise NotImplementedError

    def test_add_employee_schedule_error_duplicate(self):
        """adds an existing employee schedule"""
        raise NotImplementedError

    def test_get_employees_payroll(self):
        """employees payroll calculation"""
        raise NotImplementedError


class TestEmployeeSchedule(unittest.TestCase):
    def test_create_success(self):
        """create employee schedule"""
        raise NotImplementedError

    def test_create_error_overlapping_hours(self):
        """create schedule with overlapping hours"""
        raise NotImplementedError


class TestDayRange(unittest.TestCase):
    """ tests dayrange setup """

    def test_create_success(self):
        """tests day_start < day_end"""
        raise NotImplementedError

    def test_create_error_negative_day_range(self):
        """tests day_start > day_end"""
        raise NotImplementedError


class TestWorkHoursWageCreation(unittest.TestCase):
    def test_create_success(self):
        raise NotImplementedError

    def test_create_error_invalid_timerange(self):
        raise NotImplementedError


class TestWorkHoursWage(unittest.TestCase):
    """test wage calculation"""
    def setUp(self) -> None:
        pass

    def get_wage_45(self):
        raise NotImplementedError

    def get_wage_zero(self):
        raise NotImplementedError


class TestWeekdayWorkHours(unittest.TestCase):
    """tests work schedules"""
    def test_create_success(self):
        raise NotImplementedError

    def test_create_error_invalid_day(self):
        """invalid day number"""
        raise NotImplementedError


class TestWeekdayPayRates(unittest.TestCase):
    def setUp(self) -> None:
        """setup weekdays PayRate"""
        pass

    def test_get_salary_220(self):
        """weekday work hours"""
        raise NotImplementedError

    def test_get_salary_zero(self):
        """weekend work hours"""
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
