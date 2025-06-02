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


def set_current_date_or_format_user_date():
    """
    if the user's date input is empty, use today's date. otherwise format their 
    entered date.
    """
    while True:
        new_date = input(f"Enter Transaction Date "
                               f"(MM/DD/YYYY - can leave blank"
                               f" for today's date): ").strip()
        print("\n\n")

        if new_date == "":
            new_date = get_current_date_time_fmtd()
            break
        try:
            parsed_date = datetime.strptime(new_date, 
                                            "%m/%d/%Y")
            new_date = parsed_date.strftime("%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date format. Please enter the date as MM/DD/YYYY.")

    return new_date
