from datetime import date, datetime, time, timedelta

def next_sunday(d): # gets the date of the next Sunday
    newday = 7 - d.isoweekday() if d.isoweekday() != 7 else 7
    return d + timedelta(days=newday)

def getThisWeek(): # returns a 2-tuple of date objects representing the 1st and last days of this week
    now = date.today()
    if now.isoweekday() == 7:
        begin = now
    else:
        begin = now - timedelta(days=now.isoweekday())
    dates = []
    dates.append(begin)
    for i in range(1, 7):
        dates.append(begin + timedelta(days=i))
    return dates

def getNextWeek(d): # returns a datetime 2-tuple of the first and last days of next week, relative to the input date
    next_begin = next_sunday(d)
    next_end = next_begin + timedelta(days=6)
    return (next_begin, next_end)

def getNextWeekNow():
    return getNextWeek(date.today())

def getDateOffset(d, day): # returns the date next week that corresponds to day
# day: 0 = same day (Sunday), 6 = Saturday
    return d + timedelta(days=day)
