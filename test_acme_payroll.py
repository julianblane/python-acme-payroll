import unittest
from datetime import time
from io import StringIO

from acme_payroll import parse_employee_schedule, parse_employees_schedules_from_txt
from payroll import WeekdayWorkHours


class TestAcmePayroll(unittest.TestCase):
    """test schedules load"""

    def test_parse_employee_schedule(self):
        """successful parse"""
        data_line = 'SUSAN=MO08:00-16:00,TU09:00-18:00,WE15:00-20:00,SA09:00-15:00'
        employee_schedule = parse_employee_schedule(data_line)

        work_hours = [
            WeekdayWorkHours(weekday=0, time_start=time(hour=8), time_end=time(hour=16)),
            WeekdayWorkHours(weekday=1, time_start=time(hour=9), time_end=time(hour=18)),
            WeekdayWorkHours(weekday=2, time_start=time(hour=15), time_end=time(hour=20)),
            WeekdayWorkHours(weekday=5, time_start=time(hour=9), time_end=time(hour=15))
        ]

        self.assertEqual('SUSAN', employee_schedule.name)
        for work_period in work_hours:
            self.assertIn(work_period, employee_schedule.work_hours)

    def test_parse_employee_schedule_invalid_format(self):
        """invalid format"""
        data_line = 'JOSEPH=MO08:00-16:00TU09:00-18:00'
        self.assertRaises(ValueError, parse_employee_schedule, data_line=data_line)

    def test_parse_employee_schedule_invalid_day(self):
        """invalid data"""
        data_line = 'JULIAN=LU08:00-16:00,MA09:00-18:00'
        self.assertRaises(ValueError, parse_employee_schedule, data_line=data_line)

    def test_parse_employee_schedule_invalid_time(self):
        """invalid time input"""
        data_line = 'KEVIN=WE10:00-06:00,TH09:00-18:00'
        self.assertRaises(ValueError, parse_employee_schedule, data_line=data_line)

    def test_parse_employee_schedule_invalid_schedule(self):
        """invalid time range"""
        data_line = 'TIFFANY=WE10:00-18:00,WE16:00-20:00'
        self.assertRaises(ValueError, parse_employee_schedule, data_line=data_line)

    def test_parse_employees_schedules_from_txt_success(self):
        """load txt"""
        file_data = StringIO('NORM=FR17:00-21:00,SA17:00-22:00\nLARRY=TH06:00-08:00,TH19:00-21:00')

        schedules_parse = parse_employees_schedules_from_txt(file_data, min_lines=2)

        self.assertEqual(True, any(schedule.name == 'NORM' for schedule in schedules_parse))
        self.assertEqual(True, any(schedule.name == 'LARRY' for schedule in schedules_parse))

    def test_parse_employees_schedules_from_txt_error_not_enough_data(self):
        """load incomplete txt"""
        file_data = StringIO('NORM=FR17:00-21:00,SA17:00-22:00\nLARRY=TH06:00-08:00,TH19:00-21:00')
        self.assertRaises(ValueError, parse_employees_schedules_from_txt, file=file_data, min_lines=5)
