# -*- coding: utf-8 -*-
from urllib import urlopen
from sqliteOper.Operations import *
from Utils.UtilToolFunc import *
from bs4 import BeautifulSoup
import re
import threading
from Utils.Opener import *
from StringIO import StringIO
import gzip

class SOUFANG(threading.Thread):
    "赶集网"
    def __init__(self, threadno):
        super(SOUFANG,self).__init__()
        self.THREADNO = threadno
        self.LastUrl = ''
        self.BaseUrl = 'http://sh.fangtan007.com'
        self.thread_stop = False
        self.StartUrl = "http://sh.fangtan007.com/chuzu/fangwu/w05/"

    def run(self):
        self.crawler()

    def stop(self):
        self.thread_stop = True

    def crawler(self):
        "http://sh.fangtan007.com/fangwu/w05/"
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
            #LandLadyName  = bsObj.findAll('div',{"class","info-right-div"})[0].contents[1].contents[1].contents[3].string
            Urls = re.findall('(http:\/\/[\w]+[\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])',bsObj.findAll("script")[12].text)
            SourceUrl = ''
            for url in Urls:
                if "fang.com" in url and 'htm' in url:
                    SourceUrl = url
                    break
            if SourceUrl == '':
                return

            request = urllib2.Request(SourceUrl)
            request.add_header('Accept-encoding', 'gzip')
            response = urllib2.urlopen(request)
            sourcebsObj = ''
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO( response.read())
                f = gzip.GzipFile(fileobj=buf)
                data = unicode(f.read(),'gbk')


            square = ''
            floorAll = ''
            floor = ''
            decoration = ''
            Orientation = ''
            type = ''
            LandLadyName = ''
            Address = ''
            appliance = ''
            rentType= '不限'
            counth = '0'
            countr = '0'
            countt = '0'
            describe = ''
            District = ''
            Area = ''

            Sqlite = SqliteOpenClass()

            for element in re.findall('\<ul[\S|\s]+?ul\>',data):
                if '<li class="chuang">' in element:
                    ull = BeautifulSoup(element)
                    appliance = re.sub('\n','|',ull.findAll("ul")[0].text)
                elif 'house-info' in element:
                    ull = BeautifulSoup(element)
                    for ele in ull.findAll("ul")[0]:
                        try:
                            text = re.sub('[\r\n\t ]','',ele.text)
                        except:
                            continue
                        if '租金' in text:
                            price = ele.contents[1].string
                        elif '概况' in text:
                            props = text.split('：')[1].split('|')
                            for con in props:
                                if '室' in con:
                                    rooms = con
                                elif 'm²' in con:
                                    square = con
                                elif '/' in con and '层' in con:
                                    floor = re.findall('\d+',con)[0]
                                    floorAll = re.findall('\d+',con)[1]
                                elif '东' in con or '西' in con or '南' in con or '北' in con:
                                    Orientation = con
                                elif '装修' in con or '不限' in con:
                                    decoration = con
                                else:
                                    type = con
                        elif '小区' in text:
                            EstateName = re.findall(unicode('：([\W|\w]+?)\[','utf8'),text)[0]
                            try:
                                District = re.findall('\[([\S|\s]+?)\]',text)[0].split('/')[0]
                                Area = re.findall('\[([\S|\s]+?)\]',text)[0].split('/')[1]
                            except:
                                Area = Sqlite.getestatelinkwithname(EstateName)
                                District = Sqlite.getareadistrict(Area)



            if len(re.findall('\<div class="agent-txt agent-txt-per floatl"\>([\S|\s]+?)\<\/div\>',data)) > 0:
                describe = re.sub('\<[\S|\s]+?\>','',re.sub('[\r\n\t ]','',re.findall('\<div class="agent-txt agent-txt-per floatl"\>([\S|\s]+?)\<\/div\>',data)[0]))

            if len(re.findall('\<span class="floatl name"\>([\S|\s]+?)\<\/span\>',data)) > 0:
                LandLadyName = re.findall('\<span class="floatl name"\>([\S|\s]+?)\<\/span\>',data)[0]

            Address = ''

            #图片列表
            pics = ''
            for ele in re.findall('\<img[\S|\s]+?\>',data):
                if 'mt10' in ele:
                    obj = BeautifulSoup(ele).findAll("img")[0]
                    pics += obj.attrs['src'] + "|"

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
                                   Orientation,appliance,SourceUrl,describe,District,Area)
                return
        except Exception,ex:
            print(ex)
            print(SearchUrl)
            print(SourceUrl)
            pass


