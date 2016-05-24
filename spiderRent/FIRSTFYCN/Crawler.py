# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading
from Utils.Opener import *

class FIRSTFYCN(threading.Thread):
    "搜狐焦点"
    def __init__(self, threadno):
        super(FIRSTFYCN,self).__init__()
        self.THREADNO = threadno
        self.LastUrl = ''
        self.BaseUrl = 'http://sh.fangtan007.com'
        self.thread_stop = False
        self.StartUrl = "http://sh.fangtan007.com/chuzu/fangwu/w24/"

    def run(self):
        self.crawler()

    def stop(self):
        self.thread_stop = True

    def crawler(self):
        "http://sh.fangtan007.com/chuzu/fangwu/w13/"
        urlbuff = ''
        while self.thread_stop == False:
            if urlbuff != '':
                self.LastUrl = urlbuff
            urlbuff = ''
            import time
            time.sleep(60)  #每隔60s 启动一次查询
            bsObj = getbsobj(self.StartUrl)
            UrlList = bsObj.findAll("div",{'class','sub-left-list'})[0].contents[1]
            count = 0
            for EleLi in UrlList:
                try:
                    href = EleLi.findAll('div',{"class","houseinfo-name"})[0].contents[0].contents[0].attrs['href']
                    count += 1
                    if self.LastUrl == href:
                        break

                    if count >= 3:
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
                if "01fy.cn" in url and 'htm' in url:
                    SourceUrl = url
                    break
            if SourceUrl == '':
                return
            sourceHtml = urlopen(SourceUrl)
            sourcebsObj = BeautifulSoup(sourceHtml.read())

            square = ''
            floorAll = ''
            floor = ''
            decoration = ''
            Orientation = ''
            type = ''
            Address = ''
            appliance = ''
            district = ''
            area = ''
            describe = ''
            try:
                for ele in sourcebsObj.findAll("div",{"class","cr_left"})[0].contents:
                    T = ''
                    try:
                        T = re.sub('[\r\n\t ]','',ele.text)
                    except:
                        continue
                    if '租金价格' in T:
                        if '面议' in T:
                            price = '面议'
                        else:
                            price = re.findall('\d+',re.sub('[\r\n\t ]','',T))[0]
                    elif '户型面积' in T:
                        estate = re.findall(unicode('：([\S|\s]+)','utf8'),T)[0]
                        rooms = re.sub(' ','',estate.split('-')[0])
                        square = re.sub(' ','',estate.split('-')[1])
                    elif '小区名称' in T:
                            EstateName = re.findall(unicode('：([\S|\s]+)\（?','utf8'),T)[0]
                    elif '小区地址' in T:
                        position = re.findall(unicode('：([\S|\s]+)','utf8'),T)[0]
                        district = re.sub(' ','',position.split('-')[1])
                        if len(position.split('-')) == 4:
                            area = re.sub(' ','',position.split('-')[2])
                        if len(position.split('-')[len(position.split('-'))-1]) > 2:
                            Address = re.findall(unicode('[\（|\(]([\S|\s]+)[\）\)]','utf8'),position)[0]
                    elif '概况' in T:
                        prop = re.findall(unicode('：([\S|\s]+)','utf8'),T)[0]
                        if '-' in prop:
                            for e in prop.split('-'):
                                if "装修" in e:
                                    decoration = e
                                elif '东' in e or '西' in e or  '南' in e or  '北' in e:
                                    Orientation = e
                                else:
                                    type = e
                        else:
                             if "装修" in prop:
                                 decoration = prop
                             elif '东' in prop or '西' in prop or  '南' in prop or  '北' in prop:
                                Orientation = prop
                             else:
                                type = prop
                    elif '楼层' in T:
                        try:
                            floor = re.findall('\d+',T)[0]
                            floorAll = re.findall('\d+',T)[1]
                        except:
                            pass
                    elif '联系人' in T:
                        LandLadyName = re.findall(unicode('：([\S|\s]+)','utf8'),T)[0]


                describe =  sourcebsObj.findAll("div",{"class","des"})[0].text

                pics = ''
                try:
                    for ele in sourcebsObj.findAll('div',{"class","desc-image"}):
                        pics += ele.findAll("img")[0].attrs["data-original"] + "|"
                except:
                    pass

            except Exception,exc:
                print(exc)
                print(SourceUrl)

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
                Sqlite.insertpiclinks(id,pics)
                Sqlite.inserthouse(id,EstateName,floorAll,floor,'','unknown','unknown',type,"整租",decoration,
                                   sourceType,LandLadyName,LandLadyPhone,price,"面议",countt,counth,countr,square,
                                   Orientation,appliance, SourceUrl,describe,district,area)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            pass


