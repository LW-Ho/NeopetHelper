NEO_HOMEPAGE = "http://www.neopets.com/"
NEO_LOGIN = "http://www.neopets.com/login/"
NEO_LOGIN_REQUEST = "http://www.neopets.com/login.phtml"

#INVENTORY
NEO_INVENTORY_QS = "http://www.neopets.com/quickstock.phtml"
NEO_INVENTORY_PROCESS = "http://www.neopets.com/process_quickstock.phtml"
NEO_INVENTORY_R = "http://www.neopets.com/inventory.phtml"

#BANK
NEO_BANK = "http://www.neopets.com/bank.phtml"
NEO_BANK_INTEREST = "http://www.neopets.com/process_bank.phtml"

#STOCK MARKET
STOCK_MARKET_LIST = "http://www.neopets.com/stockmarket.phtml?type=list&full=true"

#DAILIES
NEO_ADVENT_CALENDAR = "http://www.neopets.com/winter/adventcalendar.phtml"
NEO_PROCESS_ADVENT = "http://www.neopets.com/winter/process_adventcalendar.phtml"

NEO_TRUDYS = "http://www.neopets.com/trudys_surprise.phtml?delevent=yes"
NEO_TRUDYS_SPIN = "http://www.neopets.com/trudydaily/ajax/claimprize.php"

NEO_FISHING = "http://www.neopets.com/water/fishing.phtml"

NEO_TOMBOLA = "http://www.neopets.com/island/tombola.phtml"
NEO_TOMBOLA_PLAY = "http://www.neopets.com/island/tombola2.phtml"

NEO_TDMBGPOP = "http://www.neopets.com/faerieland/tdmbgpop.phtml"

NEO_SPRINGS = "http://www.neopets.com/faerieland/springs.phtml"
NEO_STICKY = "http://www.neopets.com/faerieland/process_springs.phtml?obj_info_id=8429"

NEO_OMELETTE = "http://www.neopets.com/prehistoric/omelette.phtml"

NEO_JELLY = "http://www.neopets.com/jelly/jelly.phtml"

NEO_FRUIT = "http://www.neopets.com/desert/fruit/index.phtml"

NEO_SHRINE = "http://www.neopets.com/desert/shrine.phtml"

NEO_STOCKLIST = "http://www.neopets.com/stockmarket.phtml"
NEO_STOCK_BUY_PROCESS = "http://www.neopets.com/process_stockmarket.phtml"
NEO_STOCK_BUY = "http://www.neopets.com/stockmarket.phtml?type=buy&ticker=" #Need to append desired ticker

#Shop wizard
NEO_SHOP_WIZARD = "http://www.neopets.com/market.phtml"

#POST requests
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Upgrade-Insecure-Requests': "1",
        "Host": "www.neopets.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
