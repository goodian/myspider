#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: ChinadlztbSpiderHandler.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-04 10:59:15
# Last Modified: 2018-12-07 15:51:02
#


import os
import sys
import time
import requests

from bs4 import BeautifulSoup

from utils import *
from Item import *
from contants import *
from SiteSpiderHandler import *

URL = "http://www.chinadlztb.com.cn/news/list-9-{}.html"
FIRST_URL = "http://www.chinadlztb.com.cn/news/list-9.html"

class ChinadlztbSpiderHandler(SiteSpiderHandler):

    def __init__(self, buf):
        self.buf = buf
        self.page_count = 0
        self.local_datas_file = "chinadlztb.xml"

    def parse_url(self, url):
        r = requests.get(url, HEADERS).text
        soup = BeautifulSoup(r, "lxml")
        catlis = soup.find_all(class_ = "catlist_li")

        for l in catlis:
            t_str = l.span.get_text()
            href = l.a['href']
            title = l.a['title'].encode("utf-8")

            item = Item(t_str, href, title)
            self.buf.add(item)

    def get_page_count(self):
        r = requests.get(FIRST_URL, HEADERS).text
        soup = BeautifulSoup(r, "lxml")
        div = soup.find(class_ ="pages")
        # if div is None, it means no response
        if div is None: return

        last_url = div.input.get("value")
        self.page_count = int(last_url.split("-")[-1].split(".")[0])
        write_log("info", "page_count is : %d", self.page_count)

    def parse(self, max_time = -1):
        print("Entry Chinadlztb parser.")
        self.parse_url(FIRST_URL)

        self.get_page_count()

        for i in range(self.page_count):
            self.parse_url(URL.format(str(i + 1)))
            time.sleep(1)


    def datas_handle(self):
        # load old datas
        obuf = DatasBuffer()
        obuf.load(self.local_datas_file)



