#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
import configuration as cf

mail_config = cf.mail_outlook
mail_config_table = cf.MAIL_COFIG_TABLE[mail_config]

class Mail:
    def __init__(self):
        self.subject = 'Email authentication from AJ Kipper'
        self.form_msg = "This is a mailbox validation from "
        self.content = 'Hi,thank you for registering the chat room created by AJ Kipper!'
        self.smtp_server = mail_config_table[cf.smtp_server]
        self.mail_account = mail_config_table[cf.mail_account]
        self.mail_passwd = mail_config_table[cf.mail_passwd]
        self.user_email = mail_config_table[cf.user_email]
    def send_email(self):
        msg = MIMEText(self.content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = self.subject
        msg['From'] = self.form_msg
        msg['To'] = ";".join(self.user_email)
        try:
            server = smtplib.SMTP(self.smtp_server)
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
            traceback.print_exc()
            print Exception,str(error)
            return False





