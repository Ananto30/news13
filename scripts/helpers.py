from datetime import datetime, timedelta

from scripts.models import News


def print_headlines(news_list: list[News]):
    """
    Print news headlines
    """
    print(f"সর্বশেষ খবর - {len(news_list)} টি")
    print("=" * 50)
    for news in news_list:
        print(f"{news.title} - {pretty_date(news.published_time.timestamp())}")
        print(f"{news.summary}")
        print(f"বিস্তারিত: {news.link}")
        print("-" * 50)


def pretty_date(time):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.utcnow()

    if isinstance(time, int):
        time_diff = now - datetime.utcfromtimestamp(time)
    elif isinstance(time, datetime):
        time_diff = now - time
    else:
        time_diff = now - now

    day_diff = time_diff.days
    ret = ""

    if day_diff < 0:
        ret = ""
    elif day_diff == 0:
        ret = _last_24_hours_date(time_diff)
    elif day_diff == 1:
        ret = "গতকাল"
    elif day_diff < 7:
        ret = _bangla_number(str(round(day_diff))) + " দিন আগে"
    elif day_diff < 31:
        ret = _bangla_number(str(round(day_diff / 7))) + " সপ্তাহ আগে"
    elif day_diff < 365:
        ret = _bangla_number(str(round(day_diff / 30))) + " মাস আগে"
    elif day_diff >= 365:
        ret = _bangla_number(str(round(day_diff / 365))) + " বছর আগে"

    return ret


def _last_24_hours_date(time_diff: timedelta) -> str:
    second_diff = time_diff.seconds
    ret = ""
    if second_diff < 10:
        ret = "এই মাত্র"
    elif second_diff < 60:
        ret = _bangla_number(str(round(second_diff))) + " সেকেন্ড আগে"
    elif second_diff < 120:
        ret = "১ মিনিট আগে"
    elif second_diff < 3600:
        ret = _bangla_number(str(round(second_diff / 60))) + " মিনিট আগে"
    elif second_diff < 7200:
        ret = "১ ঘন্টা আগে"
    elif second_diff < 86400:
        ret = _bangla_number(str(round(second_diff / 3600))) + " ঘন্টা আগে"
    else:
        ret = "গত ২৪ ঘন্টা"

    return ret


def _bangla_number(string):
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
