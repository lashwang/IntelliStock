#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_account = 'lashwang@outlook.com'
mail_passwd = 'meimei1985'
user_email = '171629646@qq.com'
mail_postfix = 'outlook.com'

class Mail:
    def __init__(self):
        self.smtp_server = 'smtp-mail.outlook.com:587'
        self.subject = 'Email authentication from AJ Kipper'
        self.form_msg = "This is a mailbox validation from" + ""
        self.content = 'Hi,thank you for registering the chat room created by AJ Kipper!'
        self.mail_account = mail_account
        self.mail_passwd = mail_passwd
        self.user_email = user_email
    def send_email(self):
        msg = MIMEText(self.content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = self.subject
        msg['From'] = self.form_msg
        msg['To'] = ";".join(self.user_email)
        try:
            server = smtplib.SMTP()
            # 服务器连接
            server.connect(self.smtp_server)
            # 返回服务器特性
            server.ehlo()
            # 进行TLS安全传输
            server.starttls()
            # 账号密码登录
            server.login(self.mail_account, self.mail_passwd)
            # 邮件正文发送
            server.sendmail(self.form_msg, self.user_email, msg.as_string())
            # 关闭服务器连接
            server.close()
            return True
        except Exception, error:
            print str(error)
            return False





