#!/usr/bin/env python
# -*- coding:utf8 -*-
from GRFY.Crawler import *
from ANJUKESOURCE.Crawler import *
from WUBATONGCHENG.Crawler import *
from GANJI.Crawler import *
from SOUFANG.Crawler import *
from FOCUSCN.Crawler import *
from FIRSTFYCN.Crawler import *
from Utils.SMTP import *


quit = False
while quit == False:
    try:
    #模拟登陆至房探主页
        init()
        initPhonelady()
        GRFY_thread = GRFY(6)
        GRFY_thread.start()
        time.sleep(5)
        SOUFANG_thread  = SOUFANG(1)
        SOUFANG_thread.start()
        time.sleep(5)
        ANJUKE_thread = ANJUKE(2)
        ANJUKE_thread.start()
        time.sleep(5)
        FIRSTFYCN_thread = FIRSTFYCN(3)
        FIRSTFYCN_thread.start()
        time.sleep(5)
        FOCUSCN_thread = FOCUSCN(4)
        FOCUSCN_thread.start()
        time.sleep(5)
        GANJI_thread = GANJI(5)
        GANJI_thread.start()
        time.sleep(5)
        WUBATONGCHENG_thread = WUBATONGCHENG(7)
        WUBATONGCHENG_thread.start()
        time.sleep(5)
    except Exception,ex:
        print(ex)
        sendmail(ex)
        pass

    time.sleep(6000)
    print(str(ANJUKE_thread.isAlive()) + "|" + str(FIRSTFYCN_thread.isAlive()) + "|" + str(FOCUSCN_thread.isAlive()) + "|" + str(GANJI_thread.isAlive()) + "|" + str(GRFY_thread.isAlive()) + "|" + str(SOUFANG_thread.isAlive()) + "|" + str(WUBATONGCHENG_thread.isAlive()))
    sql = SqliteOpenClass()
    sendmail("检索状态：\n\r\t安居客：" + str(ANJUKE_thread.isAlive()) + "\r\n\t第一房源：" + str(FIRSTFYCN_thread.isAlive()) + "\r\n\t焦点房产：" + str(FOCUSCN_thread.isAlive()) + "\r\n\t赶集网：" + str(GANJI_thread.isAlive())
             +  "\r\n\tGRFY：" +  str(GRFY_thread.isAlive()) + "\r\n\t搜房网：" + str(SOUFANG_thread.isAlive()) + "\r\n\t58同城：" + str(WUBATONGCHENG_thread.isAlive()) + "\r\n"
             +  "上次循环获取房源总计：" + str(sql.getcurrentnum()) + "\r\n"
             +  "历史房源总计：" + str(sql.gethisnum()))
    sql.movehousedata()
    SOUFANG_thread.stop()
    ANJUKE_thread.stop()
    FIRSTFYCN_thread.stop()
    FOCUSCN_thread.stop()
    GANJI_thread.stop()
    GRFY_thread.stop()
    WUBATONGCHENG_thread.stop()
    time.sleep(70)
