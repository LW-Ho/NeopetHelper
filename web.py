from urllib.parse import urlencode, quote_plus
import Constants, re, requests, json
from bs4 import BeautifulSoup

def check_for_random_event(response):
    if 'class="randomEvent"' in response:
        print("-----------RANDOM EVENT------------")
        soup = BeautifulSoup(response , "html.parser")
        div = soup.find("div", {'id':re.compile('^randomEventDiv')})
        text = div.find("div", {"class": "copy"}).getText().strip()
        print(text)

def get(session, url, referer = "" ):
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            #"Cache-Control": "max-age=0", #Cache control doesn't exist for refresh? or going to quickstock
            "Connection": "keep-alive",
            "Host": "www.neopets.com",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            }
    if referer != "":
        headers['Referer'] = referer

    r = session.get(url, headers=headers, allow_redirects=True).text
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            }

    s = urlencode(postFields, quote_via=quote_plus)
    headers['Content-Length'] = str(len(s))
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers["Origin"] = Constants.NEO_HOMEPAGE
    headers['Referer'] = referer

    r = session.post(url, postFields, headers=headers, allow_redirects=True, verify=False).text
    check_for_random_event(r)

    return r
