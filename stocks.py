import Constants, requests, timestamp, pickle, time, web, re, bank
from bs4 import BeautifulSoup

def __get_cheapest_stock(session):
    min_price = 15 # most users can only buy stocks at 15 or greater although some can at 10
    lowest_price = 20 # lowest priced stock's price
    ticker = None # lowest priced stock' ticker

    # These are indexes and gaps between data in the table used for soup parsing
    current_price_index = 4
    gap = 5

    source = web.get(session, Constants.STOCK_MARKET_LIST)

    soup = BeautifulSoup(source, "html.parser")
    stock_params = soup.find_all("td", {"align": "center", "bgcolor": "#eeeeff"})

    for i in range(0, len(stock_params), gap):
        if int(stock_params[i+3].getText()) < lowest_price and int(stock_params[i+3].getText()) >= min_price:
            lowest_price = int(stock_params[i+3].getText())
            ticker = stock_params[i].getText()

    return ticker, lowest_price #Returns cheapest available stock above or at min_price

def buy_stock(session, times):
    key = "stocks"

    timeExpiry = times.get(key)

    if timeExpiry == None or time.time() > timeExpiry:

        shares = 1000
        ticker, price = __get_cheapest_stock(session)

        if ticker is not None:
            funds = True

            source = web.get(session, Constants.NEO_STOCK_BUY + ticker)
            balance = bank.getOnHandBalance(source)

            # Not enough nps get money from bank
            if balance < shares*price:
                funds = bank.withdraw(session, shares*price - balance)

            # If we have enough then buy the stocks
            if funds:
                soup = BeautifulSoup(source, "html.parser")
                ref = soup.find("input", {"name": "_ref_ck"})["value"]

                postFields = {"_ref_ck": ref, "type": "buy", "ticker_symbol": ticker, "amount_shares": shares}
                web.post(session, Constants.NEO_STOCK_BUY_PROCESS, postFields, Constants.NEO_STOCK_BUY + ticker)
                print("Bought " + str(shares) + " of " + ticker + "!")

                times[key] = timestamp.endOfDay()

                file = open('times.pkl', 'wb')
                pickle.dump(times, file)
                file.close()

        else:
            print("No stocks currently trading below 20np")
            times[key] = timestamp.end_of_hour()

#Unused for the time being
class Stock(object):
  def __init__(self, ticker, name, volume, open, current, change):
      self.ticker = ticker
      self.name = name
      self.volume = volume
      self.open = open
      self.current = current
      self.change = change
