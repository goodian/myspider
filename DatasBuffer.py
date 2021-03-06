#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: DatasBuffer.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-06 11:18:01
# Last Modified: 2018-12-07 17:10:58
#


import os
import sys
import threading

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from Item import *

class DatasBuffer:
    def __init__(self):
        self.blist = []
        self.lock = threading.Lock()

    def add(self, e):
        self.lock.acquire()
        self.blist.append(e)
        self.lock.release()

    def pop(self):
        self.lock.acquire()

        if self.size() > 0:
            try:
                e = self.blist.pop()
            except Exception as e:
                pass
        else:
            e = None

        self.lock.release()

        return e

    def reset(self):
        self.lock.acquire()
        self.blist.clear()
        self.lock.release()

    def size(self):
        return len(self.blist)

    def __parse_file(self, fp):
        tree = ET.parse(SYS_ROUTE_CONF);
        if not tree: return

        data_list = tree.findall("data")
        for d in data_list:
            try:
                href = d.attrib["href"]
                title = d.attrib["title"]
                t_str = d.attrib["timeDate"]
            except Exception as e:
                continue

            self.add(Item(t_str, href, title))

    def load(self, f):
        with open(f) as fp:
            __parse_file(fp)

    def __dump_file(self, fp):
        pass

    def dump(self, f):
        with open(f) as fp:
            __dump_file(fp)

