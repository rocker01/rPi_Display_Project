#!/usr/bin/python
# -*- coding:utf-8 -*-
#code adapted by Manu Narang
import sys
import os
import socket
#import commands
import requests


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
#epd.Clear(0xFF)
#

font15 = ImageFont.truetype(os.path.join(picdir, 'Monaco.ttf'), 15)
font16 = ImageFont.truetype(os.path.join(picdir, 'Monaco.ttf'), 16)
font24 = ImageFont.truetype(os.path.join(picdir, 'Monaco.ttf'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Monaco.ttf'), 18)


image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame

draw = ImageDraw.Draw(image)

hostName = socket.gethostname()
ipAddress = socket.gethostbyname(hostName)
#ipAddress2 = commands.getoutput('ifconfig wlan0 | grep "inet " | cut -d " " -f10')

URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"

r = requests.get(url = URL).json()

indCases = str(r['IND']['data'][-1]['total_cases'])[:-2]
indNewCases = str(r['IND']['data'][-1]['new_cases'])[:-2]

canCases = str(r['CAN']['data'][-1]['total_cases'])[:-2]
canNewCases = str(r['CAN']['data'][-1]['new_cases'])[:-2]

usaCases = str(r['USA']['data'][-1]['total_cases'])[:-2]
usaNewCases = str(r['USA']['data'][-1]['new_cases'])[:-2]

draw.text((0, 0), 'IND ' + indCases + ' +' + indNewCases, font=font18, fill=0)
draw.text((0, 20), 'CAN ' + canCases + ' +' + canNewCases, font=font18, fill=0)
draw.text((0, 40), 'USA ' + usaCases + ' +' + usaNewCases, font=font18, fill=0)


draw.text((0, 70), time.strftime("%H:%M:%S   %Y-%m-%d"), font=font16, fill=0)


epd.display(epd.getbuffer(image))

