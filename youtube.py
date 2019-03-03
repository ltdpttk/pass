import concurrent.futures
import BlynkLib
import sys
import time 
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if sys.version_info[0] > 2:
	from http.cookiejar import LWPCookieJar
	from urllib.request import Request, urlopen
	from urllib.parse import quote_plus, urlparse, parse_qs
else:
	from cookielib import LWPCookieJar
	from urllib import quote_plus
	from urllib2 import Request, urlopen
	from urlparse import urlparse, parse_qs


_URL = 'https://www.youtube.com/watch?v=NrzLnl3tH0U?autoplay=1'
_MAIL = 'thuykieulk1999@gmail.com'
_VIEW = 0

blynk = BlynkLib.Blynk(token = 'e80ff069a180413cb357e059bb0a1568' , server = 'blynk.getblocky.com')
import _thread
_thread.start_new_thread(blynk.run,())

while blynk.state != BlynkLib.AUTHENTICATED:
    pass

def _viewCount():
    html = requests.get(_URL).text.split('\n')
    for x in html :
        if 'watch-view-count' in x :
            viewCount = int(x[116:].split(' ')[0])
            return viewCount
    return None

def _viewCheckRoutine():
    while True :
        time.sleep(10)
        currentCount = _viewCount()
        if currentCount != _VIEW :
            currentCount = _VIEW
            blynk.email(_MAIL , "Youtube View" , "View : {}".format(_viewCount()))
_thread.start_new_thread(_viewCheckRoutine,())

def randomDelay():
    delayTime = random.randrange(20 , 50)
    time.sleep(delayTime)


def chromeThread (a=0):
    for i in range(5):
        if i <5:
            randomDelay()
            web = webdriver.Chrome()
            web.get(_URL)
            time.sleep(120)
            randomDelay()
            web.quit()
        else:
            break





with concurrent.futures.ThreadPoolExecutor (max_workers=4) as ex :
    threads = {ex.submit(chromeThread,0) : 0 for i in range(1)}
    for future in concurrent.futures.as_completed(threads):
        url = threads[future]
        try :
            data = future.result()
        except Exception as err:
            print(err)
