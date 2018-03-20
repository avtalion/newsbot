#!/usr/bin/python3
import time
import datetime
import requests
import bs4
import logging
import traceback
# this should get 3 atricles from 3 different site and send it to nevet vie gmail.
# FIXME: when the project is operetional i should addfilename='log.txt' to the logging.basicConfig line
logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
# this does everything but front page for davar1
def parsedavar(address):
    davarsoup = bs4.BeautifulSoup(address.text, 'lxml')
    # gets headline:
    davartitle = davarsoup.select('.headline')[0].getText()
    # gets author:
    davarauthor = davarsoup.select('.under-headline')[0].getText()
    # gets the content:
    davartext = davarsoup.select('.article-body')[0].getText()
    return (davartitle, davarauthor, davartext)

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
            logging.debug('got davar1 front')
            davarsoup = bs4.BeautifulSoup(davar.text, 'lxml')
            headlinelinks = davarsoup.select('.headline > a') # gets only the links from the page
            if len(headlinelinks) == 0:
                raise Exception('No articles found on davar1')

            logging.debug('Matched %d items at davar1' % (len(headlinelinks)))
            # gets the first three article pages and makes sure they are there
            davarfirst = requests.get(headlinelinks[0].get('href'))
            davarfirst.raise_for_status()
            davarsecond = requests.get(headlinelinks[1].get('href'))
            davarsecond.raise_for_status()
            davarthird = requests.get(headlinelinks[3].get('href'))
            davarthird.raise_for_status()

            logging.info('First article: %s' % headlinelinks[0].get('href'))
            logging.info('Second article: %s' % headlinelinks[1].get('href'))
            logging.info('Third article: %s' % headlinelinks[3].get('href'))

            # parse davarfirst:
            davarfirstcontent = parsedavar(davarfirst)
            logging.info('Davarfirst title: ' + davarfirstcontent[0])
            logging.info('Davarfirst author: ' + davarfirstcontent[1])
            logging.info('Davarfirst text: ' + davarfirstcontent[2][0:50])
            # parse davarsecond:
            davarsecondcontent = parsedavar(davarsecond)
            logging.info('Davarsecond title: ' + davarsecondcontent[0])
            logging.info('Davarsecond author: ' + davarsecondcontent[1])
            logging.info('davarsecond text: ' + davarsecondcontent[2][0:50])
            # parse davarthird:
            davarthirdcontent = parsedavar(davarthird)
            logging.info('davarthird title: ' + davarthirdcontent[0])
            logging.info('davarthird author: ' + davarthirdcontent[1])
            logging.info('davarthird text: ' + davarthirdcontent[2][0:50])
            logging.debug('Got davar1.')

        except:
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
            # TODO: parse it so it takes the first 3 articles head and content

        except:
            makor_rishon = 'נמנעה הגישה למקור ראשון'
            logging.error(traceback.format_exc())
# gets the article from the marker
        try:
            marker = requests.get('https://www.themarker.com/')
            marker.raise_for_status()
            logging.debug('got the marker')
            # TODO: parse it so it takes the first 3 articles head and content

        except:
            logging.error(traceback.format_exc())
            marker = 'נמנעה הגישה לדה מרקר'
        exit() # this one to be eliminated once i start working on the .doc
# TODO: make it one .doc file

# TODO: send it to the kindle

        time.sleep(60) # this makes sure it runs once a day

# QUESTION figure out whether you want the program to end?
    if now.year == 2019:
        run = False
# QUESTION send an aboortion email when the loop stops?
