#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: MailSink.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-04 15:10:59
# Last Modified: 2018-12-07 15:00:50
#


import os
import sys
import smtplib

from utils import *

from email.mime.text import MIMEText

def MailSink():
    def __init__(self, host, port):
        self.host, self.port = host, port

    def send_mail(self, from_addr, to_addrs, subject = "", msg = ""):
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(from_addr, 'utf-8')
        message['To'] =  Header(",".joins(to_addrs), 'utf-8')

        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException:
            write_log("error", "send mail failed, smtp error.")
        except Exception:
            write_log("error", "send mail failed.")

