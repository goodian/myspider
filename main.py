#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#      Filename: main.py
#
#        Author: g.goodian@gmail.com
#   Description: ---
#        Create: 2018-12-03 18:39:31
# Last Modified: 2018-12-07 15:35:37
#

import os
import sys
import argparse
import threading

import requests

from utils import *
from DatasBuffer import *

from ChinadlztbSpiderHandler import *

#LOG_FILE = "/var/log/myspider.log"
LOG_FILE = "/tmp/myspider.log"
# interval, 1h
INTERVAL = 60 * 60

def spider_handler(buf):
    handler_list = []
    handler_list.append(ChinadlztbSpiderHandler(buf))
    last_time = 0

    while True:
        print("spider_handler111")
        time.sleep(3)
        print("spider_handler222")

        cur_time = time.time()
        if cur_time - last_time < INTERVAL:
            continue

        for handler in handler_list:
            handler.parse()
            handler.datas_handle()


def datas_handler(buf):
    print("entry datas_handler")
    while True:
        if buf.size() > 0:
            print("pop:", buf.pop())
            time.sleep(1)

def work_main(conf_file = ""):
    # TODO: load conf file

    # create datas buffer
    buf = DatasBuffer()

    spider_handler(buf)

def monitor_child():
    global CHILD
    while True:
        try:
            os.wait()
            pid = CHILD
            CHILD = 1
            logging.info("Fatal error detected from the child %d. Fork a new one in 5 seconds.\n",pid)
            break
        except OSError:
            pid = CHILD
            CHILD = 1
            logging.info("Failed to wait the child %d. Fork a new one in 5 seconds.\n",pid)
            break
        except KeyboardInterrupt:
            pid = CHILD
            CHILD = 1
            if pid != 1:
                kill_pid(pid,signal.SIGINT)
            # end if
            logging.info("Interrupted. Bye-bye~\n");
            os._exit(-1);
        except:
            if CHILD == 1:
                logging.info("Interrupted while monitoring. Child already terminated. Try to fork a new one.\n")
                break
            else:
                pass
            # end if
        # end try
    # end while
    try:
        time.sleep(5)
    except:
        pass
    # end try

#end monitor_child

if __name__ == "__main__":
    os.umask(0)
    set_logfile(LOG_FILE)

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--conf", help="conf location")
    parser.add_argument("-d", "--daemon", action='store_true', help="daemon mode")

    args = parser.parse_args()

    if args.daemon:
        make_daemon()
        while True:
            try:
                CHILD = os.fork()
            except Exception as e:
                logging.info('Failed to fork a child: %s. Retry in 5 seconds.\n',e)
                try:
                    time.sleep(5)
                except:
                    pass
                #end try
                continue
            #end try
            if CHILD == 0:
                logging.info('Child %d started to work.\n',os.getpid())
                work_main(args.conf)
                os.exit(-1)
            else:
                monitor_child()
            #end if
        #end while
    else:
        work_main(args.conf)
    #end if

