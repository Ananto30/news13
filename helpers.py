from datetime import datetime

import pytz


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """

    now = datetime.now(pytz.utc)
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "এই মাত্র"
        if second_diff < 60:
            return bangla_number(str(round(second_diff))) + " সেকেন্ড আগে"
        if second_diff < 120:
            return "১ মিনিট আগে"
        if second_diff < 3600:
            return bangla_number(str(round(second_diff / 60))) + " মিনিট আগে"
        if second_diff < 7200:
            return "১ ঘন্টা আগে"
        if second_diff < 86400:
            return bangla_number(str(round(second_diff / 3600))) + " ঘন্টা আগে"
    if day_diff == 1:
        return "গতকাল"
    if day_diff < 7:
        return bangla_number(str(round(day_diff))) + " দিন আগে"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def bangla_number(string):
    number_map = {
        "0": "০",
        "1": "১",
        "2": "২",
        "3": "৩",
        "4": "৪",
        "5": "৫",
        "6": "৬",
        "7": "৭",
        "8": "৮",
        "9": "৯",
    }

    return "".join([number_map[s] for s in string])