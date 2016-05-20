#coding=utf8
import smtplib
from email.mime.text import MIMEText
from email.header import Header


mail_host="smtp.scutech.com"  #设置服务器
mail_user="suncheng@scutech.com"    #用户名
mail_pass="Skcnc988330"   #口令

sender = 'suncheng@scutech.com'
receivers = ['suncheng@scutech.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def sendmail(error):
    message = MIMEText(error, 'plain', 'utf-8')
    message['From'] = Header(unicode("房源爬虫",'utf8'), 'utf-8')
    message['To'] =  Header("", 'utf-8')

    subject = unicode('房源进展通知','utf8')
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException,ex:
        print (ex)
        print "Error: 无法发送邮件"
