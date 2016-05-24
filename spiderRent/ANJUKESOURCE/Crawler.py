# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading

class ANJUKE(threading.Thread):
    def __init__(self, threadno):
        super(ANJUKE,self).__init__()
        self.THREADNO = threadno
        self.LastUrl = ''
        self.thread_stop = False
        self.StartUrl = "http://sh.zu.anjuke.com/fangyuan/l2-px3/?kw=%E4%B8%AA%E4%BA%BA%E6%88%BF%E6%BA%90&cw=%E4%B8%AA%E4%BA%BA%E6%88%BF%E6%BA%90"

    def run(self):
        self.crawler(self.StartUrl)

    def stop(self):
        self.thread_stop = True

    def crawler(self,StartUrl):
        "http://sh.zu.anjuke.com/fangyuan/l2-px3/?kw=%E4%B8%AA%E4%BA%BA%E6%88%BF%E6%BA%90&cw=%E4%B8%AA%E4%BA%BA%E6%88%BF%E6%BA%90"
        LoopMark = True
        urlbuff = ''
        while LoopMark == True:
            if urlbuff != '':
                self.LastUrl = urlbuff
            urlbuff = ''
            import time
            time.sleep(60)  #每隔60s 启动一次查询
            html = urlopen(StartUrl)
            bsObj = BeautifulSoup(html.read())
            UrlList = bsObj.findAll("div",{'class','zu-itemmod'})
            count = 0
            for EleLi in UrlList:
                try:
                    href = EleLi.contents[3].contents[1].contents[0].attrs['href']
                    count += 1
                    if self.LastUrl == href:
                        break

                    if count >= 20:
                        break

                    if urlbuff == '':
                        urlbuff = href
                    #说明是新的信息，需要载入进来
                    self.crawler_level2(href)
                except:
                    continue

    def crawler_level2(self,SearchUrl):
        html = urlopen(SearchUrl)
        bsObj = BeautifulSoup(html.read())
        try:
            rooms = ''
            square = ''
            EstateName = ''
            Distinct = ''
            Area = ''
            Address = ''
            Orientation = ''
            type = ''
            floor = ''
            floorAll = ''
            renttype = ''
            decoration = ''
            price = bsObj.findAll("span",{"class","f26"})[0].string
            for ele in bsObj.findAll("dl",{"class","p_phrase"}):
                try:
                    if '房型' in ele.text:
                        rooms = ele.contents[3].string
                    elif '面积' in ele.text and  '总建' not in ele.text:
                        square = ele.contents[3].string
                    elif '小区名' in ele.text:
                        EstateName = ele.contents[3].contents[1].string
                    elif '版块' in ele.text:
                        Distinct = ele.contents[3].contents[1].string
                        Area = ele.contents[3].contents[3].string
                    elif '地址' in ele.text:
                        Address = ele.contents[3].contents[0]
                    elif '朝向' in ele.text:
                        Orientation = ele.contents[3].string
                    elif '类型' in ele.text:
                        type = ele.contents[3].string
                    elif '楼层' in ele.text:
                        floor = ele.contents[3].string.split('/')[0]
                        floorAll = ele.contents[3].string.split('/')[1]
                    elif '租赁方式' in ele.text:
                        renttype = ele.contents[3].string
                    elif '装修' in ele.text:
                        decoration = ele.contents[3].string
                except:
                    continue

            LandLadyName = bsObj.findAll(id='broker_true_name')[0].string
            LandLadyPhone = re.sub(' ','',bsObj.findAll("div",{"class","broker_tel"})[0].contents[1])
            appliance = ''
            dupmark = checkDup(LandLadyPhone)
            if dupmark == True:
                return

            try:
                content = bsObj.findAll("div",{"class","pro_links"})[0].contents[1]
                for ele in content:
                    if ele.name == 'span':
                        appliance += ele.text + '/'
            except:
                appliance = '未知'

            describe = bsObj.findAll("div",{"class","pro_con"})[0].text

            Sqlite = SqliteOpenClass()
            standardName = Sqlite.getestatename(EstateName,Address)

            try:
                countr =  re.findall(unicode("(\d+)室"),rooms)[0]
            except:
                countr = 0

            try:
                counth =  re.findall(unicode("(\d+)厅"),rooms)[0]
            except:
                counth = 0

            try:
                countt =  re.findall(unicode("(\d+)卫"),rooms)[0]
            except:
                countt = 0

            #判断房源类型类型，根据描述中关键词判断
            sourceType = "个人房源"

            if standardName == '':
                return
            else :
                id = uuid.uuid1()
                Sqlite.inserthouse(id,EstateName,floorAll,floor,'','unknown','unknown',type,renttype,decoration,
                                   sourceType,LandLadyName,LandLadyPhone,price,"面议",countt,counth,countr,square,
                                   Orientation,'', SearchUrl,describe,Distinct,Area)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            pass


