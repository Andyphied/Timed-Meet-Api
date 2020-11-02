from datetime import datetime, time, timedelta


def time_plus(time: time, timedelta: timedelta):
    """Helps add timedelta to time

    Args:
        time (time): the time
        timedelta (timedelta): The timedelta

    Returns:
        time: the summed time
    """
    start = datetime(2000,
                     1,
                     1,
                     hour=time.hour,
                     minute=time.minute,
                     second=time.second)
    end = start + timedelta
    return end.time()


def time_subtract(time: time, timedelta: timedelta):
    """Helps add timedelta to time

    Args:
        time (time): the time
        timedelta (timedelta): The timedelta

    Returns:
        time: the summed time
    """
    start = datetime(2000,
                     1,
                     1,
                     hour=time.hour,
                     minute=time.minute,
                     second=time.second)
    end = start - timedelta
    return end.time()
