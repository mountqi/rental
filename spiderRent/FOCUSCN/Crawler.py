# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading
from Utils.Opener import *

class FOCUSCN(threading.Thread):
    "搜狐焦点"
    def __init__(self, threadno):
        super(FOCUSCN,self).__init__()
        self.THREADNO = threadno
        self.LastUrl = ''
        self.BaseUrl = 'http://sh.fangtan007.com'
        self.thread_stop = False
        self.StartUrl = "http://sh.fangtan007.com/chuzu/fangwu/w13/"

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
            try:
                UrlList = bsObj.findAll("div",{'class','sub-left-list'})[0].contents[1]
            except:
                print("获取失败：" + self.StartUrl)
                continue
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
                except Exception,ex:
                    continue

    def crawler_level2(self,SearchUrl):
        bsObj = getbsobj(SearchUrl)
        try:
            LandLadyPhone = bsObj.findAll(id='tel')[0].string

            dupmark = checkDup(LandLadyPhone)
            if dupmark == True:
                return

            LandLadyName = bsObj.findAll("div",{"class","info-right-div"})[0].contents[1].contents[1].contents[3].string
            Urls = re.findall('(http:\/\/[\w]+[\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])',bsObj.findAll("script")[12].text)
            SourceUrl = ''
            for url in Urls:
                if "focus.cn" in url and 'htm' in url:
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

            try:
                price = sourcebsObj.findAll("div",{"class","boxAtt"})[0].findAll("span")[0].string

                for ele in sourcebsObj.findAll("div",{"class","boxAL"})[0].contents:
                    try:
                        prop = ele.text
                    except:
                        continue
                    if '户型' in prop:
                        rooms = re.findall(unicode('：([\s|\S]+)\（','utf8'),prop)[0]
                    elif '面积' in prop:
                        square = re.findall(unicode('：([\s|\S]+)','utf8'),prop)[0]
                    elif '楼层' in prop:
                        floor = re.findall('\d+',prop)[0]
                        floorAll = re.findall('\d+',prop)[1]
                    else:
                        type = re.findall(unicode('：([\s|\S]+)','utf8'),prop)[0]

                for ele in sourcebsObj.findAll("div",{"class","boxAR"})[0].contents:
                    try:
                        prop = ele.text
                    except:
                        continue
                    if '装修' in prop:
                        decoration = re.findall(unicode('：([\s|\S]+)','utf8'),prop)[0]
                    elif '朝向' in prop:
                        Orientation = re.findall(unicode('：([\s|\S]+)','utf8'),prop)[0]
                    else:
                        continue

                try:
                    for ele in sourcebsObj.findAll('div',{"class","r"})[1].contents:
                        try:
                            T = ele.text
                        except:
                            continue
                        if '小区' in T:
                            estate = re.sub('[\r\n\t]','',ele.contents[1].text)
                            EstateName = re.sub(' ','',re.findall(unicode('：([\W|\w]+?)\（'),estate)[0])
                            area = re.findall(unicode('\（([\W|\w]+?)\）'),estate)[0].split(' ')[1]
                            district = re.findall(unicode('\（([\W|\w]+?)\）'),estate)[0].split(' ')[0]
                            Address = re.findall(unicode('：([\S|\s]+) ','utf8'),ele.contents[3].text)[0]
                        else:
                            continue
                    appliances = sourcebsObj.findAll("div",{"class","blockLC"})[0].contents[1].contents[1].findAll('span')
                    for item in appliances:
                        appliance += item.string + "|"
                    describe = sourcebsObj.findAll(id = "houseInfo")[0]
                    pics = ''
                    for p in sourcebsObj.findAll("div",{"class","blockLD"})[0].findAll("img"):
                        pics += p.attrs['src'] + '|'
                except:
                    pass
            except:
                pass

            Sqlite = SqliteOpenClass()

            try:
                describe = re.sub('[\r\n\t]','',describe.text)
            except:
                pass

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


