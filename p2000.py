#!/usr/bin/env python

# file     : p2000.py
# purpose  : display digital pager system of the dutch emergency services
#
# author   : harald van der laan
# date     : 2017/02/08
# version  : v2.1.0
#
# changelog:
# - v2.1.0      added refresh modus to script and configuration file
# - v2.0.1      added configuration file for variable urls
# - v2.0.0      script rewritten to python
# - =< v1.9.9   Legacy and not supported any more

""" p2000.py - display the dutch digital emergency services pager system

    usage   : ./p2000.py [region code]
    requires: internet connection to download messages from http://p2000mobiel.nl """

import sys
import urllib2
import os
import re
import time
import platform
import ConfigParser

try:
    from p2000lib import p2000
except ImportError:
    sys.stderr.write("[-] could not import p2000lib/p2000.py\n")
    sys.stderr.write("[-] please re-download this script.\n")
    sys.exit(1)

def main(conf):
    """ main function for downloading and displaying the pager messages """
    if len(sys.argv) == 2:
        # undocumented feature, use only when you know the safety regions in 'the netherlands'
        baseurl = conf.get('global', 'baseurl')
        region = conf.get('regions', 'region' + sys.argv[1])
        url = baseurl + region
    else:
        baseurl = conf.get('global', 'baseurl')
        region = conf.get('global', 'defregion')
        url = baseurl + region

    try:
        req = urllib2.Request(url)
        raw_html = urllib2.urlopen(req)
    except urllib2.HTTPError:
        sys.stderr.write('[-] p2000: could not download content\n')
        sys.exit(1)

    # download webpage
    with open('p2000.lst', 'w+') as dfh:
        for lines in raw_html:
            if re.match('<div class=', lines):
                if not re.match('.*\"date\"', lines) and not re.match('.*\"call_type_', lines):
                    msg = re.sub('<[^>]+>', '', lines)
                    dfh.write(msg)

    with open('p2000.lst', 'r') as pager:
        for dummy in range(35):
            try:
                msg = pager.next()
            except StopIteration:
                break

            msg = re.sub(r'\r\n', '', msg)
            msg = re.sub(r'\)\[', ')\n[', msg)
            msg = re.sub(r'n\[', 'n\n[', msg)
            msg = re.sub(r'd\[', 'd\n[', msg)
            msg = re.sub(r't\[', 't\n[', msg)
            msg = re.sub(r'e\[', 'e\n[', msg)
            msg = re.sub(r'k\[', 'k\n[', msg)

            p2000msg = p2000.PreprocessMessage(msg)
            p2000.DisplayMessage(p2000msg.msgtype, msg)

    os.remove('p2000.lst')

if __name__ == "__main__":
    CONFIG = 'p2000.cfg'

    if os.path.exists(CONFIG):
        CONF = ConfigParser.ConfigParser()
        CONF.read(CONFIG)
    else:
        sys.stderr.write('[-] p2000: could not find CONFIGfile: {}\n' .format(CONFIG))
        sys.exit(1)

    if CONF.get('global', 'refresh') == 'true':
        try:
            while True:
                if platform.system == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')

                main(CONF)
                time.sleep(60)
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        main(CONF)
        sys.exit(0)
