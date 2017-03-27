
#!/usr/bin/python
# -*- coding: utf-8 -*-

import dateTimeUtil

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


EXPORT_XLS_FILE_NAME = 'stock_export_' + dateTimeUtil.now_date() + '.xlsx'
