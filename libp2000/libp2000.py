#!/usr/bin/env python

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
