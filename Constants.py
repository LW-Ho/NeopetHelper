NEO_HOMEPAGE = "https://www.neopets.com/"
NEO_LOGIN = "https://www.neopets.com/login/"
NEO_LOGIN_REQUEST = "https://www.neopets.com/login.phtml"

#INVENTORY
NEO_INVENTORY_QS = "https://www.neopets.com/quickstock.phtml"
NEO_INVENTORY_PROCESS = "https://www.neopets.com/process_quickstock.phtml"
NEO_INVENTORY_R = "https://www.neopets.com/inventory.phtml"

#BANK
NEO_BANK = "https://www.neopets.com/bank.phtml"
NEO_BANK_INTEREST = "https://www.neopets.com/process_bank.phtml"

#STOCK MARKET
STOCK_MARKET_LIST = "https://www.neopets.com/stockmarket.phtml?type=list&full=true"

#DAILIES
NEO_ADVENT_CALENDAR = "https://www.neopets.com/winter/adventcalendar.phtml"
NEO_PROCESS_ADVENT = "https://www.neopets.com/winter/process_adventcalendar.phtml"

NEO_TRUDYS = "https://www.neopets.com/trudys_surprise.phtml?delevent=yes"
NEO_TRUDYS_SPIN = "https://www.neopets.com/trudydaily/ajax/claimprize.php"

NEO_FISHING = "https://www.neopets.com/water/fishing.phtml"

NEO_TOMBOLA = "https://www.neopets.com/island/tombola.phtml"
NEO_TOMBOLA_PLAY = "https://www.neopets.com/island/tombola2.phtml"

NEO_TDMBGPOP = "https://www.neopets.com/faerieland/tdmbgpop.phtml"

NEO_SPRINGS = "https://www.neopets.com/faerieland/springs.phtml"
NEO_STICKY = "https://www.neopets.com/faerieland/process_springs.phtml?obj_info_id=8429"

NEO_OMELETTE = "https://www.neopets.com/prehistoric/omelette.phtml"

NEO_JELLY = "https://www.neopets.com/jelly/jelly.phtml"

NEO_FRUIT = "https://www.neopets.com/desert/fruit/index.phtml"

NEO_SHRINE = "https://www.neopets.com/desert/shrine.phtml"

NEO_STOCKLIST = "https://www.neopets.com/stockmarket.phtml"
NEO_STOCK_BUY_PROCESS = "https://www.neopets.com/process_stockmarket.phtml"
NEO_STOCK_BUY = "https://www.neopets.com/stockmarket.phtml?type=buy&ticker=" #Need to append desired ticker

#Shop wizard
NEO_SHOP_WIZARD = "https://www.neopets.com/market.phtml"

# Mystery Island Training School
NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_START = "https://www.neopets.com/island/process_training.phtml"
NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_END   = "https://www.neopets.com/island/process_training.phtml"
NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_STATUS = "https://www.neopets.com/island/training.phtml?type=status"
NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_COURSES = "https://www.neopets.com/island/training.phtml?type=courses"
NEO_MYSTERY_ISLAND_TRAINING_SCHOOL_PAY_STONE = "https://www.neopets.com/island/process_training.phtml?type=pay&pet_name="

# PetLab
NEO_PET_LAB2 = "https://www.neopets.com/lab2.phtml"
NEO_PET_LAB2_PROCESS = "https://www.neopets.com/process_lab2.phtml"

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
