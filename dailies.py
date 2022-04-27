'''
This program performs the most common and lucrative neopet daily activities.
Run this at least once a day to continue building your account even while you're
too busy being an adult

NOTES:
Does not work with a pin
'''
import asyncio, logging
import login, Constants, web, bank, stocks
import requests, time, timestamp, pickle

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

LOGGER = logging.getLogger('NeopetHelper')

SLEEPTIME = 60 * 60 * 8 # 8 Hours

times = {}

async def main():
    # Login details
    username = ""
    password = ""

    session = requests.Session()

    result = login.login(session, username, password)
    if not result:
        LOGGER.info('Login Falied, next time to try it again, sleeping 180s')
        await asyncio.sleep(180)
        return # next time to login

    login.save_cookies(session)

    global times

    # Opens a pickle file that contains timestamps of when the daily was last performed
    try:
        file = open('times.pkl', 'rb')
    except FileNotFoundError:
        LOGGER.info("Creating file")
        file = open('times.pkl', 'wb')
        file.close()
    else:
        times = pickle.load(file)
        file.close()

    dailies(session)

    LOGGER.info('Work done, sleeping time '+str(SLEEPTIME)+' ... ')
    await asyncio.sleep(SLEEPTIME)

def dailies(session):
    global times
    bank.collectInterest(session, times)
    stocks.buy_stock(session, times)
    trudysSurprise(session)
    shrine(session)
    jelly(session)
    fishing(session)
    omelette(session)
    tdmbgpop(session)
    healingSprings(session)
    adventCalendar(session)
    #sticky(session)
    #tombola(session)
    #fruitMachine(session)

def adventCalendar(session):
    global times

    december = 12

    # Only execute if we're in the month of december
    if int(time.strftime("%m")) == december:
        key = "advent"
        timeExpiry = times.get(key)

        if timeExpiry == None or time.time() > timeExpiry:
            response = web.get(session, Constants.NEO_ADVENT_CALENDAR)

            web.post(session, Constants.NEO_PROCESS_ADVENT, {}, Constants.NEO_ADVENT_CALENDAR)

            LOGGER.info("Collected Advent Calendar")
            times[key] = timestamp.endOfDay()

            file = open('times.pkl', 'wb')
            pickle.dump(times, file)
            file.close()

def trudysSurprise(session):
    global times

    key = "trudy"
    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_TRUDYS)

        postFields = {"action": "beginroll"}
        web.post(session, Constants.NEO_TRUDYS_SPIN, postFields, Constants.NEO_TRUDYS)
        time.sleep(11) # Sleeps because when you spin the wheel you must wait for it to stop before collecting prize

        postFields = {"action": "prizeclaimed"}
        web.post(session, Constants.NEO_TRUDYS_SPIN, postFields, Constants.NEO_TRUDYS)

        LOGGER.info("Spun Trudy's Surprise Wheel")

        times[key] = timestamp.endOfDay()

        file = open('times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def fishing(session):
    global times
    waitTime = 13
    key = "fishing"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_FISHING)
        postFields = {"go_fish": "1"}

        source = web.post(session, Constants.NEO_FISHING, postFields, Constants.NEO_FISHING)

        LOGGER.info("Went Fishing")

        times[key] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

#Tombola might be broken, if not it needs to check if tombola is closed. Otherwise it looks bad and it lags hard.
def tombola(session):
    key = "tombola"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_TOMBOLA)

        postFields = {}
        source = web.post(session, Constants.NEO_TOMBOLA_PLAY, postFields, Constants.NEO_TOMBOLA)

        LOGGER.info("Played Tombola")

        times[key] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def tdmbgpop(session):
    global times
    key = "tdmbgpop"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_TDMBGPOP)
        postFields = {"talkto": "1"}

        source = web.post(session, Constants.NEO_TDMBGPOP, postFields, Constants.NEO_TDMBGPOP)

        LOGGER.info("Visited TDMBGPOP")

        times[key] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def healingSprings(session):
    global times
    waitTime = 0.5
    key = "springs"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_SPRINGS)
        postFields = {"type": "heal"}

        source = web.post(session, Constants.NEO_SPRINGS, postFields, Constants.NEO_SPRINGS)

        LOGGER.info("Went to healing springs")

        times[key] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def sticky(session):
    global times
    waitTime = 0.5
    key = "sticky"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_STICKY, Constants.NEO_SPRINGS)

        LOGGER.info("Got Sticky Snowball")

        times[key] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def omelette(session):
    global times
    key = "omelette"
    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_OMELETTE)
        postFields = {"type": "get_omelette"}

        source = web.post(session, Constants.NEO_OMELETTE, postFields, Constants.NEO_OMELETTE)

        LOGGER.info("Collected an omelette")

        times[key] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def jelly(session):
    global times
    key = "jelly"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_JELLY)
        postFields = {"type": "get_jelly"}

        source = web.post(session, Constants.NEO_JELLY, postFields, Constants.NEO_JELLY)

        LOGGER.info("Collected Jelly")

        times[key] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def fruitMachine(session):
    waitTime = 24
    key = "fruit"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = session.get(Constants.NEO_FRUIT, headers=Constants.HEADERS)

        #This one is tough you need to extract a hidden value from the source
        postFields = {"type": "get_jelly"}
        header = POST.getPostHeader(postFields, Constants.NEO_FRUIT)
        source = session.post(Constants.NEO_FRUIT, postFields, headers=Constants.HEADERS, verify=False).text

        times[key] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

    else:
        LOGGER.info("Already did fruit machine in last 24 hours")

def shrine(session):
    global times
    waitTime = 12
    key = "shrine"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_SHRINE)

        #This one is tough you need to extract a hidden value from the source
        postFields = {"type": "approach"}
        source = web.post(session, Constants.NEO_SHRINE, postFields, Constants.NEO_SHRINE)

        LOGGER.info("Went to shrine")

        times[key] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

if __name__ == "__main__":
    while True:
        asyncio.run(main())        
