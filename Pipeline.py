#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: ./Pipeline.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-04 14:39:26
# Last Modified: 2018-12-07 15:18:24
#


import os
import sys

import threading

class Pipeline():
    def __init__(self):
        self.lock = threading.Lock()
        self.item_list = []


