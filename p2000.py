#!/usr/bin/env python

# file     : p2000.py
# purpose  : display digital pager system of the dutch emergency services
#
# author   : harald van der laan
# date     : 2016/11/25
# version  : v2.0.0
#
# changelog:
# - v2.0.0      script rewritten to python
# - =< v1.9.9   Legacy and not supported any more

""" p2000.py - display the dutch digital emergency services pager system

    usage   : ./p2000.py [region code]
    requires: internet connection to download messages from http://p2000mobiel.nl """

import sys
import urllib2
import os
import re

try:
    from p2000lib import p2000
except ImportError:
    sys.stderr.write("[-] could not import p2000lib/p2000.py\n")
    sys.stderr.write("[-] please re-download this script.\n")
    sys.exit(1)

def main():
    """ main function for downloading and displaying the pager messages """
    if len(sys.argv) == 2:
        # undocumented feature, use only when you know the safety regions in 'the netherlands'
        url = 'http://p2000mobiel.nl/' + sys.argv[1] + '/a.html'
    else:
        url = 'http://p2000mobiel.nl/40/geheel-nederland.html'

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
            msg = pager.next()

            msg = re.sub(r'\r\n', '', msg)
            msg = re.sub(r'\)\[', ')\n[', msg)
            msg = re.sub(r'n\[', 'n\n[', msg)
            msg = re.sub(r'd\[', 'd\n[', msg)
            msg = re.sub(r't\[', 't\n[', msg)
            msg = re.sub(r'e\[', 'e\n[', msg)

            p2000msg = p2000.PreprocessMessage(msg)
            p2000.DisplayMessage(p2000msg.msgtype, msg)

    os.remove('p2000.lst')

if __name__ == "__main__":
    main()
    sys.exit(0)
