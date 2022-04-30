from datetime import time


class DayRange:
    """Weekday range"""

    def __init__(self, weekday_start: int, weekday_end: int):
        pass


class WorkHours:
    """Time range"""

    def __init__(self, time_start, time_end):
        pass


class WeekdayWorkHours(WorkHours):
    """Work schedule defined by day and time range"""

    def __init__(self, weekday, time_start, time_end):
        super().__init__(time_start, time_end)
        pass


class WorkHoursWage(WorkHours):
    """Wage for a time range"""

    def __init__(self, time_start: time, time_end: time, amount: int):
        super().__init__(time_start, time_end)
        pass

    def get_wage(self, time_start: time, time_end: time) -> int:
        """
        calculates amount of money based off of supplied schedule
        :param time_start: schedule start
        :param time_end: schedule end
        :return: amount of money
        """
        pass


class PayRate:
    """Hourly wages in day range"""

    def __init__(self, day_range: DayRange, hourly_wages: list[WorkHoursWage]):
        pass

    def calculate_salary(self, schedule: WeekdayWorkHours) -> int:
        """
        calculate salary for supplied schedule
        :param schedule: worked days and hours
        :return: amount of money
        """
        pass


class EmployeeSchedule:
    """Individual employee worked hours"""

    def __init__(self, name: str, work_hours: list[WeekdayWorkHours]):
        pass


class Payroll:
    """Payrates and employee schedules"""

    def __init__(self, rates: list[PayRate]):
        pass

    def add_employee_schedule(self, schedule: EmployeeSchedule):
        pass

    def get_employees_payroll(self) -> tuple[tuple[str, int], ...]:
        """
        calculates employees salaries
        :returns: tuple of employee-salary tuples
        """
        pass
