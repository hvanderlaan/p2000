#!/usr/bin/env python

# file     : p2000.py
# purpose  : display digital pager system of the dutch emergency services
#
# author   : harald van der laan
# date     : 2017/10/05
# version  : v2.2.0
#
# changelog:
# - v2.2.1      Fixed unicode bug
# - v2.2.0      recode with nicer code
# - v2.1.0      added refresh modus to script and configuration file
# - v2.0.1      added configuration file for variable urls
# - v2.0.0      script rewritten to python
# - =< v1.9.9   Legacy and not supported any more

""" p2000.py - display the dutch digital emergency services pager system
    usage   : ./p2000.py --help
    requires: internet connection to download messages from http://p2000mobiel.nl """

from __future__ import (print_function, unicode_literals)

import sys
import os
import time
import re
import argparse
import ConfigParser

try:
    from libp2000 import libp2000
except ImportError:
    sys.stderr.write('[-] could not find libp2000.\n')
    sys.exit(1)

def main(conf):
    """ main function """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region', help='security region', default='40')
    parser.add_argument('-l', '--lines', help='number of lines', default='5')
    args = parser.parse_args()

    numlines = args.lines
    url = conf.get('global', 'baseurl') + conf.get('regions', 'region' + args.region)

    # color schema
    fdp = '\033[38;5;9m'
    lfl = '\033[38;5;118m'
    ems = '\033[38;5;220m'
    pdp = '\033[38;5;39m'
    cgd = '\033[38;5;208m'
    rst = '\033[0m'

    data = libp2000.get_p2000_data(url)
    p2000data = libp2000.convert_to_json(data)

    for _ in xrange(int(numlines)):
        if re.match('Ambulance', str(p2000data['p2000'][_]["call_type"])):
            col = ems
        elif re.match('Brandweer', str(p2000data['p2000'][_]["call_type"])):
            col = fdp
        elif re.match('Lifeliner', str(p2000data['p2000'][_]["call_type"])):
            col = lfl
        elif re.match('Politie', str(p2000data['p2000'][_]["call_type"])):
            col = pdp
        else:
            col = cgd

        print('{}{} - {}'. format(col, p2000data['p2000'][_]["date"],
                                  p2000data['p2000'][_]["call_type"]))
        print('{}{}' .format(col, p2000data['p2000'][_]["message"]))
        for i in xrange(len(p2000data['p2000'][_]['called'])):
            print('{}{}' .format(col, p2000data['p2000'][_]['called'][i]))

        print('{}' .format(rst))

if __name__ == "__main__":
    CONF = ConfigParser.ConfigParser()
    CONF.read('p2000.cfg')

    if CONF.get('global', 'refresh') == 'true':
        try:
            while True:
                os.system('clear')
                main(CONF)
                time.sleep(int(CONF.get('global', 'refreshtime')))
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        main(CONF)

    sys.exit(0)
