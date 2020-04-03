#!/usr/bin/env python

# File   : ./p2000.py
# Purpose: Python script for showing emergency services pager messages
#
# Auhtor : Harald van der Laan
# Date   : 2018/09/20
# Version: v2.3.2
#
# Requirements:
#  - requests
#  - bs4
#  - progress
#  - working internet connection
#
# Changelog:
#  - v2.3.2     Bugfix: most recent message in -f mode was not shown     Harald
#  - v2.3.1     Added extra option -c and clean up unused code           Harald
#  - v2.3.0     pretify follow mode / autorefresh                        Gerdriaan
#  - v2.2.3     better import of configfile                              Harald
#  - v2.2.2     Created new header in python files                       Harald
#  - v2.2.1     Fixed unicode bug                                        Harald
#  - v2.2.0     recode with nicer code                                   Harald
#  - v2.1.0     added refresh modus to script and configuration file     Harald
#  - v2.0.1     added configuration file for variable urls               Harald
#  - v2.0.0     script rewritten to python                               Harald
#  - =< v1.9.9  Legacy and not supported any more                        Harald
#
# Copyright:
# =============================================================================
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For the full license, see the LICENSE file.
#
# Disclaimer:
# =============================================================================
# Software provided by Harald van der Laan is for illustrative purposes only
# which provides customers with programming information regarding the products.
# This software is supplied "AS IS" without any warranties and support.
#
# Harald van der Laan assumes no responsibility or liability for the use of the
# software, conveys no license or title under any patent, copyright, or mask
# work right to the product.
#
# Harald van der Laan reserves the right to make changes in the software without
# notification. Harald van der Laan also make no representation or warranty that
# such application will be suitable for the specified use without further
# testing or modification.

""" p2000.py - display the dutch digital emergency services pager system
    usage   : ./p2000.py --help
    requires: internet connection to download messages from http://p2000mobiel.nl """

from __future__ import (print_function, unicode_literals)
from progress.bar import Bar

import sys
import os
import time
import re
import argparse
import configparser as ConfigParser

try:
    from libp2000 import libp2000
except ImportError:
    sys.stderr.write('[-] could not find libp2000.\n')
    sys.exit(1)

def p2000_pp(el):
    # color schema
    fdp = '\033[38;5;9m'
    lfl = '\033[38;5;118m'
    ems = '\033[38;5;220m'
    pdp = '\033[38;5;39m'
    cgd = '\033[38;5;208m'
    rst = '\033[0m'

    if re.match('Ambulance', str(el["call_type"])):
        col = ems
    elif re.match('Brandweer', str(el["call_type"])):
        col = fdp
    elif re.match('Lifeliner', str(el["call_type"])):
        col = lfl
    elif re.match('Politie', str(el["call_type"])):
        col = pdp
    else:
        col = cgd

    ret = '{}{} - {}\n'.format(col, el["date"], el["call_type"])
    ret += '{}{}\n'.format(col, el["message"])
    for i in range(len(el['called'])):
        ret += '{}{}\n' .format(col, el['called'][i])

    ret += '{}' .format(rst)

    return ret


def main(conf):
    """ main function """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', help='clear previous messagesi. works only with -f', default=False, action='store_true')
    parser.add_argument('-f', '--follow', help='follow mode', default=False, action='store_true')
    parser.add_argument('-l', '--lines', help='number of lines', default='5')
    parser.add_argument('-r', '--region', help='security region', default='40')
    args = parser.parse_args()

    numlines = args.lines
    url = conf.get('global', 'baseurl') + conf.get('regions', 'region' + args.region)

    data = libp2000.get_p2000_data(url)
    p2000data = libp2000.convert_to_json(data)

    for _ in range(int(numlines)):
        idx = _
        if args.follow:
            # output the first item last
            idx = int(numlines) - _
        print(p2000_pp(p2000data['p2000'][idx-1]))

    if args.follow:
        refreshtime = int(conf.get('global', 'refreshtime'))
        bar = Bar('Refresh in: ', max=refreshtime)
        olddata = p2000data['p2000']
        try:
            while True:
                newdata = libp2000.convert_to_json(libp2000.get_p2000_data(url))['p2000']
                newdata.reverse()
                diff = [x for x in newdata if x not in olddata]
                if len(diff) > 0:
                    if args.clear:
                        os.system('clear')
                    for item in diff:
                        print(p2000_pp(item))
                olddata = newdata
                bar.goto(0)
                for t in range(refreshtime):
                    bar.next()
                    time.sleep(1)
                bar.clearln()

        except KeyboardInterrupt:
            bar.finish()
            sys.exit(0)

if __name__ == "__main__":
    CONFIG = os.path.dirname(os.path.abspath(__file__)) + '/p2000.cfg'
    CONF = ConfigParser.ConfigParser()
    CONF.read(CONFIG)

    os.system('clear')
    main(CONF)

    sys.exit(0)
