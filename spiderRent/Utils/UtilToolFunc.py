#coding=utf8
import re
from sqliteOper.Operations import *
import smtplib

landlady = ['无中介','非中介','个人房源','免中介','我是房东','个人发布',
                '个人出租','房东直接出租','本人是房东','房东直租','本人是房东',
                '发自手机','非诚勿扰','非中介出租','换工作','工作地点变更']
agency = ['本人中介']

Ladyphones = []



def checkSourceType(describe):
    "根据输入字符判断消息来源是房东/中介/租客"
    for word in landlady:
        arr = re.findall(unicode(word,'utf8') + "?",describe)
        if len(arr) > 0:
            return "个人房源"

    for word in agency:
        arr = re.findall(unicode(word,'utf8') + "?",describe)
        if len(arr) > 0:
            return "中介房源"

    #无法判断的类型
    sqlite = SqliteOpenClass()
    try:
        sqlite.insertUnknowndesc(describe)
    finally:
        return "疑似中介房源"


def checkDup(phone):
    phone = str(re.sub(' ','',phone))
    sql = SqliteOpenClass()

    if sql.checkdup(phone):
        return True
    else:
        Ladyphones.append(phone)
        sql.insertdbphone(phone)
        return False

def initPhonelady():
    sql = SqliteOpenClass()
    phones = sql.getphones()
    strs = phones.split('|')
    for Astring in strs:
        Ladyphones.append(str(re.sub(' ','',Astring)))









