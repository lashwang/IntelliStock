#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
import configuration as cf

mail_config = cf.mail_zlfm
mail_config_table = cf.MAIL_COFIG_TABLE[mail_config]
user_email = 'lashwang@outlook.com'


class Mail:
    def __init__(self):
        self.subject = 'Email authentication from AJ Kipper'
        self.content = 'Hi,thank you for registering the chat room created by AJ Kipper!'
        self.smtp_server = mail_config_table[cf.smtp_server]
        self.mail_account = mail_config_table[cf.mail_account]
        self.mail_passwd = mail_config_table[cf.mail_passwd]
    def send_email(self):
        msg = MIMEText(self.content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = self.subject
        msg['From'] = self.mail_account
        msg['To'] = user_email
        try:
            server = smtplib.SMTP(self.smtp_server)
            server.set_debuglevel(1)
            #server.connect(self.smtp_server)
            server.ehlo()
            server.starttls()
            server.login(self.mail_account, self.mail_passwd)
            server.ehlo()
            server.sendmail(self.mail_account,user_email,msg.as_string())
            server.close()
            return True
        except Exception, error:
            traceback.print_exc()
            print Exception,str(error)
            return False





