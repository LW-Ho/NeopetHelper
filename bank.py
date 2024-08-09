import Constants, web
import pickle, time, timestamp
from bs4 import BeautifulSoup

import logging
LOGGER = logging.getLogger('Bank')


#I don't like how this function requires you send the source code of the bank
#It should probably request the bank for itself or be set to private
def getBankBalance(response):
    soup = BeautifulSoup(response, "html.parser")
    tag = soup.find(attrs={'onsubmit' : 'return one_submit();'})
    bankBalance = tag.findChildren("b")[1].string[:-2].strip().replace(",","")
    return int(bankBalance)

def getOnHandBalance(response):
    soup = BeautifulSoup(response, "html.parser")
    # Fixed index out of range
    try:
        tag = soup.findChildren("a", attrs={'id' : 'npanchor'})[0].string
        onHandBalance = tag.replace(",","")
        return int(onHandBalance)
    except:
        return 0

async def deposit(session, amount):
    response = await web.get(session, Constants.NEO_BANK)
    onHandBalance = getOnHandBalance(response)

    #send POST to deposit
    if onHandBalance >= amount and amount != 0:
        postFields = {"type": "deposit", "amount": amount}
        source = await web.post(session, Constants.NEO_BANK_INTEREST, postFields, Constants.NEO_BANK)

    else:
        LOGGER.info("You don't have " + str(amount) + " to deposit!")

    return onHandBalance

async def withdraw(session, amount):

    response = await web.get(session, Constants.NEO_BANK)
    bankBalance = getBankBalance(response)

    #withdraw
    if amount <= bankBalance and amount!=0:
        postFields = {"type": "withdraw", "amount": amount}
        await web.post(session, Constants.NEO_BANK_INTEREST, postFields, Constants.NEO_BANK)
        return True

    #insufficient funds
    else:
        LOGGER.info("Insufficient Funds")
        return False

async def collectInterest(session, times, resultDic:dict = {}):
    key = "interest"

    try:

        timeExpiry = times.get(key)

        if timeExpiry == None or time.time() > timeExpiry:
            #Future edit check if interest has been collected
            #Return interest collected
            await web.get(session, Constants.NEO_BANK, Constants.NEO_HOMEPAGE)

            #send POST to collect interest
            postFields = {"type": "interest"}
            await web.post(session, Constants.NEO_BANK_INTEREST, postFields, Constants.NEO_BANK)

            LOGGER.info("Bank interest collected :)")
            times[key] = timestamp.endOfDay()
            resultDic[key] = {"Bank interest collected :)": "Done"}

            file = open('times.pkl', 'wb')
            pickle.dump(times, file)
            file.close()
    except:
        pass
