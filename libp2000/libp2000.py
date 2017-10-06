#!/usr/bin/env python

# File   : ./libp2000/libp2000.py
# Purpose: Library file for the p2000.py script
#
# Auhtor : Harald van der Laan
# Date   : 2017/10/06
# Version: v1.0.1
#
# Requirements:
#  - requests
#  - bs4
#  - working internet connection
#
# Changelog:
#  - v1.0.1     Created new header in python files                       Harald
#  - v1.0.0     Initial version                                          Harald
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

""" libp2000.py - python function file for processing p2000 pager messages """

import sys
import re
import json
import requests
import bs4

def get_p2000_data(url):
    """ function to get p2000 data from the internet.
    this function requires: requests and bs4.BeautifulSoup """

    try:
        html = requests.get(url)
    except requests.exceptions.ConnectionError:
        sys.stderr.write('[-] connection failed.\n')
        sys.exit(1)

    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    data = soup.findAll('div', {'class': ['date', 'message', 'called',
                                          'call_type_1', 'call_type_2', 'call_type_3',
                                          'call_type_4', 'call_type_5', 'call_type_6',
                                          'call_type_7', 'call_type_8', 'call_type_9']})

    return data

def convert_to_json(data):
    """ function to convert data to json formatted data.
        this dunction requires: re and json """

    jsondata = '{"p2000": ['

    # matching all relevant lines.
    for line in data:
        if re.match('.*\"date', str(line)):
            line = '{"date": "' + str(line) + '", '
        if re.match('.*\"call_type_', str(line)):
            line = '"call_type": "' + str(line) + '", '
        if re.match('.*\"message', str(line)):
            line = '"message": "' + str(line) + '", '
        if re.match('.*\"called', str(line)):
            line = '"called": ["' + str(line) + '"]},'

        # substitute <br/> to , for valid json format
        line = re.sub('<br/>', '", "', str(line))
        # remove other html taggs
        line = re.sub('<[^>]+>', '', str(line))

        jsondata = jsondata + line

    # create valid json closing
    jsondata = jsondata[:-1] + ']}'

    return json.loads(jsondata)
