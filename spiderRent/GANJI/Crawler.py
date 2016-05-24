# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading
from Utils.Opener import *

class GANJI(threading.Thread):
    "赶集网"
    def __init__(self, threadno):
        super(GANJI,self).__init__()
        self.THREADNO = threadno
        self.LastUrl = ''
        self.BaseUrl = 'http://sh.fangtan007.com'
        self.thread_stop = False
        self.StartUrl = "http://sh.fangtan007.com/chuzu/fangwu/w02/"

    def run(self):
        self.crawler(self.StartUrl)

    def stop(self):
        self.thread_stop = True

    def crawler(self,StartUrl):
        "http://sh.fangtan007.com/fangwu/w01/"
        urlbuff = ''
        while self.thread_stop == False:
            if urlbuff != '':
                self.LastUrl = urlbuff
            urlbuff = ''
            import time
            time.sleep(60)  #每隔60s 启动一次查询
            bsObj = getbsobj(StartUrl)
            UrlList = bsObj.findAll("div",{'class','sub-left-list'})[0].contents[1]
            count = 0
            for EleLi in UrlList:
                try:
                    href = EleLi.findAll('div',{"class","houseinfo-name"})[0].contents[0].contents[0].attrs['href']
                    count += 1
                    if self.LastUrl == href:
                        break

                    if count >= 20:
                        break

                    if urlbuff == '':
                        urlbuff = href
                    #说明是新的信息，需要载入进来
                    self.crawler_level2(self.BaseUrl + href)
                except:
                    continue

    def crawler_level2(self,SearchUrl):
        bsObj = getbsobj(SearchUrl)
        try:
            LandLadyPhone = bsObj.findAll(id='tel')[0].string

            dupmark = checkDup(LandLadyPhone)
            if dupmark == True:
                return

            Urls = re.findall('(http:\/\/[\w]+[\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])',bsObj.findAll("script")[12].text)
            SourceUrl = ''
            for url in Urls:
                if "ganji.com" in url and 'htm' in url:
                    SourceUrl = url
                    break
            if SourceUrl == '':
                return
            sourceHtml = urlopen(SourceUrl)
            sourcebsObj = BeautifulSoup(sourceHtml.read())
            price = sourcebsObj.findAll("b",{"class","basic-info-price"})[0].contents[0].string

            square = ''
            floorAll = ''
            floor = ''
            decoration = ''
            Orientation = ''
            type = ''
            LandLadyName = ''
            Address = ''
            appliance = ''
            rentType=''
            counth = '0'
            countr = '0'
            countt = '0'
            district = ''
            area = ''
            EstateName = ''
            for ele in sourcebsObj.findAll("ul",{"class","basic-info-ul"})[0].contents:
                try:
                    prop = re.sub('[\t\r\n ]','',ele.text)
                except:
                   continue
                if "户型" in prop:
                    try:
                        roomprops1 = prop.split('-')
                        for state in roomprops1:
                            if "室" in state:
                                rooms = state
                            elif '㎡' in state:
                                square = state
                            else:
                                rentType = state
                    except:
                        pass
                elif "概况" in prop:
                    for state in prop.split('：')[1].split('-'):
                        if '装修' in state or "毛坯" in state:
                            decoration = state
                        elif '东' in state or '西' in state or '南' in state or '北' in state:
                            Orientation = state
                        else:
                            type = state
                elif "小区" in prop:
                    EstateName = re.findall(unicode('：([\W|\w]+)[-|\（|\(]'),prop)[0]
                    if '-' in EstateName:
                        EstateName = EstateName.split('-')[0]
                elif "楼层" in prop:
                    floor = re.findall('(\d+)',prop)[0]
                    floorAll = re.findall('(\d+)',prop)[1]
                elif "位置" in prop:
                    position = re.findall(unicode('：([\W]+)','utf8'),re.sub(' ','',sourcebsObj.findAll("ul",{"class","basic-info-ul"})[0].contents[11].text))[0].split('-')
                    district = position[1]
                    if len(position) == 2:
                        area = position[1]
                    else:
                        area = position[2]
                elif "地址" in prop:
                    Address = re.sub('[\t\n\r ]','',ele.contents[3].text)
                elif "配置" in prop:
                    appliance = prop.split('：')[1]

            LandLadyName = re.findall(unicode('：([\W|\w]+)\(','utf8'),re.sub('[\r\n\t ]','',sourcebsObj.findAll("span",{"class","contact-col"})[0].text))[0]

            #图片列表
            pics = ''
            if len(sourcebsObj.findAll("div",{"class","pics"})) > 0:
                for ele in sourcebsObj.findAll("div",{"class","pics"})[0].findAll("img"):
                    pics += ele.attrs['src'] + "|"

            Sqlite = SqliteOpenClass()

            describe = re.sub('[\r\n\t ]','',sourcebsObj.findAll('div',{"class","summary-cont"})[0].text)

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
                Sqlite.insertpiclinks(id,pics)
                Sqlite.inserthouse(id,EstateName,floorAll,floor,'','unknown','unknown',type,rentType,decoration,
                                   sourceType,LandLadyName,LandLadyPhone,price,"面议",countt,counth,countr,square,
                                   Orientation,appliance, SourceUrl,describe,district,area)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            print(SourceUrl)
            pass


