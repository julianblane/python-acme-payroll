import unittest
from datetime import time

from payroll import Payroll, PayRate, DayRange, WorkHours, WorkHoursWage, EmployeeSchedule, WeekdayWorkHours


class TestPayroll(unittest.TestCase):
    """Test payroll setup and calculation"""

    def setUp(self) -> None:
        # pay rates creation
        weekdays = DayRange(0, 4)
        weekend = DayRange(5, 6)

        weekdays_wage = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=6, minute=00), amount=15),
            WorkHoursWage(time_start=time(hour=6, minute=1), time_end=time(hour=18, minute=00), amount=10),
            WorkHoursWage(time_start=time(hour=18, minute=1), time_end=time(hour=00, minute=00), amount=15)
        ]
        weekend_wage = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=16, minute=00), amount=25),
            WorkHoursWage(time_start=time(hour=16, minute=1), time_end=time(hour=00, minute=00), amount=20),
        ]

        pay_rates = [
            PayRate(day_range=weekdays, hourly_wages=weekdays_wage),
            PayRate(day_range=weekend, hourly_wages=weekend_wage)
        ]

        self.payroll = Payroll(rates=pay_rates)

        # employee monica schedule
        monica_work_hours = [
            WeekdayWorkHours(weekday=0, time_start=time(hour=16, minute=0), time_end=time(hour=20, minute=00)),
            WeekdayWorkHours(weekday=1, time_start=time(hour=8, minute=0), time_end=time(hour=12, minute=00)),
        ]
        monica_schedule = EmployeeSchedule(name='MONICA', work_hours=monica_work_hours)

        self.payroll.add_employee_schedule(monica_schedule)

        # employee diane schedule
        diane_work_hours = [
            WeekdayWorkHours(weekday=6, time_start=time(hour=10, minute=0), time_end=time(hour=20, minute=00)),
        ]
        diane_schedule = EmployeeSchedule(name='DIANE', work_hours=diane_work_hours)

        self.payroll.add_employee_schedule(diane_schedule)

    def test_add_employee_schedule_success(self):
        """adds a new employee schedule"""
        work_hours = [
            WeekdayWorkHours(weekday=0, time_start=time(hour=8, minute=0), time_end=time(hour=12, minute=00)),
            WeekdayWorkHours(weekday=1, time_start=time(hour=9, minute=0), time_end=time(hour=15, minute=00))
        ]
        schedule = EmployeeSchedule(name='PETER', work_hours=work_hours)

        self.payroll.add_employee_schedule(schedule)

        self.assertIn(schedule, self.payroll.employee_schedules)

    def test_add_employee_schedule_error_duplicate(self):
        """adds an existing employee schedule"""
        schedule = EmployeeSchedule(name='MONICA', work_hours=[])

        self.assertRaises(ValueError, self.payroll.add_employee_schedule, schedule=schedule)

    def test_get_employees_payroll(self):
        payroll_wages = self.payroll.get_employees_payroll()

        self.assertEqual(2, len(payroll_wages))
        self.assertIn(('MONICA', 90), payroll_wages)
        self.assertIn(('DIANE', 230), payroll_wages)


class TestPayrollIncomplete(unittest.TestCase):
    def test_create_error_incomplete(self):
        """incomplete payroll initialization"""
        weekdays = DayRange(0, 5)
        weekdays_wage = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=0, minute=0), amount=15),
        ]

        pay_rates = [
            PayRate(day_range=weekdays, hourly_wages=weekdays_wage)
        ]

        self.assertRaises(ValueError, Payroll, rates=pay_rates)


class TestEmployeeSchedule(unittest.TestCase):
    def test_create_success(self):
        """create employee schedule"""
        work_hours = [
            WeekdayWorkHours(weekday=4, time_start=time(hour=8, minute=0), time_end=time(hour=16, minute=0)),
            WeekdayWorkHours(weekday=5, time_start=time(hour=10, minute=0), time_end=time(hour=19, minute=0)),
        ]
        schedule = EmployeeSchedule('MARTIN', work_hours=work_hours)

        self.assertEqual('MARTIN', schedule.name)
        self.assertEqual(work_hours, schedule.work_hours)

    def test_create_error_overlapping_hours(self):
        """create schedule with overlapping hours"""
        work_hours = [
            WeekdayWorkHours(weekday=1, time_start=time(hour=8, minute=0), time_end=time(hour=15, minute=0)),
            WeekdayWorkHours(weekday=1, time_start=time(hour=14, minute=0), time_end=time(hour=20, minute=0)),
        ]

        self.assertRaises(ValueError, EmployeeSchedule, name='DOUG', work_hours=work_hours)


class TestDayRange(unittest.TestCase):
    """tests dayrange setup"""

    def test_create_success(self):
        """tests day_start < day_end"""
        day_range = DayRange(0, 2)
        self.assertEqual(0, day_range.weekday_start)
        self.assertEqual(2, day_range.weekday_end)

    def test_create_error_negative_day_range(self):
        """tests day_start > day_end"""
        self.assertRaises(ValueError, DayRange, weekday_start=3, weekday_end=2)


class TestWorkHoursCreation(unittest.TestCase):
    """tests workhours initialization"""
    def test_create_edge_case_day_end(self):
        """create workhours that end at midnight"""
        time_start = time(hour=22, minute=0)
        time_end = time(hour=00, minute=0)
        work_hours = WorkHours(
            time_start=time_start,
            time_end=time_end,
        )

        self.assertEqual(time_start, work_hours.time_start)
        # assert time_end gets shifted a minute back
        self.assertEqual(time(hour=23, minute=59), work_hours.time_end)

    def test_create_edge_case_day_start(self):
        """create workhours that start a minute later than midnight"""
        time_start = time(hour=00, minute=1)
        time_end = time(hour=12, minute=0)
        hourly_wage = WorkHours(
            time_start=time_start,
            time_end=time_end,
        )

        # assert the missing minute gets included
        self.assertEqual(time(hour=00, minute=00), hourly_wage.time_start)
        self.assertEqual(time_end, hourly_wage.time_end)

    def test_create_error_invalid_timerange(self):
        """time_start > time_end"""
        time_start = time(hour=19, minute=0)
        time_end = time(hour=14, minute=0)

        self.assertRaises(ValueError, WorkHours, time_start=time_start, time_end=time_end)


class TestWorkHoursWageCreation(unittest.TestCase):
    """tests workhours setup"""

    def test_create_success(self):
        time_start = time(hour=12, minute=0)
        time_end = time(hour=14, minute=0)
        hourly_wage = WorkHoursWage(
            time_start=time_start,
            time_end=time_end,
            amount=30
        )

        self.assertEqual(time_start, hourly_wage.time_start)
        self.assertEqual(time_end, hourly_wage.time_end)
        self.assertEqual(30, hourly_wage.amount)

    def test_create_error_invalid_amount(self):
        """amount < 0"""
        time_start = time(hour=10, minute=0)
        time_end = time(hour=14, minute=0)

        self.assertRaises(ValueError, WorkHoursWage, time_start=time_start, time_end=time_end, amount=-30)


class TestWorkHoursWage(unittest.TestCase):
    """test wage calculation"""

    def setUp(self) -> None:
        self.daytime_wage = WorkHoursWage(time_start=time(hour=9, minute=0), time_end=time(hour=17, minute=0),
                                          amount=15)

    def test_get_wage_45(self):
        wage = self.daytime_wage.get_wage(time_start=time(hour=9, minute=0), time_end=time(hour=12, minute=0))
        self.assertEqual(45, wage)

    def test_get_wage_zero(self):
        wage = self.daytime_wage.get_wage(time_start=time(hour=20, minute=0), time_end=time(hour=20, minute=1))
        self.assertEqual(0, wage)


class TestWeekdayWorkHours(unittest.TestCase):
    """tests work schedules"""

    def test_create_success(self):
        time_start = time(hour=12, minute=0)
        time_end = time(hour=15, minute=0)

        work_hours = WeekdayWorkHours(weekday=1, time_start=time_start, time_end=time_end)

        self.assertEqual(1, work_hours.weekday)
        self.assertEqual(time_start, work_hours.time_start)
        self.assertEqual(time_end, work_hours.time_end)

    def test_create_error_invalid_day(self):
        """invalid day number"""
        time_start = time(hour=12, minute=0)
        time_end = time(hour=15, minute=0)

        self.assertRaises(ValueError, WeekdayWorkHours, weekday=7, time_start=time_start, time_end=time_end)


class TestPayRateCreation(unittest.TestCase):
    """test payrate initialization"""
    def test_create_success(self):
        """successful init"""
        day_range = DayRange(0, 0)
        hourly_wages = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=19, minute=00), amount=20),
            WorkHoursWage(time_start=time(hour=19, minute=1), time_end=time(hour=00, minute=00), amount=15),
        ]

        pay_rate = PayRate(day_range=day_range, hourly_wages=hourly_wages)

        self.assertEqual(day_range, pay_rate.day_range)
        self.assertEqual(hourly_wages, pay_rate.hourly_wages)

    def test_create_overlapping(self):
        """payrate with overlapping hours"""
        day_range = DayRange(0, 0)
        hourly_wages = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=16, minute=00), amount=20),
            WorkHoursWage(time_start=time(hour=8, minute=1), time_end=time(hour=00, minute=00), amount=15),
        ]

        self.assertRaises(ValueError, PayRate, day_range=day_range, hourly_wages=hourly_wages)

    def test_create_incomplete(self):
        """payrate with missing hours"""
        day_range = DayRange(0, 0)
        hourly_wages = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=10, minute=00), amount=20),
            WorkHoursWage(time_start=time(hour=14, minute=1), time_end=time(hour=00, minute=00), amount=15),
        ]

        self.assertRaises(ValueError, PayRate, day_range=day_range, hourly_wages=hourly_wages)


class TestWeekdayPayRates(unittest.TestCase):
    def setUp(self) -> None:
        """setup weekdays PayRate"""
        day_range = DayRange(0, 4)
        hourly_wages = [
            WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=16, minute=00), amount=20),
            WorkHoursWage(time_start=time(hour=16, minute=1), time_end=time(hour=00, minute=00), amount=15),
        ]

        self.weekdays_payrate = PayRate(day_range=day_range, hourly_wages=hourly_wages)

    def test_get_salary_220(self):
        """weekday work hours"""
        schedule = WeekdayWorkHours(weekday=1, time_start=time(hour=8, minute=0), time_end=time(hour=20, minute=0))
        salary = self.weekdays_payrate.calculate_salary(schedule)
        self.assertEqual(220, salary)

    def test_get_salary_zero(self):
        """weekend work hours"""
        schedule = WeekdayWorkHours(weekday=6, time_start=time(hour=8, minute=0), time_end=time(hour=8, minute=1))
        salary = self.weekdays_payrate.calculate_salary(schedule)
        self.assertEqual(0, salary)


if __name__ == '__main__':
    unittest.main()
