'''
This program performs the most common and lucrative neopet daily activities.
Run this at least once a day to continue building your account even while you're
too busy being an adult

NOTES:
Does not work with a pin
'''

import login, Constants, web, bank, stocks
import requests, time, timestamp, pickle

times = {}

def main():
    # Login details
    username = ""
    password = ""

    session = requests.Session()

    login.login(session, username, password)
    login.save_cookies(session)

    global times

    # Opens a pickle file that contains timestamps of when the daily was last performed
    try:
        file = open('times.pkl', 'rb')
    except FileNotFoundError:
        print("Creating file")
        file = open('times.pkl', 'wb')
        file.close()
    else:
        times = pickle.load(file)
        file.close()

    dailies(session)

def dailies(session):
    global times
    bank.collectInterest(session, times)
    stocks.buy_stock(session, times)
    trudysSurprise(session)
    #shrine(session)
    #jelly(session)
    #fishing(session)
    #omelette(session)
    #tdmbgpop(session)
    #healingSprings(session)
    #sticky(session)
    #tombola(session)
    #fruitMachine(session)

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

        print("Spun Trudy's Surprise Wheel")

        times[key] = timestamp.endOfDay()

        file = open('times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def fishing(session):
    waitTime = 13
    dict = "fishing"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_FISHING)
        postFields = {"go_fish": "1"}

        source = web.post(session, Constants.NEO_FISHING, postFields, Constants.NEO_FISHING)

        print("Went Fishing")

        times[dict] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

#Tombola might be broken, if not it needs to check if tombola is closed. Otherwise it looks bad and it lags hard.
def tombola(session):
    dict = "tombola"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_TOMBOLA)

        postFields = {}
        source = web.post(session, Constants.NEO_TOMBOLA_PLAY, postFields, Constants.NEO_TOMBOLA)

        print("Played Tombola")

        times[dict] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def tdmbgpop(session):
    dict = "tdmbgpop"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_TDMBGPOP)
        postFields = {"talkto": "1"}

        source = web.post(session, Constants.NEO_TDMBGPOP, postFields, Constants.NEO_TDMBGPOP)

        print("Visited TDMBGPOP")

        times[dict] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def healingSprings(session):
    waitTime = 0.5
    dict = "springs"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_SPRINGS)
        postFields = {"type": "heal"}

        source = web.post(session, Constants.NEO_SPRINGS, postFields, Constants.NEO_SPRINGS)

        print("Went to healing springs")

        times[dict] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def sticky(session):
    waitTime = 0.5
    dict = "sticky"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_STICKY, Constants.NEO_SPRINGS)

        print("Got Sticky Snowball")

        times[dict] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def omelette(session):
    dict = "omelette"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_OMELETTE)
        postFields = {"type": "get_omelette"}

        source = web.post(session, Constants.NEO_OMELETTE, postFields, Constants.NEO_OMELETTE)

        print("Collected an omelette")

        times[dict] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def jelly(session):
    dict = "jelly"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_JELLY)
        postFields = {"type": "get_jelly"}

        source = web.post(session, Constants.NEO_JELLY, postFields, Constants.NEO_JELLY)

        print("Collected Jelly")

        times[dict] = timestamp.endOfDay()

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

def fruitMachine(session):
    waitTime = 24
    dict = "fruit"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = session.get(Constants.NEO_FRUIT, headers=Constants.HEADERS)

        #This one is tough you need to extract a hidden value from the source
        postFields = {"type": "get_jelly"}
        header = POST.getPostHeader(postFields, Constants.NEO_FRUIT)
        source = session.post(Constants.NEO_FRUIT, postFields, headers=Constants.HEADERS, verify=False).text

        times[dict] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

    else:
        print("Already did fruit machine in last 24 hours")

def shrine(session):
    waitTime = 12
    dict = "shrine"

    file = open(r'times.pkl', 'rb')
    times = pickle.load(file)
    file.close()

    timeExpiry = times.get(dict)

    if timeExpiry == None or time.time() > timeExpiry:
        response = web.get(session, Constants.NEO_SHRINE)

        #This one is tough you need to extract a hidden value from the source
        postFields = {"type": "approach"}
        source = web.post(session, Constants.NEO_SHRINE, postFields, Constants.NEO_SHRINE)

        print("Went to shrine")

        times[dict] = timestamp.getTimestamp(waitTime)

        file = open(r'times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()

if __name__ == "__main__":
    main()
