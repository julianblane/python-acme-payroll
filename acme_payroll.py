import datetime
import sys
from io import StringIO
from typing import TextIO

from payroll import EmployeeSchedule, WeekdayWorkHours

WEEKDAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
TIME_FORMAT = '%H:%M'


def parse_employee_schedule(data_line: str) -> EmployeeSchedule:
    """
    Parses employee schedule data line into EmployeeSchedule objets

    :param data_line:
    :return: EmployeeSchedule
    """
    name, schedule = data_line.split('=')
    work_hours_string: list[str] = schedule.split(',')
    work_hours: list[WeekdayWorkHours] = []

    for work_hour_string in work_hours_string:
        try:
            # split schedule into day and time range
            weekday_string = work_hour_string[0:2]
            time_range_string = work_hour_string[2:].strip()
        except IndexError:
            raise ValueError(f'Invalid schedule format: {work_hour_string}')

        try:
            # split time range to start and end
            time_start_string, time_end_string = time_range_string.split('-')
        except ValueError:
            raise ValueError(f'Invalid time range: {time_range_string}')

        try:
            time_start = datetime.datetime.strptime(time_start_string, TIME_FORMAT).time()
        except ValueError:
            raise ValueError(f'Invalid time format: {time_start_string}')

        try:
            time_end = datetime.datetime.strptime(time_end_string, TIME_FORMAT).time()
        except ValueError:
            raise ValueError(f'Invalid time format: {time_end_string}')

        try:
            weekday = WEEKDAYS.index(weekday_string)
        except ValueError:
            raise ValueError(f'Invalid day input: {weekday_string}')

        work_hours.append(WeekdayWorkHours(weekday, time_start, time_end))

    return EmployeeSchedule(name, work_hours)


def parse_employees_schedules_from_txt(file: TextIO, min_lines: int):
    data_lines = file.readlines()

    if len(data_lines) < min_lines:
        raise ValueError(f'Insufficient data, supply at least {min_lines} sets of data - supplied {len(data_lines)}')

    return [parse_employee_schedule(data_line) for data_line in data_lines]