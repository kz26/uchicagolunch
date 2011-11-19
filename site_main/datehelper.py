from datetime import date, datetime, timedelta

def next_sunday(d): # gets the date of the next Sunday
    newday = 7 - d.isoweekday() if d.isoweekday() != 7 else 7
    return date(d.year, d.month, d.day + newday)

def getNextWeek(d): # returns a datetime 2-tuple of the first and last days of next week, relative to the input date
    next_begin = next_sunday(d)
    next_end = next_begin + timedelta(days=6)
    return (next_begin, next_end)

def getRelativeDate(d, day): # returns the date next week that corresponds to day
# day: 0 = same day (Sunday), 6 = Saturday
    nw = getNextWeek(d)
    return (nw + timedelta(days=day))
