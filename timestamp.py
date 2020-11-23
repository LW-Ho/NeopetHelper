import time
from datetime import datetime, timedelta
from pytz import timezone

def getTimestamp(hoursLater):
    currentTime = time.time()
    secLater = hoursLater*60*60
    timestamp = currentTime + secLater

    return timestamp

def endOfDay():
    neopetsTimezone = timezone('America/Vancouver')
    neopetsCurrentTime = datetime.now(neopetsTimezone)
    #print(neopetsTime.strftime('%Y-%m-%d_%H-%M-%S'))
    midnight = datetime.now(neopetsTimezone).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=24)

    return time.time() + (midnight-neopetsCurrentTime).total_seconds()

def end_of_hour():
    neopetsTimezone = timezone('America/Vancouver')
    neopetsCurrentTime = datetime.now(neopetsTimezone)
    #print(neopetsTime.strftime('%Y-%m-%d_%H-%M-%S'))
    hour = (datetime.now(neopetsTimezone)+ timedelta(hours=1)).replace(minute=4, second=0, microsecond=0)

    return time.time() + (hour-neopetsCurrentTime).total_seconds()

def timeRemaining(clock):
    min_remaning = (clock - time.time())/60
    #print(str(min_remaning) + " min" )
    return int(min_remaning)
