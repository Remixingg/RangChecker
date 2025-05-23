from datetime import datetime

def get_today_date():
    today = datetime.now()
    # return today.strftime("%m/%d/%Y")
    return today.strftime("%A, %d %B %Y")