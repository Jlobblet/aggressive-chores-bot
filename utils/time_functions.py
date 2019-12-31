from datetime import datetime, timedelta

import regex as re


def date_ISO(time):
    try:
        parsed_time = datetime.strptime(time, "%Y-%m-%d")
        return parsed_time
    except ValueError:
        return None


def date_ISO_no_year(time):
    now = datetime.now()
    try:
        parsed_time = datetime.strptime(time, "%m-%d")
        parsed_time = parsed_time.replace(year=now.year)
        if parsed_time < now:
            parsed_time = parsed_time.replace(year=now.year + 1)
        return parsed_time
    except ValueError:
        return None


def date_british(time):
    try:
        parsed_time = datetime.strptime(time, "%d/%m/%Y")
        return parsed_time
    except ValueError:
        return None


def date_british_no_year(time):
    now = datetime.now()
    try:
        parsed_time = datetime.strptime(time, "%d/%m")
        parsed_time = parsed_time.replace(year=now.year)
        if parsed_time < now:
            parsed_time = parsed_time.replace(year=now.year + 1)
        return parsed_time
    except ValueError:
        return None


def datetime_ISO(time):
    try:
        parsed_time = datetime.strptime(time, "%Y-%m-%d %H:%M")
        return parsed_time
    except ValueError:
        return None


def datetime_ISO_no_year(time):
    now = datetime.now()
    try:
        parsed_time = datetime.strptime(time, "%m-%d %H:%M")
        parsed_time = parsed_time.replace(year=now.year)
        if parsed_time < now:
            parsed_time = parsed_time.replace(year=now.year + 1)
        return parsed_time
    except ValueError:
        return None


def datetime_british(time):
    try:
        parsed_time = datetime.strptime(time, "%H:%M %d/%m/%Y")
        return parsed_time
    except ValueError:
        return None


def datetime_british_no_year(time):
    now = datetime.now()
    try:
        parsed_time = datetime.strptime(time, "%H:%M %d/%m")
        parsed_time = parsed_time.replace(year=now.year)
        if parsed_time < now:
            parsed_time = parsed_time.replace(year=now.year + 1)
        return parsed_time
    except ValueError:
        return None


def time_HMS(time):
    now = datetime.now()
    try:
        parsed_time = datetime.strptime(time, "%H:%M:%S").replace(
            year=now.year, month=now.month, day=now.day
        )
        if parsed_time < now:
            parsed_time += timedelta(days=1)
        return parsed_time
    except ValueError:
        return None


def time_HM(time):
    now = datetime.now()
    try:
        parsed_time = datetime.strptime(time, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if parsed_time < now:
            parsed_time += timedelta(days=1)
        return parsed_time
    except ValueError:
        return None


def time_regex(time):
    now = datetime.now()
    result = re.match(
        r"(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?(?!^)$", time, flags=re.IGNORECASE
    )
    if result:
        parsed_time = now
        if result.group(1):
            parsed_time += timedelta(days=int(result.group(1)[:-1]))
        if result.group(2):
            parsed_time += timedelta(hours=int(result.group(2)[:-1]))
        if result.group(3):
            parsed_time += timedelta(minutes=int(result.group(3)[:-1]))
        if result.group(4):
            parsed_time += timedelta(seconds=int(result.group(4)[:-1]))
        return parsed_time


time_functions = (
    date_ISO,
    date_ISO_no_year,
    date_british,
    date_british_no_year,
    datetime_ISO,
    datetime_ISO_no_year,
    datetime_british,
    datetime_british_no_year,
    time_HMS,
    time_HM,
    time_regex,
)
