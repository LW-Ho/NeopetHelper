'''
These Classes handle all data and actions related to other user's shops.
Main actions include scraping all item data from the shop and purchasing of items
'''

from bs4 import BeautifulSoup
import re, web, Constants
from webbrowser import open_new_tab

class Shop():
    def __init__(self, shop_page_source, session):
        self.session = session
        self.shop_items = Shop.scrape_shop_items(shop_page_source)
        self.owner = self.get_shop_owner(shop_page_source)

    def get_shop_owner(self, shop_page_source):
        soup = BeautifulSoup(shop_page_source, "html.parser")
        owner = soup.find_all("a", {'href':re.compile('^/userlookup.phtml?')})[1].getText()
        return owner

    @staticmethod
    def scrape_shop_items(shop_page_source):
        shop_items = []

        soup = BeautifulSoup(shop_page_source, "html.parser")
        items = soup.find_all("td", {"align":"center", "valign": "top"})

        try:
            if len(items) > 0:
                for item in items:
                    try:
                        buy_link = item.find("a", {'href':re.compile('^buy_item.phtml?')})["href"]
                        obj_id = int(buy_link[buy_link.find("obj_info_id=") + 12: buy_link.find("&g=")])
                        name = item.find("b").getText()
                        quantity = int(item.getText()[item.getText().find(name) + len(name): item.getText().find(" ", item.getText().find(name) + len(name))])
                        price = int(item.getText()[item.getText().find("Cost : ") + 7: item.getText().find(" NP", item.getText().find("Cost : ") + 7)].replace(",",""))
                        shop_items.append(ShopItem(name, price, quantity, obj_id, buy_link))
                    except:
                        pass

        except:
            with open('html.html', 'wb') as file:
                file.write(shop_page_source.encode('utf8'))
            open_new_tab("html.html")
            print("No shop items to be scraped. Why? __scrape_shop_items function")

        return Shop.__remove_duplicate(shop_items)

    @staticmethod
    def __remove_duplicate(list):
        #Often a shop's item list will have a duplicate of the first item in the list
        try:
            duplicate_item = list[0]
            for i in range(1, len(list)):
                if duplicate_item.obj_id == list[i].obj_id:
                    list.remove(list[i])
                    break
        except Exception as e:
            print(e)

        return list

    def __update_shop(self, shop_page_source):
        self.shop_items.clear()
        self.shop_items = Shop.scrape_shop_items(shop_page_source)

    def buy_searched_item(self):
        #This function assumes you searched for a particular item and so that item will be in position 0
        self.buy_item(0)

    def buy_item(self, item_index):
        item = self.shop_items[item_index]
        referer = Constants.NEO_HOMEPAGE + "browseshop.phtml?owner=" + self.owner
        updated_shop_page_source = web.get(self.session, Constants.NEO_HOMEPAGE + item.buy_link, referer=referer)

        #Could be some error checking, expired link, price change, someone else bought it
        self.__update_shop(updated_shop_page_source)
        print("Bought", item.name, "for", item.price, "NP")

        return item.price

    def print_shop_items(self):
        for item in self.shop_items:
            print(item.name, item.quantity, item.price)

class ShopItem():
    def __init__(self, name, price, quantity, obj_id, buy_link):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.obj_id = obj_id
        self.buy_link = buy_link

    def __str__(self):
        return self.name
