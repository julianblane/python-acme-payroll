from datetime import time, timedelta, datetime


class DayRange:
    """Weekday range"""

    def __init__(self, weekday_start: int, weekday_end: int):
        """
        weekday range, 0 = monday, 6 = sunday

        :param weekday_start: inclusive
        :param weekday_end: inclusive
        """
        if weekday_start not in range(0, 7):
            raise ValueError('weekday_start out of range 0-6')
        if weekday_end not in range(0, 7):
            raise ValueError('weekday_end out of range 0-6')
        if weekday_end < weekday_start:
            raise ValueError("weekday_start can't be grater than weekday_end")

        self.weekday_start = weekday_start
        self.weekday_end = weekday_end

    def contains(self, weekday):
        """
        check if the day range contains a certain week day

        :param weekday: day of the week
        :return: is it contained by the range
        """
        return weekday in range(self.weekday_start, self.weekday_end + 1)


class WorkHours:
    """Time range"""

    def __init__(self, time_start, time_end):
        """
        time range defined by start and end
        :param time_start: time start inclusive
        :param time_end: time end inclusive
        """
        if time_start == time(hour=0, minute=1):
            # shift a minute back to consider day starts at 00:00
            time_start = time(hour=0, minute=0)

        if time_end == time(hour=0, minute=0):
            # shift a minute back to keep time in a single day
            time_end = time(hour=23, minute=59)

        if time_start > time_end:
            raise ValueError("time_start can't be grater than time_end")

        self.time_start = time_start
        self.time_end = time_end


class WeekdayWorkHours(WorkHours):
    """Work schedule defined by day and time range"""

    def __init__(self, weekday: int, time_start: time, time_end: time):
        """
        Define work hours through weekday, and time range

        :param weekday: day of the week, 0 - monday, 6 - sunday
        :param time_start: time of day inclusive
        :param time_end: time of day inclusive
        """
        super().__init__(time_start, time_end)
        if weekday not in range(0, 7):
            raise ValueError('weekday out of the range 0 - 6')

        self.weekday = weekday


class WorkHoursWage(WorkHours):
    """Wage for a time range"""

    def __init__(self, time_start: time, time_end: time, amount: int):
        """
        Wage in a determinate time range

        :param time_start: start time, inclusive
        :param time_end: end time, inclusive
        :param amount: wage in usd dollars
        """
        super().__init__(time_start, time_end)

        if amount < 0:
            raise ValueError("amount can't be less than 0")

        self.amount = amount

    def get_wage(self, time_start: time, time_end: time) -> int:
        """
        calculates amount of money based off of supplied schedule

        :param time_start: schedule start
        :param time_end: schedule end
        :return: amount of money
        """
        if time_end == time(hour=0, minute=0):
            # shift 1 minute back to keep time in same day
            time_end = time(hour=23, minute=59)
        if time_start > time_end:
            raise ValueError("Invalid time range")

        hours_worked = 0
        if time_end > self.time_start and time_start < self.time_end:
            clamp_time_start = datetime.combine(datetime.today(), max(self.time_start, time_start))
            clamp_time_end = datetime.combine(datetime.today(), min(self.time_end, time_end))

            # add an extra minute to account for schedules ending at midnight
            seconds_worked = (clamp_time_end - clamp_time_start).seconds + 60
            hours_worked = int(seconds_worked / 3600)

        return hours_worked * self.amount


class PayRate:
    """Hourly wages in day range"""

    def __init__(self, day_range: DayRange, hourly_wages: list[WorkHoursWage]):
        """
        Create payrate defined by dayrange and hourly wages in those days

        :param day_range: positive dayrange
        :param hourly_wages: wages per hour covering all 24hs
        """

        # order hourly wages
        hourly_wages.sort(key=lambda hw: hw.time_start)

        # check hourly wages cover 24hs
        last_time = datetime.combine(datetime.today(), time(hour=0, minute=0))

        for hourly_wage in hourly_wages:
            if hourly_wage.time_start > last_time.time():
                raise ValueError(
                    f"hourly wages don't cover all 24hs, missing from {last_time.time()} to {hourly_wage.time_start}"
                )
            # check hourly wage doesn't start before the last one ends
            elif hourly_wage.time_start < last_time.time():
                raise ValueError(
                    f"hourly wages overlap"
                )

            # save end_time adding an extra minute
            last_time = datetime.combine(datetime.today(), hourly_wage.time_end) + timedelta(minutes=1)

        # check schedule ends at 00:00
        if last_time.time() != time(hour=0, minute=0):
            raise ValueError(f"hourly wages don't cover all 24hs, workhours end at {last_time.time()}")

        self.day_range = day_range
        self.hourly_wages = hourly_wages

    def calculate_salary(self, schedule: WeekdayWorkHours) -> int:
        """
        calculate salary for supplied schedule

        :param schedule: worked days and hours
        :return: amount of money
        """
        salary = 0
        if self.day_range.contains(schedule.weekday):
            for hourly_wage in self.hourly_wages:
                salary += hourly_wage.get_wage(schedule.time_start, schedule.time_end)

        return salary


class EmployeeSchedule:
    """Individual employee worked hours"""

    def __init__(self, name: str, work_hours: list[WeekdayWorkHours]):
        """
        Create employee schedule based on worked hours

        :param name: employee name
        :param work_hours: list of worked hours per day
        """
        # sort workhours by day then start time
        work_hours.sort(key=lambda w: (w.weekday, w.time_start))

        # check for overlaps
        for i in range(1, len(work_hours)):
            if work_hours[i - 1].weekday == work_hours[i].weekday:
                if work_hours[i].time_start < work_hours[i - 1].time_end:
                    raise ValueError('schedule has overlapping hours')

        self.name = name
        self.work_hours = work_hours


class Payroll:
    """Payrates and employee schedules"""

    def __init__(self, rates: list[PayRate]):
        """
        Creates payroll defining payrates

        :param rates: list of payrates
        """
        # order rates by weekday
        rates.sort(key=lambda r: r.day_range.weekday_start)

        # check rates cover all 7 days
        last_day = 0
        for rate in rates:
            if last_day != rate.day_range.weekday_start:
                raise ValueError(
                    f'payroll rates are missing days between day {last_day} and {rate.day_range.weekday_start}'
                )
            elif last_day > rate.day_range.weekday_start:
                raise ValueError('payroll rates have overlapping days')

            last_day = rate.day_range.weekday_end + 1

        if last_day != 7:
            raise ValueError('payroll rates are missing days')

        self.rates = rates
        self.employee_schedules = []

    def add_employee_schedule(self, schedule: EmployeeSchedule):
        """
        adds employee schedule to payroll

        :param schedule: employee schedule
        """
        if any([employee.name == schedule.name for employee in self.employee_schedules]):
            raise ValueError('employee already added to payroll')

        self.employee_schedules.append(schedule)

    def get_employees_payroll(self) -> tuple[tuple[str, int], ...]:
        """
        calculates employees salaries

        :returns: tuple of employee-salary tuples
        """
        pass
