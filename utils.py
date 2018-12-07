#!/usr/bin/env python
# -*- encoding:utf-8 -*-
#
#      Filename: utils.py
#
#        Author: gongyanlei@antell.com.cn
#   Description: ---
#        Create: 2017-08-04 16:37:53
# Last Modified: 2018-12-06 17:26:56
#

import os
import sys
import time
import logging

def __get_log_level(level = "info"):
    lv = level.lower()

    if lv == "debug":
        return logging.DEBUG
    elif lv == "critical":
        return logging.CRITICAL
    elif lv == "error":
        return logging.ERROR
    elif lv == "warning":
        return logging.WARNING
    else:
        return logging.INFO

#end __get_log_level

__logfile = ''
__MAX_LOG_SIZE = 2 * 1024 * 1024
def set_logfile(filename, maxsize = 2*1024*1024, level = "info"):
    global __logfile,__MAX_LOG_SIZE

    __logfile = filename
    if maxsize < 1024:
        print('maxsize too small. reset it to 1024.\n')
        __MAX_LOG_SIZE = 1024
    else:
        __MAX_LOG_SIZE = maxsize
    # end if

    logging.basicConfig(level=__get_log_level(level),
            format='%(asctime)s %(process)d [line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=filename,
            filemode='a')
# end set_logfile

def write_log(level, fmt, *msg):
    global __logfile, __MAX_LOG_SIZE
    if len(__logfile) == 0:
        return
    # end if

    size = 0

    try:
        size = os.path.getsize(__logfile)
    except:
        pass
    # end try

    try:
        if size >= __MAX_LOG_SIZE:
            os.system("truncate --size 0 " + __logfile)
            logging.log(__get_log_level(level), "Log file size reached the maximum. Truncated.")
        # end if

        logging.log(__get_log_level(level), fmt % msg)
    except Exception as e:
        print('Failed to write log to %s: %s.' % (__logfile,e))
        pass
# end write_log

def make_daemon():

    try:
        if os.fork() > 0: os._exit(0)
    except OSError as error:
        print('fork #1 failed: %d (%s)' % (error.errno, error.strerror))
        os._exit(1)    

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            print('Daemon PID %d' % pid)
            os._exit(0)
    except OSError as error:
        print('fork #2 failed: %d (%s)' % (error.errno, error.strerror))
        os._exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'ab+', 0)

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

#end make_daemon

