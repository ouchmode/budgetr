from datetime import datetime
import json

def string_to_datetime(date_time):
    format = "%m/%d/%Y"
    datetime_str = datetime.strptime(date_time, format)

    return datetime_str


