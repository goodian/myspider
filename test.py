#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: test.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-04 14:45:06
# Last Modified: 2018-12-06 17:52:55
#


import os
import sys
import requests

from bs4 import BeautifulSoup

from ChinadlztbSpiderHandler import *

#handler = ChinadlztbSpiderHandler()

#handler.parse("http://www.chinadlztb.com.cn/news/list-9.html")

page_count = 0
url = "http://www.chinadlztb.com.cn/news/list-9.html"

r = requests.get(url, HEADERS).text
soup = BeautifulSoup(r, "lxml")
div = soup.find(class_ ="pages")
last_url = div.input.get("value")
page_count = int(last_url.split("-")[-1].split(".")[0])
print(page_count)
