from datetime import datetime

def get_time_period_of_day():
    """
    returns "morning", "afternoon", "evening" or "night" based on the 
    current time of day. calling it the time 'period'. 
    """
    curr_hour = datetime.today().hour

    if 5 <= curr_hour < 12:
        return "Morning"
    elif 12 <= curr_hour < 17:
        return "Afternoon"
    elif 17 <= curr_hour < 21:
        return "Evening"
    else:
        return "Night"

def get_current_date_time_fmtd():
    """ used to default to the current date. """
    return datetime.today().strftime('%m/%d/%Y')

