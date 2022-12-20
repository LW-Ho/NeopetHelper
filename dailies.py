'''
This program performs the most common and lucrative neopet daily activities.
Run this at least once a day to continue building your account even while you're
too busy being an adult

NOTES:
Does not work with a pin
'''
import asyncio, logging
from random import randrange
import login, Constants, web, bank, stocks
from trainingSchool import TrainingSchool
from ShopWizard import ShopWizard
import requests, time, timestamp, pickle
import gmail
import json

import os
USERNAME        = str(os.environ.get('USERNAME', ''))
PASSWORD        = str(os.environ.get('PASSWORD', ''))
FAIL_RETRY_SECOND   = int(os.environ.get('FAIL_RETRY_SECOND', '3600'))
SUCCESS_NEXT_TIME   = int(os.environ.get('SUCCESS_NEXT_TIME', '3600'))
PET_LAB2_PETNAME = str(os.environ.get('PET_LAB2_PETNAME', ''))
PET_TRAINING_PETNAME = str(os.environ.get('PET_TRAINING_PETNAME', ''))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

LOGGER = logging.getLogger('NeopetHelper')

times = {}
resultDic = {}

async def main():
    # Login details
    username = USERNAME
    password = PASSWORD

    session = requests.Session()

    result = login.login(session, username, password)
    if not result:
        LOGGER.info('Login Falied, send email to notify.') 
        try: 
            gmail.notify('error')
        except:
            LOGGER.error('send email error.')
        LOGGER.info('next time to try it again, sleeping '+str(FAIL_RETRY_SECOND)+'s')
        await asyncio.sleep(FAIL_RETRY_SECOND)
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
        try:
            times = pickle.load(file)
            file.close()
        except Exception as e:
            LOGGER.error(e)

    dailies(session)

    gmail.notify('done', json.dumps(resultDic))

    mins = randrange(600,1200) + SUCCESS_NEXT_TIME
    LOGGER.info('Work done, sleeping time '+str(mins)+' ... ')
    await asyncio.sleep(mins)

def dailies(session):
    global resultDic
    global times
    bank.collectInterest(session, times, resultDic)
    stocks.buy_stock(session, times, resultDic)
    trudysSurprise(session)
    # shrine(session)
    # jelly(session)
    # fishing(session)
    # omelette(session)
    # tdmbgpop(session)
    # healingSprings(session)
    # adventCalendar(session)
    #sticky(session)
    #tombola(session)
    #fruitMachine(session)
    # petlab2(session)
    # islandTraining(session)

def islandTraining(session):
    global resultDic
    global times
    waitTime = 0.5
    key = "islandTraining"
    petName = PET_TRAINING_PETNAME

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry or True:
        try:
            trainingSchool = TrainingSchool(session)
            shopWizard = ShopWizard(session)
            payDoneMessage = []

            # Check pet status
            postFields = {"type" : "complete", "pet_name": petName}
            result = web.post(session, Constants.NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_END, postFields, Constants.NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_STATUS)

            # Choice pet
            postFields = {"type" : "start", "course_type": "Level", "pet_name": petName}
            result = web.post(session, Constants.NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_START, postFields, Constants.NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_COURSES)

            # Check stone(s)
            response = web.get(session, Constants.NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_STATUS)
            codestones = trainingSchool.checkStone(response, petName)

            # Buy stone
            for stone in codestones:
                price = shopWizard.buy(stone, max_searches=5)
                payDoneMessage.append(stone+': '+str(price[0]))

            # Pay Stone
            response = web.get(session, Constants.NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_PAY_STONE+petName)

            resultDic[key] = {petName: payDoneMessage}
            times[key] = timestamp.getTimestamp(waitTime)

            file = open(r'times.pkl', 'wb')
            pickle.dump(times, file)
            file.close()
        except:
            resultDic[key] = {petName: "Fail"}

def petlab2(session):
    global resultDic
    global times
    waitTime = 0.5
    key = "petlab2"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        try:
            response = web.get(session, Constants.NEO_PET_LAB2)

            postFields = {"chosen" : PET_LAB2_PETNAME}
            result = web.post(session, Constants.NEO_PET_LAB2_PROCESS, postFields, Constants.NEO_PET_LAB2)

            LOGGER.info("Pet Lab 2 Done PetName : "+PET_LAB2_PETNAME)
            resultDic[key] = {PET_LAB2_PETNAME: "Done"}

            times[key] = timestamp.getTimestamp(waitTime)

            file = open(r'times.pkl', 'wb')
            pickle.dump(times, file)
            file.close()
        except:
            resultDic[key] = {PET_LAB2_PETNAME: "Fail"}

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
    global resultDic
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
        resultDic[key] = {"Spun Trudy's Surprise Wheel": "Done"}

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
    global resultDic
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
        resultDic[key] = {"Went to healing springs": "Done"}

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
