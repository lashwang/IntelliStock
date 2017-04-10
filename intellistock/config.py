
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import datatime

mail_account = 'mail_account'
mail_passwd = 'mail_passwd'
smtp_server = 'smtp_server'


mail_qq = 'qq'
mail_outlook = 'outlook'
mail_sina = 'sina'
mail_zlfm = 'zlfm'


MAIL_CONFIG_QQ = {
    mail_account:'171629646@qq.com',
    mail_passwd:'Meimei_1985',
    smtp_server:'smtp.qq.com'
}


MAIL_CONFIG_OUTLOOK = {
    mail_account:'lashwang@outlook.com',
    mail_passwd:'meimei1985',
    smtp_server:'smtp-mail.outlook.com:587'
}

MAIL_CONFIG_SINA = {
    mail_account:'lashwang@sina.com',
    mail_passwd:'meimei1985',
    smtp_server:'smtp.sina.com'
}

MAIL_CONFIG_ZLFM = {
    mail_account:'stock@zl-fm.com',
    mail_passwd:'992154',
    smtp_server:'smtp.ym.163.com'
}



MAIL_COFIG_TABLE = {
    mail_qq: MAIL_CONFIG_QQ,
    mail_outlook: MAIL_CONFIG_OUTLOOK,
    mail_sina: MAIL_CONFIG_SINA,
    mail_zlfm: MAIL_CONFIG_ZLFM,
}

EXPORT_PATH_DIR = 'output'
EXPORT_XLS_FILE_NAME = 'stock_export_' + datatime.now_date() + '.xlsx'
EXPORT_XLS_FILE_PATH = os.path.join(EXPORT_PATH_DIR,EXPORT_XLS_FILE_NAME)

QQ_XINGU_URL = 'http://web.ifzq.gtimg.cn/stock/xingu/xgrl/xgql?' \
               'type=all&page={}&psize={}&col=sgrq&order=desc&_var=v_xgql'

QQ_XINGU_DEFAULT_PAGE_SIZE = 100

REQUEST_DELAY = 1


# cache time out, min
CACHE_FOLDER = os.path.join(EXPORT_PATH_DIR,'cache')
DEFAULT_CACHE_TIME_OUT_MIN = 120

CACHE_LOCK_FILE = 'index.lock'

CACHE_DB_FILE = 'cache.db'


# db config
STOCK_DB_FOLDER = os.path.join(EXPORT_PATH_DIR,'db')
STOCK_DB_PATH = os.path.join(STOCK_DB_FOLDER,'stock.db')


CHECK_IF_TRADING_URL = 'http://appqt.gtimg.cn/utf8/q=marketStat'