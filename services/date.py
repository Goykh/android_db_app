from datetime import datetime
from zoneinfo import ZoneInfo


def convert_tz_and_format(time: datetime, tz: str = "Europe/Prague", format: str = "%d-%m-%Y") -> str:
    """
    Converts the time to the given timezone and format.
    Default values to be used in this app.
    :param time: time to convert
    :param tz: timezone to convert to
    :param format: format to convert to
    :return: str with converted time
    """
    tz = ZoneInfo(tz)
    return time.astimezone(tz).strftime(format)


def get_current_date() -> str:
    """
    Gets the current date and converts the month name
    to czech.
    :return: a string with the day and month
    """
    czech_months = {
        1: "Leden",
        2: "Unor",
        3: "Brezen",
        4: "Duben",
        5: "Kveten",
        6: "Cerven",
        7: "Cervenec",
        8: "Srpen",
        9: "Zari",
        10: "Rijen",
        11: "Listopad",
        12: "Prosinec",
    }
    day = datetime.now().day
    month = czech_months[datetime.now().month]
    return f"{day}-{month}"
