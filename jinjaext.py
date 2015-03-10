def convertdate(datetime, format='%a-%d-%m-%Y'):
    return datetime.date().strftime(format) 