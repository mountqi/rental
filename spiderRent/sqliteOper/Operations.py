#-*- coding: UTF-8 -*-
import sqlite3
import uuid
import time
import threading

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SqliteOpenClass:
    def __init__(self):
        self.lock = threading.RLock()
        self.dbpath = 'F:\项目文档\SpiderRent\spiderRent\HouseDB\HouseInfo'

    def get_conn(self):
        conn = sqlite3.connect( self.dbpath )
        return conn

    def conn_close(self,conn=None):
        conn.close()

    def save(self,sql, conn=None):
        conn.execute(sql)

    def insertdistinct(self,disId,distinctName,CityId):
        if distinctName.strip() == '':
            pass
        name = unicode(distinctName)
        sql = "INSERT INTO Dics VALUES ('{0}','{1}','{2}')".format(disId,name,CityId)
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def getestatelink(self):
        sql = "SELECT ESTATENAME, ESTATELINK, MARK FROM ESTATELINK where mark = 'N'"
        connection = self.get_conn()
        cur = connection.execute(sql)
        arr = []
        time.sleep(0.01)
        for row in cur:
            try:
                arr.append(row)
            except:
                print(row)
        self.conn_close(connection)
        return arr

    def getestatearea(self,estatename):
        sql = "SELECT AREANAME FROM ESTATELINK where ESTATENAME = '{0}'".format(estatename)
        connection = self.get_conn()
        cur = connection.execute(sql)
        time.sleep(0.01)
        if cur.arraysize == 0:
            self.conn_close(connection)
            return ''
        self.conn_close(connection)
        return cur[0]

    def getestatename(self,name,address):
        "小区名字重复性判断"
        name = name.strip()
        sql = "SELECT AliasA FROM EstateAlias WHERE AliasA like '%{0}%' OR AliasB like '%{1}%' OR AliasC like '%{2}%' OR AliasD like '%{3}%'".format(name,name,name,name)
        connection = self.get_conn()
        cur = connection.execute(sql)
        data = cur.fetchall()
        connection.commit()
        time.sleep(0.01)
        if len(data) == 0:
            sqlInsert = "INSERT INTO UnKnownEstateName VALUES ('{0}','{1}')".format(name,address)
            connection.execute(sqlInsert)
            self.conn_close(connection)
            return ''
        else :
            self.conn_close(connection)
            return name

    def updatestatelink(self,link):
        sql = "UPDATE ESTATELINK SET MARK = 'Y' WHERE ESTATELINK LIKE '%{0}%'".format(link.strip('\n'))
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def getestatelinkwithname(self,name):
        sql = "SELECT AREANAME FROM ESTATELINK WHERE ESTATENAME LIKE '%{0}%'".format(name.strip())
        connection = self.get_conn()
        value = connection.execute(sql)
        connection.commit()
        r = value.fetchall()
        try:
            return r[0][0]
        except:
            return ''

    def getareadistrict(self,area):
        sql = "SELECT DISTINCTNAME FROM DICS WHERE DISTINCTID IN (SELECT DISTINCTID FROM AREA WHERE AREANAME LIKE '%{0}%')".format(area.strip())
        connection = self.get_conn()
        value = connection.execute(sql)
        connection.commit()
        r = value.fetchall()
        try:
            return r[0][0]
        except:
            return ''

    def insertestatelink(self,area, name,link):
        sql = "INSERT INTO ESTATELINK VALUES ('{0}','{1}','{2}')".format(area ,name,link)
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def insertarea(self,AreaId,AreaName,DistinctId,CityId,Sublink):
        sql = "INSERT INTO AREA (AreaID, AreaName,DistinctID,CityID,xqlistLink)" \
            "VALUES ('{0}','{1}','{2}','{3}','{4}')".format(AreaId,AreaName,DistinctId,CityId,Sublink)
        connection = self.get_conn()
        connection.execute(sql)
        connection.commit()
        self.conn_close(connection)

    def insertestate(self,estateId, EstateName,distinct,area,TotalSquare,TotalHouse,BuildYear,FloorAreaRatio,ParkingNum,GreenRate,\
                     Address,Developer,PropertyType,PropertyFee,PropertyCompany,CityId):
        sql = " INSERT INTO Estate (EstateID,EstateName,DistinctID,CityID,BuildYear,Address,Developer," \
                "PropertyCompany,PropertyType,PropertyFee,TotalSquare,TotalHouse,FloorAreaRatio,ParkingNum,GreenRate)" \
                " values ('{0}', '{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}')".format(estateId,\
                EstateName,distinct,CityId,BuildYear,Address,Developer,PropertyCompany,PropertyType,PropertyFee,TotalSquare,\
                TotalHouse,FloorAreaRatio,ParkingNum,GreenRate)
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()

    def inserthouse(self,houseId,EstateName,FloorAll,Floor,FloorLevel,RoomNum,BuildingNo,Type,RentType,
                    Decoration,HouseSourceType,LandladyName,LandLadyPhone,RentPrice,PriceType,CountT,CountH,CountR,
                    Square,Orientation,Appliance,link,descibe,district,area):
        ISOTIMEFORMAT="%Y-%m-%d %X"
        curtime = time.strftime(ISOTIMEFORMAT, time.localtime())

        sql_insert_house = "INSERT INTO House VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')".format(
            houseId,EstateName,curtime,str(FloorAll),str(Floor), '',RoomNum,BuildingNo,Type,district,area)

        sql_insert_houseinfo = "INSERT INTO HouseInfo VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}')".format(
            houseId,RentType,Decoration,HouseSourceType,LandladyName,LandLadyPhone,RentPrice,RentType,str(CountT),str(CountH),str(CountR),str(Square),
            Orientation,Appliance,curtime,link,descibe)

        conn = sqlite3.connect(self.dbpath)
        conn.execute(sql_insert_house)
        conn.execute(sql_insert_houseinfo)
        conn.commit()
        conn.close()

    def insertUnknowndesc(self,describe):
        sql = "INSERT INTO UnKnownDescWord VALUES ('{0}')".format(describe)
        conn = sqlite3.connect(self.dbpath)
        conn.execute(sql)
        conn.commit()
        conn.close()

    def insertpiclinks(self,id,links):
        if len(links) == 0:
            return

        sql = "INSERT INTO HousePicLinks VALUES('{0}','{1}')".format(id,links)
        conn = sqlite3.connect(self.dbpath)
        conn.execute(sql)
        conn.commit()
        conn.close()

    def getdbphone(self):
        sql = "SELECT * FROM PHONELIST"
        conn = sqlite3.connect(self.dbpath)
        value = conn.execute(sql)
        conn.commit()
        r = value.fetchall()
        try:
            return r
        except:
            return ''

    def insertdbphone(self,phone):
        sql = "INSERT INTO PHONELIST VALUES ('{0}')".format(phone)
        conn = sqlite3.connect(self.dbpath)
        conn.execute(sql)
        conn.commit()
        conn.close()

    def movehousedata(self):
        sqlA = "INSERT INTO HOUSEHIS SELECT * FROM HOUSE"
        sqlB = "INSERT INTO HOUSEINFOHIS SELECT * FROM HOUSEINFO"
        sqlC = "DELETE FROM HOUSE"
        sqlD = "DELETE FROM HOUSEINFO"
        sqlE = "DELETE FROM PHONELIST"

        conn = sqlite3.connect(self.dbpath)
        conn.execute(sqlA)
        conn.execute(sqlB)
        conn.execute(sqlC)
        conn.execute(sqlD)
        conn.execute(sqlE)
        conn.commit()
        conn.close()

    def insertnewphone(self,phone):
        sqlA = "INSERT INTO PHONELIB VALUES '{0}'".format(phone)

        conn = sqlite3.connect(self.dbpath)
        conn.execute(sqlA)
        conn.commit()
        conn.close()

    def getphones(self):
        sql = "SELECT * FROM PHONELIST"
        PHONES = ''
        connection = self.get_conn()
        value = connection.execute(sql)
        connection.commit()
        r = value.fetchall()
        for phone in r:
            PHONES += phone[0] + "|"
        return PHONES

    def checkdup(self,phone):
        sql = "SELECT * FROM PHONELIST WHERE PHONE = '{0}'".format(phone)
        connection = self.get_conn()
        value = connection.execute(sql)
        connection.commit()
        r = value.fetchall()
        if len(r) > 0:
            return True;
        else:
            return False;

    def getcurrentnum(self):
        "获取House表房源数量"
        sql = "SELECT COUNT(*) FROM HOUSE";
        connection = self.get_conn()
        cur = connection.execute(sql)
        connection.commit()
        value = cur.fetchall()
        return value[0][0]

    def gethisnum(self):
        "获取历史表中字段数量"
        sql = "SELECT COUNT(*) FROM HOUSEHIS";
        connection = self.get_conn()
        cur = connection.execute(sql)
        connection.commit()
        value = cur.fetchall()
        return value[0][0]












