from urllib.parse import urlencode, quote_plus
import Constants, re, time
from bs4 import BeautifulSoup
from selenium import webdriver
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

def get_cookies(url):
    # Use selenium to get stackpath cookies.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=' + UA)
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    try:
        browser = webdriver.Chrome(executable_path='./chromedriver/stable/chromedriver',options=chrome_options)
    except:
        browser = webdriver.Chrome(options=chrome_options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    browser.get(url)
    time.sleep(5)
    _d = {}
    for i in browser.get_cookies():
        _d[i.get('name')] = i.get('value')
    browser.close()
    return _d

def get(session, url, referer = "", cookies={}):
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

    cookies = get_cookies(Constants.NEO_LOGIN) # avoid stackpath CDN
    r = session.get(url, headers=headers, cookies=cookies, allow_redirects=True, verify=False).text
    check_for_random_event(r)

    return r

def post(session, url, postFields, referer):
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

    cookies = get_cookies(Constants.NEO_LOGIN) # avoid stackpath CDN
    r = session.post(url, postFields, headers=headers, cookies=cookies, allow_redirects=True, verify=False).text
    check_for_random_event(r)

    return r
