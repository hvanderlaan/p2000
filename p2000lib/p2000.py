#!/usr/bin/env python

# file     : p2000lib/p2000.py
# purpose  : modules for displaying p2000 pager messages
#
# author   : harald van der laan
# date     : 2016/11/25
# version  : v1.0.1
#
# changelog:
# - v1.0.1      created different colorschema for microsoft windows
# - v1.0.0      initial version

''' p2000lib/p2000.py - module for displaying p2000 pager messages '''

from __future__ import print_function
import re
import platform

# pylint: disable=R0903
# R0903: to few public methods
class DisplayMessage(object):
    ''' class for displaying the pager messages in color '''
    def __init__(self, msgtype, msg):
        self.msgtype = msgtype
        self.msg = msg

        if platform.system() == 'Windows':
            self.fdp = '\033[1;31m'         # red color
            self.lfl = '\033[1;32m'         # green color
            self.ems = '\033[1;33m'         # yellow color
            self.pdp = '\033[1;34m'         # blue color
            self.cgd = '\033[31m'           # color light red
            self.rst = '\033[0m'            # normal color (reset)
        else:
            self.fdp = '\033[38;5;9m'       # red color
            self.lfl = '\033[38;5;118m'     # green color
            self.ems = '\033[38;5;220m'     # yellow color
            self.pdp = '\033[38;5;39m'      # blue color
            self.cgd = '\033[38;5;208m'     # orange color
            self.rst = '\033[0m'            # normal color (reset)

        if msgtype == 'lfl':
            print("{}{}{}" .format(self.lfl, self.msg, self.rst))
        elif self.msgtype == 'fdp':
            print("{}{}{}" .format(self.fdp, self.msg, self.rst))
        elif self.msgtype == 'ems':
            print("{}{}{}" .format(self.ems, self.msg, self.rst))
        elif self.msgtype == 'pdp':
            print("{}{}{}" .format(self.pdp, self.msg, self.rst))
        elif self.msgtype == 'cgd':
            print("{}{}{}" .format(self.cgd, self.msg, self.rst))
        else:
            print("{}{}{}" .format(self.pdp, self.msg, self.rst))

class PreprocessMessage(object):
    ''' class for determening the call type '''
    def __init__(self, msg):
        self.msg = msg

        if (re.match('.*[Ll]ifeliner', self.msg) or re.match('.*[Ll][Ff][Ll]', self.msg)
                or re.match('.*[Mm][Mm][Tt]', self.msg)):
            self.msgtype = 'lfl'
        elif (re.match('.*GLM_', msg) or re.match('.*BRW', msg)
              or re.match('.*[Bb]randweer', msg) or re.match('^[Pp][Rr][Ii][Oo]', msg)
              or re.match('^[Pp] ', msg) or re.match('^AL', msg)):
            self.msgtype = 'fdp'
        elif re.match('.*Wachtarts', msg) or re.match('.*Forensisch', msg):
            self.msgtype = 'pdp'
        elif (re.match('.*A[1-2]', msg) or re.match('.*[Aa][Mm][Bb][Uu]', msg)
              or re.match('.*B[1-2]', msg) or re.match('.*Solo', msg) or re.match('.*VWS', msg)
              or re.match('.*CPA', msg) or re.match('.*SEH', msg) or re.match('.*MKA', msg)
              or re.match('.*RAV', msg) or re.match('.*RAVAA', msg) or re.match('.*GHOR', msg)
              or re.match('.*OvDG', msg) or re.match('.*test', msg)):
            self.msgtype = 'ems'
        elif re.match('.*[Kk][Nn][Bb][Rr][Dd]', msg) or re.match('.*[Kk][Nn][Mm][Rr]', msg):
            self.msgtype = 'cgd'
        else:
            self.msgtype = 'other'
