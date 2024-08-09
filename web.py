from urllib.parse import urlencode, quote_plus
import Constants, re, time
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

def check_for_random_event(response):
    if 'class="randomEvent"' in response:
        print("-----------RANDOM EVENT------------")
        soup = BeautifulSoup(response , "html.parser")
        div = soup.find("div", {'id':re.compile('^randomEventDiv')})
        text = div.find("div", {"class": "copy"}).getText().strip()
        print(text)

def check_for_announcement(response):
    if 'class="bg-pattern"' in response:
        print("-----------Important Announcement!------------")
        return True

def check_avoid_stackpath(response):
    if 'is using a security service for protection against online attacks' in response:
        print("-----------Got StackPath!------------")
        return True

async def get_cookies(url):
    async with async_playwright() as p:
        for browser_type in [p.chromium]:
            browser = await browser_type.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            time.sleep(5)
            cookies = await context.cookies()
            await browser.close()

            temp_cookies = {}
            for index in cookies:
                temp_cookies[index['name']] = index['value']

            return temp_cookies

async def get(session, url, referer = "", cookies=None):
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            # "Cache-Control": "max-age=0", #Cache control doesn't exist for refresh? or going to quickstock
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.neopets.com",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': UA,
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            }
    if referer != "":
        headers['Referer'] = referer

    cookies = await get_cookies(Constants.NEO_LOGIN)
    r = session.get(url, headers=headers, cookies=cookies, allow_redirects=True, verify=False).text

    return r

async def post(session, url, postFields, referer, cookies=None):
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            #"Cache-Control": "max-age=0", #Cache control doesn't exist for refresh? or going to quickstock
            "Connection": "keep-alive",
            "Host": "www.neopets.com",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': UA,
            }

    s = urlencode(postFields, quote_via=quote_plus)
    headers['Content-Length'] = str(len(s))
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers["Origin"] = Constants.NEO_HOMEPAGE
    headers['Referer'] = referer

    cookies = await get_cookies(Constants.NEO_LOGIN)
    r = session.post(url, postFields, headers=headers, cookies=cookies, allow_redirects=True, verify=False).text

    return r
