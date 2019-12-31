from utils.time_functions import time_functions


def parse_time(time):
    parsed_time = None
    for func in time_functions:
        parsed_time = func(time)
        if parsed_time:
            break
    return parsed_time
