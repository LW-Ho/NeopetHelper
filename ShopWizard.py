import Constants, web, re, timestamp, time
from bs4 import BeautifulSoup
from Shop import Shop, ShopItem

class ShopWizard:
    def __init__(self, session):
        self.session = session
        self.searches = 0
        self.__shopwizard_ban = False
        self.__shopwizard_ban_time = None
        self.__shopwizard_ban_duration_min = 0
        self.__does_not_exist = False

    def __search(self, item, max_searches, criteria="exact", min_price = 0, max_price = 999999):
        new_search = ItemSearch(item)
        for i in range(max_searches):
            self.searches+=1
            if self.__shopwizard_ban == False:
                referer = "http://www.neopets.com/market.phtml?type=wizard"
                postFields = {"type": "process_wizard",
                            "feedset": 0,
                            "shopwizard": item,
                            "table": "shop",
                            "criteria": criteria,
                            "min_price": min_price,
                            "max_price": max_price}

                search_results_page_source = web.post(self.session, Constants.NEO_SHOP_WIZARD, postFields, referer)
                self.__check_shopwizard_ban(search_results_page_source)
                new_search.add_shops(self.__parse_search(search_results_page_source, item))

        return new_search

    def __parse_search(self, source, item):
        soup = BeautifulSoup(source , "html.parser")
        search_results = []
        table_index = 2

        #Scrapes all the data from the table within the page source
        try:
            table_of_shops = soup.find_all("table")[table_index]
            prices = table_of_shops.find_all("td", {"align": "right", "bgcolor":re.compile("^#F")}) # All prices
            quantities = table_of_shops.find_all("td", {"align": "center", "bgcolor":re.compile("^#F")}) # all quanitities
            shop_owners = table_of_shops.find_all("a", {'href':re.compile('^/browseshop.phtml?')})
            shop_links = table_of_shops.find_all("a", {'href':re.compile('^/browseshop.phtml?')}) #Gives all anchors
        except:
            print("Error in __parse_search function : could not scrape search results")

        for x in range(len(shop_owners)):
            search_results.append(SearchResult(shop_owners[x].getText(), int(quantities[x].getText()), int(prices[x].getText()[:-3].replace(",","")), shop_links[x]["href"]))

        return search_results

    def __check_shopwizard_ban(self, source):
        if "too many searches!" in source:
            self.__shopwizard_ban = True
            self.__shopwizard_ban_time = timestamp.end_of_hour()
            self.__shopwizard_ban_duration_min = timestamp.timeRemaining(self.__shopwizard_ban_time)
            print("ShopWizard banned for " + str(self.__shopwizard_ban_duration_min) + " minutes.")
            print("Total of", self.searches, "searches before ban.")

    def __send_purchase_request(self, Item_Search):
        referer = "http://www.neopets.com" + Item_Search.cheapest_result().shop_link
        buy_link = Constants.NEO_HOMEPAGE + Item_Search.cheapest_result().shop.shop_items[0].buy_link
        source = web.get(self.session, buy_link, referer)

        Item_Search.decrease_shop_quantity()

    def super_shopwizard_search(self, item):
        print("------------- SSW for", item, "---------------")
        self.market_price(item, max_searches = 200, shops_to_display = 15, ssw=True)

    def market_price(self, item, max_searches = 10, shops_to_display = 10, ssw=False):
        #Improvements for this method include average price across different subsets
        #Number of items available give idea of scarcity
        #Add variance in price.
        searches = 0
        Item_Search = ItemSearch(item)

        while Item_Search.search_completed() < 13 and searches < max_searches:
            search = self.__search(item, 1)
            searches += 1

            if search.search_results == 0 and ssw:
                print("Complete search not possible - defaulting to 100 searches")
                ssw = False
                max_searches = 100
            else:
                Item_Search.add_shops(search.search_results)

        if len(Item_Search.search_results) < shops_to_display:
            shops_to_display = len(Item_Search.search_results)

        for x in range(shops_to_display):
            print(Item_Search.search_results[x])

        print(searches, "total searches.")
        return Item_Search

    def buy(self, item, quantity = 1, max_searches = 10):
        prices_paid = []

        Item_Search = self.__search(item, max_searches)

        if Item_Search.cheapest_result() != None and self.__shopwizard_ban != True:
            for i in range(quantity):
                self.__open_shop(Item_Search)
                price = Item_Search.cheapest_result().shop.shop_items[0].price
                self.__send_purchase_request(Item_Search)
                prices_paid.append(price)

        return prices_paid

    '''
    Sends a GET request to navigate to the shop with the cheapest priced item.
    '''
    def __open_shop(self, Item_Search):
        if Item_Search.cheapest_result() is not None:
            response = web.get(self.session, Constants.NEO_HOMEPAGE + Item_Search.cheapest_result().shop_link)

            while "Sorry - The owner of this shop has been frozen!" in response:
                print("Shop Frozen")
                Item_Search.remove_shop()
                response = web.get(self.session, Constants.NEO_HOMEPAGE + Item_Search.cheapest_result().shop_link)

            Item_Search.cheapest_result().add_shop_details(response, self.session)

class ItemSearch:
    def __init__(self, search_item):
        self.search_item = search_item
        self.search_results = [] #List of search result objects (shop owners) selling the search_item
        self.search_groups = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.users_group_index = 5 #Need this update dynamically

    def __sort(self):
        self.search_results.sort(key=lambda x: x.price, reverse=False)
        return 0

    def average_price(self):
        average = 0
        count = 0
        for i in range(len(self.search_groups)):
            count+= self.search_groups[i]
        for n in range(count):
            average += self.search_results[n].price

        return average/count

    def search_completed(self):
        count = 0
        for i in range(len(self.search_groups)):
            count+= self.search_groups[i]
        return count

    def cheapest_result_in_group(self):
        if self.search_groups[self.users_group_index] == 0:
            return None
        else:
            for shop in self.search_results:
                if self.get_shop_group(shop.owner) == self.users_group_index:
                    return shop

    def get_object_id(self):
        if len(self.search_results) > 0:
            return self.cheapest_result().obj_id
        else:
            return -1

    def cheapest_result(self):
        if len(self.search_results) == 0:
            return None
        else:
            return self.search_results[0]

    def remove_shop(self, index = 0):
        if len(self.search_results) > 0:
            self.search_results.pop(index)

    def add_shops(self, shops):
        #Check shop group has been added already
        if len(shops) > 0:
            _group = self.get_shop_group(shops[0].owner)

            if self.search_groups[_group] == 0:
                self.search_results.extend(shops)
                self.search_groups[_group] = 1
                self.__sort()
                return True

        return False

    def decrease_shop_quantity(self):
        self.search_results[0].stock-= 1

        if self.search_results[0].stock <= 0:
            self.search_results.pop(0)

    def get_shop_group(self, owner):
        _group = ord(owner[0])

        if _group == 95:
            _group = 10
        elif _group < 58:
            _group = _group % 48
        else:
            _group = (_group % 97) % 13
        return _group

    def __str__(self):
        s = str(self.search_groups)
        for shop in self.search_results:
            s = s + "\n" + str(shop)

        return s

class SearchResult:
    def __init__(self, owner, stock, price, shop_link):
        self.owner = owner
        self.stock = stock
        self.price = price
        self.shop_link = shop_link
        self.obj_id = int(self.shop_link[self.shop_link.find("&buy_obj_info_id=") + len("&buy_obj_info_id=") : self.shop_link.find("&buy_cost_neopoints=")])
        self.shop = None

    def add_shop_details(self, shop_page_source, session):
        self.shop = Shop(shop_page_source, session)

    def __str__(self):
        return self.owner + " " + str(self.stock) + " " + str(self.price)
