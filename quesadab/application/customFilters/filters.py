import datetime

def formatDateTime(value, format="%m-%d-%Y"):
    print type(value)
    return value.strftime(format)
    # return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")