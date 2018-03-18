#!/usr/bin/python3
import time
import datetime
import requests
import bs4
import logging
import traceback
# this should get 3 atricles from 3 different site and send it to nevet vie gmail.
logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

logging.debug('Start of program')
run = True
while run:
    now = datetime.datetime.now()
    if True:  # now.hour == 7 and now.minute == 0: runs the code at seven
        logging.debug('its %s and the script runs' % now)
# takes the page from davar rishon.
        try:
            davar = requests.get('http://www.davar1.co.il/')
            davar.raise_for_status()
            logging.debug('got davar1')
            davarsoup = bs4.BeautifulSoup(davar.text, 'lxml')
            headlinelinks = davarsoup.select('.headline > a') # gets only the links from the page
            logging.info('Matched %d items at davar1' % (len(headlinelinks)))
            # gets the first three article pages
            davarfirst = requests.get(headlinelinks[0].get('href'))
            davarsecond = requests.get(headlinelinks[1].get('href'))
            davarthird = requests.get(headlinelinks[2].get('href'))
            logging.info('\nfirst article: %s\nsecond article: %s\nthird article: %s' % (headlinelinks[0], headlinelinks[1], headlinelinks[2]))
            # TODO take the articles and the title to them

        except:
            davar = 'נמנעה הגישה לדבר ראשון'
            logging.error(traceback.format_exc())
# takes a page from haaretz
        try:
            haaretz = requests.get('https://www.haaretz.co.il/')
            haaretz.raise_for_status()
            logging.debug('got haaretz')
             # TODO parse it so it takes the first 3 articles head and content

        except:
            haaretz = 'נמנעה הגישה לעיתון הארץ'
            logging.error(traceback.format_exc())

# gets the article from makor rishon
        try:
            makor_rishon = requests.get('https://www.makorrishon.co.il/')
            makor_rishon.raise_for_status()
            logging.debug('got makor rishon')
            # TODO parse it so it takes the first 3 articles head and content

        except:
            makor_rishon = 'נמנעה הגישה למקור ראשון'
            logging.error(traceback.format_exc())
# gets the article from the marker
        try:
            marker = requests.get('https://www.themarker.com/')
            marker.raise_for_status()
            logging.debug('got the marker')
            # TODO parse it so it takes the first 3 articles head and content

        except:
            logging.error(traceback.format_exc())
            marker = 'נמנעה הגישה לדה מרקר'
        exit() # this one to be eliminated once i start working on the .doc
# TODO make it one .doc file

# TODO send it to the kindle

        time.sleep(60) # this makes sure it runs once a day

# QUESTION figure out whether you want the program to end?
    if now.year == 2019:
        run = False
# QUESTION send an aboortion email when the loop stops?
