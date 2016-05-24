# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup
import threading
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from Utils.SMTP import *

opener = ''
mutex = threading.Lock()

def init():
    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)
    global opener
    opener = urllib2.build_opener(handler)
    postdata = urllib.urlencode({'userName':'skcncspeaker@hotmail.com',
    'password':'skcnc988330',
    'records':'1'})
    url = 'http://sh.fangtan007.com/my/doLogin'
    result = opener.open(url,postdata)
    print(result.msg)



def getbsobj(url):
    global mutex
    mutex.acquire()
    try:
        html = opener.open(url)
        bsObj = BeautifulSoup(html.read())
        mutex.release()
        return bsObj
    except Exception,ex:
        mutex.release()
        if ex.args[0].errno != 10060:
            init()
        print(ex)
        return ''