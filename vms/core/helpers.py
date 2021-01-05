import dateutil.parser
from werkzeug.exceptions import BadRequest


def format_date(date):
    return dateutil.parser.isoparse(date).date()


def verify_dates(dates):
    if dates[0].weekday() > 4:
        raise BadRequest("The start date must be not in the weekend")
    if dates[1].weekday() > 4:
        raise BadRequest("The end date must be not in the weekend")
    if dates[0] > dates[1]:
        raise BadRequest("The start date must be earlier than end date")


def get_periods_intersection(period):
    if period[1][0] > period[0][1] or period[0][0] > period[1][1]:
        return None
    else:
        maximum = max(period[0][0], period[1][0])
        minimum = min(period[0][1], period[1][1])
        return [maximum, minimum] if maximum != minimum else [maximum]
