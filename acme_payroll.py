from datetime import time, datetime
import sys
from io import StringIO
from typing import TextIO

from payroll import EmployeeSchedule, WeekdayWorkHours, DayRange, WorkHoursWage, PayRate, Payroll

WEEKDAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
TIME_FORMAT = '%H:%M'


def parse_employee_schedule(data_line: str) -> EmployeeSchedule:
    """
    Parses employee schedule data line into EmployeeSchedule objets

    :param data_line:
    :return: EmployeeSchedule
    """
    try:
        name, schedule = data_line.split('=')
        work_hours_string: list[str] = schedule.split(',')
    except ValueError:
        raise ValueError(f'Invalid employee schedule format: {data_line}')

    work_hours: list[WeekdayWorkHours] = []

    for work_period_string in work_hours_string:
        try:
            try:
                # split schedule into day and time range
                weekday_string = work_period_string[:2]
                time_range_string = work_period_string[2:].strip()
            except IndexError:
                raise ValueError(f'Invalid schedule format: {work_period_string}')

            try:
                # split time range to start and end
                time_start_string, time_end_string = time_range_string.split('-')
            except ValueError:
                raise ValueError(f'Invalid time range: {time_range_string}')

            time_start = datetime.strptime(time_start_string, TIME_FORMAT).time()
            time_end = datetime.strptime(time_end_string, TIME_FORMAT).time()

            try:
                weekday = WEEKDAYS.index(weekday_string)
            except ValueError:
                raise ValueError(f'Invalid day input: {weekday_string}')

            work_hours.append(WeekdayWorkHours(weekday, time_start, time_end))

        except ValueError as ve:
            raise ValueError(f"Error when trying to parse {name}'s schedule - {ve}")

    return EmployeeSchedule(name, work_hours)


def parse_employees_schedules_from_txt(file: TextIO, min_lines: int) -> list[EmployeeSchedule]:
    """
    loads txt and parses each line into an EmployeeSchedule

    :param file: file to load
    :param min_lines: minimum amount of lines expected
    :return: a list of EmployeeSchedules
    """
    data_lines = file.readlines()

    if len(data_lines) < min_lines:
        raise ValueError(f'Insufficient data, supply at least {min_lines} sets of data - supplied {len(data_lines)}')

    employee_schedules = [parse_employee_schedule(data_line) for data_line in data_lines]

    return employee_schedules


def set_up_payroll() -> Payroll:
    """
    inits a complete weekday-weekend payroll

    :return: the payroll
    """
    weekdays = DayRange(0, 4)
    weekend = DayRange(5, 6)

    weekdays_wage = [
        WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=9), amount=25),
        WorkHoursWage(time_start=time(hour=9, minute=1), time_end=time(hour=18), amount=15),
        WorkHoursWage(time_start=time(hour=18, minute=1), time_end=time(), amount=20)
    ]
    weekend_wage = [
        WorkHoursWage(time_start=time(hour=0, minute=1), time_end=time(hour=9), amount=30),
        WorkHoursWage(time_start=time(hour=9, minute=1), time_end=time(hour=18), amount=20),
        WorkHoursWage(time_start=time(hour=18, minute=1), time_end=time(), amount=25)
    ]

    pay_rates = [
        PayRate(day_range=weekdays, hourly_wages=weekdays_wage),
        PayRate(day_range=weekend, hourly_wages=weekend_wage)
    ]

    return Payroll(rates=pay_rates)


def print_payroll_from_file(filename: str):
    """
    parses file into schedules, adds them to payroll and prints it

    :param filename: schedules filename
    """
    # load schedules from file
    try:
        with open(filename, 'r') as data_file:
            schedules = parse_employees_schedules_from_txt(data_file, min_lines=5)
    except FileNotFoundError:
        print(f'File {sys.argv[1]} does not exist')
        return

    payroll = set_up_payroll()

    # add schedules to payroll
    for schedule in schedules:
        payroll.add_employee_schedule(schedule)

    # get salaries
    salaries = payroll.get_employees_payroll()

    # print salaries
    for salary in salaries:
        print(f'The amount to pay {salary[0]} is: {salary[1]} USD')


if __name__ == '__main__':
    try:
        print_payroll_from_file(sys.argv[1])
    except IndexError:
        print('File argument not supplied')
    except ValueError as ve:
        print(f'Error while parsing the input data; {ve}')
