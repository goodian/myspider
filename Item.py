#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: Item.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-04 12:01:19
# Last Modified: 2018-12-07 15:18:23
#


import os
import sys
import time

class Item:
    def __init__(self, t_str, href, title):
        self.t_str = t_str
        self.t_stamp = time.mktime(time.strptime(t_str, '%Y-%m-%d')) 
        self.href = href
        self.title = title

    def __str__(self):
        return u"time: %s\ttitle: %s\turl: %s\n" % \
                (self.t_str, self.title, self.href)

    def __eq__(self, obj):
        return self.t_str == obj.t_str and \
                self.href == obj.href and \
                self.title == obj.title

