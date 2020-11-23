import Constants, web
import pickle, time, timestamp
from bs4 import BeautifulSoup

#I don't like how this function requires you send the source code of the bank
#It should probably request the bank for itself or be set to private
def getBankBalance(response):
    soup = BeautifulSoup(response, "html.parser")
    tag = soup.find(attrs={'onsubmit' : 'return one_submit();'})
    bankBalance = tag.findChildren("b")[1].string[:-2].strip().replace(",","")
    return int(bankBalance)

def getOnHandBalance(response):
    soup = BeautifulSoup(response, "html.parser")
    tag = soup.findChildren("a", attrs={'id' : 'npanchor'})[0].string
    onHandBalance = tag.replace(",","")
    return int(onHandBalance)

def deposit(session, amount):
    response = web.get(session, Constants.NEO_BANK)
    onHandBalance = getOnHandBalance(response)

    #send POST to deposit
    if onHandBalance >= amount and amount != 0:
        postFields = {"type": "deposit", "amount": amount}
        source = web.post(session, Constants.NEO_BANK_INTEREST, postFields, Constants.NEO_BANK)

    else:
        print("You don't have " + str(amount) + " to deposit!")

    return onHandBalance

def withdraw(session, amount):

    response = web.get(session, Constants.NEO_BANK)
    bankBalance = getBankBalance(response)

    #withdraw
    if amount <= bankBalance and amount!=0:
        postFields = {"type": "withdraw", "amount": amount}
        web.post(session, Constants.NEO_BANK_INTEREST, postFields, Constants.NEO_BANK)
        return True

    #insufficient funds
    else:
        print("Insufficient Funds")
        return False

def collectInterest(session, times):
    key = "interest"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:
        #Future edit check if interest has been collected
        #Return interest collected
        web.get(session, Constants.NEO_BANK, Constants.NEO_HOMEPAGE)

        #send POST to collect interest
        postFields = {"type": "interest"}
        web.post(session, Constants.NEO_BANK_INTEREST, postFields, Constants.NEO_BANK)

        print("Bank interest collected :)")
        times[key] = timestamp.endOfDay()

        file = open('times.pkl', 'wb')
        pickle.dump(times, file)
        file.close()
