#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import traceback
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename
import logging

import Configuration as cf
import DateTimeUtil



logger = logging.getLogger(__name__)



mail_config = cf.mail_zlfm
mail_config_table = cf.MAIL_COFIG_TABLE[mail_config]
user_email = 'lashwang@outlook.com'


class Mail(object):
    def __init__(self):
        self.subject = 'Stock report on ' + DateTimeUtil.now_datetime()
        self.content = 'Stock report on ' + DateTimeUtil.now_datetime()
        self.smtp_server = mail_config_table[cf.smtp_server]
        self.mail_account = mail_config_table[cf.mail_account]
        self.mail_passwd = mail_config_table[cf.mail_passwd]


    def send_email(self,files=None):
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.mail_account
        msg['To'] = user_email
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(self.content, _subtype='plain', _charset='utf-8'))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server)
            # server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login(self.mail_account, self.mail_passwd)
            server.ehlo()
            server.sendmail(self.mail_account,user_email,msg.as_string())
            server.close()
            return True
        except Exception, error:
            logger.error(str(error))
            return False





