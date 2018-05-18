#!/usr/bin/python3
import time
from datetime import datetime
import requests
import bs4
import logging
import traceback
import os
# this should get 3 atricles from 3 different site and send it to nevet vie gmail.
# FIXME: when the project is operetional i should addfilename='log.txt' to the logging.basicConfig line
logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


# this does everything but front page for davar1
def parsedavar(pagereq):
    davarsoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    try:
        # gets headline:
        davartitle = davarsoup.select('.headline')[0].getText()
    except:
        davartitle = 'No title found'
        logging.error(traceback.format_exc())
    # gets author:
    try:
        davarauthor = davarsoup.select('.under-headline')[0].getText()
    except IndexError:
        davarauthor = 'No author found'
        logging.error(traceback.format_exc())
    # gets the content:
    try:
        davartext = (davarsoup.select('.article-body > p'))
        davarcontent = ''
        for i in davartext:
            davarcontent = davarcontent + i.getText() + '\n'
    except IndexError:
        davarcontent = 'No text found'
        logging.error(traceback.format_exc())
    return (davartitle, davarauthor, davarcontent)


# parses makor1
def parsemakor(pagereq):
    # makor1 is a shit website, says its ISO when its UTF-8.
    pagereq.encoding = 'utf-8'
    makorsoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    # gets headline:
    try:
        makortitle = makorsoup.select('h1')[0].getText()
    except IndexError:
        makortitle = 'No title found'
        logging.error(traceback.format_exc())
    # gets undertitle:
    try:
        makorunder = makorsoup.select('.jeg_post_subtitle')[0].getText()
    except IndexError:
        makorunder = 'No under found'
        logging.error(traceback.format_exc())
    # gets author and date:
    try:
        makorauthor = makorsoup.select('.jeg_meta_author')[0].getText()
    except IndexError:
        makorauthor = 'No author found'
        logging.error(traceback.format_exc())
    # gets the content:
    try:
        makorcontent = makorsoup.select('.content-inner')[0].getText()
    except IndexError:
        makorcontent = 'No content found'
        logging.error(traceback.format_exc())
    return makortitle, makorunder, makorauthor, makorcontent


# TODO: build a parsing func for the themarker
def parsemarker(pagereq):  # FIXME: something doesn't work here
    markersoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    # gets the headline:
    try:
        markertitle = markersoup.select('h1')[0].getText()
    except IndexError:
        markertitle = 'No title found'
        logging.error(traceback.format_exc())
    # gets the description:
    try:
        markerunder = markersoup.select('p.t-delta')[0].getText()
    except IndexError:
        markerunder = 'No under found'
        logging.error(traceback.format_exc())
    # gets author
    try:
        markerauthor = markersoup.select('a.js-stat-util-info')[0].get('data-statutil-writer')
    except IndexError:
        markerauthor = 'No author found'
        logging.error(traceback.format_exc())
    # gets the time
    try:
        markertime = markersoup.select('time')[0].get('datetime')
    except IndexError:
        markertime = 'No timestamp found'
        logging.error(traceback.format_exc())
    # gets all the paragraphs
    try:
        markercontent = ''
        contentlist = markersoup.select('.t-body-text')
        for i in contentlist:
            if contentlist.index(i) >= 3:
                markercontent = markercontent + i.getText()
    except IndexError:
        markercontent = 'No content found'
        logging.error(traceback.format_exc())
    return markertitle, markerauthor, markertime, markerunder, markercontent


logging.debug('Start of program')
os.chdir('./docs')
run = True
while run:  # program Start
    now = datetime.now()
    if True:  # TODO: uncomment this when ready: now.hour == 7 and now.minute == 0:
        logging.debug('its %s and the script runs' % now)
# takes the page from davar rishon.
        try:
            davar = requests.get('http://www.davar1.co.il/')
            davar.raise_for_status()
            logging.debug('got davar1 front')
            davarsoup = bs4.BeautifulSoup(davar.text, 'lxml')
            davarlinks = davarsoup.select('.headline > a')  # gets only the links from the page
            if len(davarlinks) == 0:
                raise Exception('No articles found on davar1')

            logging.debug('Matched %d items at davar1' % (len(davarlinks)))
            # gets the first three article pages and makes sure they are there
            davarfirst = requests.get(davarlinks[0].get('href'))
            davarfirst.raise_for_status()
            davarsecond = requests.get(davarlinks[1].get('href'))
            davarsecond.raise_for_status()
            davarthird = requests.get(davarlinks[3].get('href'))
            davarthird.raise_for_status()

            logging.info('davarfirst address:: %s' % davarlinks[0].get('href'))
            logging.info('davarsecond address:: %s' % davarlinks[1].get('href'))
            logging.info('davarthird address:: %s' % davarlinks[3].get('href'))

            davar_first_content = parsedavar(davarfirst)  # parse davarfirst:
            logging.info('Davarfirst title: ' + davar_first_content[0])
            logging.info('Davarfirst author: ' + davar_first_content[1])
            logging.info('Davarfirst text: ' + davar_first_content[2][0:50])
            davar_second_content = parsedavar(davarsecond)  # parse davarsecond:
            logging.info('Davarsecond title: ' + davar_second_content[0])
            logging.info('Davarsecond author: ' + davar_second_content[1])
            logging.info('Davarsecond text: ' + davar_second_content[2][0:50])
            davar_third_content = parsedavar(davarthird)  # parse davarthird:
            logging.info('Davarthird title: ' + davar_third_content[0])
            logging.info('Davarthird author: ' + davar_third_content[1])
            logging.info('Davarthird text: ' + davar_third_content[2][0:50])
            logging.debug('Got Davar1.')

        except:
            davar_first_content = 'שגיאה בדבר ראשון. בדוק ביומן אירועים.'
            davar_second_content = 'שגיאה בדבר ראשון. בדוק ביומן אירועים.'
            davar_third_content = 'שגיאה בדבר ראשון. בדוק ביומן אירועים.'
            logging.error(traceback.format_exc())

# gets the article pagereq from makor rishon
        try:
            makor1 = requests.get('https://www.makorrishon.co.il/')
            makor1.raise_for_status()
            makor1.encoding = 'utf-8'
            logging.debug('got makor1 front')
            makorsoup = bs4.BeautifulSoup(makor1.text, 'lxml')
            makorlinks = makorsoup.select('.jeg_post_title > a')
            if len(makorlinks) == 0:
                raise Exception('No articles found on makor1')

            logging.debug('Matched %d items on makor1' % (len(makorlinks)))
            # gets thr first three articles
            makorfirst = requests.get(makorlinks[0].get('href'))
            makorfirst.raise_for_status()
            makorsecond = requests.get(makorlinks[1].get('href'))
            makorsecond.raise_for_status()
            makorthird = requests.get(makorlinks[2].get('href'))
            makorthird.raise_for_status()

            logging.info('Makorfirst address: ' + makorlinks[0].get('href'))
            logging.info('Makorsecond address: ' + makorlinks[1].get('href'))
            logging.info('Makorthird address: ' + makorlinks[2].get('href'))

            # this parses makor1 top 3 articles.
            makorfirstcontent = parsemakor(makorfirst)  # makorfirst:
            logging.info('Makorfirst title: ' + makorfirstcontent[0])
            logging.info('Makorfirst under: ' + makorfirstcontent[1][0:50])
            logging.info('Makorfirst author: ' + makorfirstcontent[2])
            logging.info('Makorfirst content: ' + makorfirstcontent[3][0:50])
            makorsecondcontent = parsemakor(makorsecond)  # makorsecond:
            logging.info('Makorsecond title: ' + makorsecondcontent[0])
            logging.info('Makorsecond under: ' + makorsecondcontent[1][0:50])
            logging.info('Makorsecond author: ' + makorsecondcontent[2])
            logging.info('Makorsecond content: ' + makorsecondcontent[3][0:50])
            makorthirdcontent = parsemakor(makorthird)  # makorthird:
            logging.info('Makorthird title: ' + makorthirdcontent[0])
            logging.info('Makorthird under: ' + makorthirdcontent[1][0:50])
            logging.info('Makorthird author: ' + makorthirdcontent[2])
            logging.info('Makorthird content: ' + makorthirdcontent[3][0:50])
        except:
            makorfirstcontent = 'שגיאה במקור ראשון. בדוק יומן אירועים'
            makorsecondcontent = 'שגיאה במקור ראשון. בדוק יומן אירועים'
            makorthirdcontent = 'שגיאה במקור ראשון. בדוק יומן אירועים'
            logging.error(traceback.format_exc())

# gets the article addresses from de marker
        try:
            marker = requests.get('https://www.themarker.com/')
            marker.raise_for_status()
            logging.debug('got De marker front')
            markersoup = bs4.BeautifulSoup(marker.text, 'lxml')
            markertop = markersoup.select('.hero__headline')  # top needs different parsing protocole
            if len(markertop) == 0:
                raise Exception('top not found on demarker')
            markerfirst = requests.get('https://www.themarker.com' + markertop[0].get('href'))
            markerlinks = markersoup.select('article > a')
            # the marker has 2 article before the second top 3
            markersecond = requests.get('https://www.themarker.com' + markerlinks[2].get('href'))
            markerthird = requests.get('https://www.themarker.com' + markerlinks[3].get('href'))

            # TODO: parse it so it takes the first 3 articles head and content
            # marker first:
            markerfirstcontent = parsemarker(markerfirst)
            logging.info('markerfirst title: ' + markerfirstcontent[0])
            logging.info('markerfirst author: ' + markerfirstcontent[1])
            logging.info('markerfirst time: ' + markerfirstcontent[2])
            logging.info('markerfirst under: ' + markerfirstcontent[3][:50])
            logging.info('markerfirst text: ' + markerfirstcontent[4][:50])
            # marker second:
            markersecondcontent = parsemarker(markersecond)
            logging.info('markersecond title: ' + markersecondcontent[0])
            logging.info('markersecond author: ' + markersecondcontent[1])
            logging.info('markersecond time: ' + markersecondcontent[2])
            logging.info('markersecond under: ' + markersecondcontent[3][:50])
            logging.info('markersecond text: ' + markersecondcontent[4][:50])
            # marker third:
            markerthirdcontent = parsemarker(markerthird)
            logging.info('markerthird title: ' + markerthirdcontent[0])
            logging.info('markerthird author: ' + markerthirdcontent[1])
            logging.info('markerthird time: ' + markerthirdcontent[2])
            logging.info('markerthird under: ' + markerthirdcontent[3][:50])
            logging.info('markerthird text: ' + markerthirdcontent[4][:50])

        except:
            logging.error(traceback.format_exc())
            markerfirstcontent = 'error in markerfirst. check log.'
            markersecondcontent = 'error in markersecond. check log.'
            markerthirdcontent = 'error in markerthird. check log.'
# TODO: make it one .txt file
        doc = open('news_%d-%d-%d.txt' % (now.day, now.month, now.year), 'w')
        # writing davar1 to file
        doc.write('דבר ראשון:\n')
        doc.write(''.join(davar_first_content))
        logging.info('Wrote davarfirst to file.')
        doc.write(''.join(davar_second_content))
        logging.info('Wrote davarsecond to file')
        doc.write(''.join(davar_third_content))
        logging.info('Wrote davarthird to file')
        # TODO: write makor1 to file
        doc.write('מקור ראשון:\n')
        doc.write(''.join(makorfirstcontent))
        logging.info('Wrote makorfirst to file')
        # TODO: write demarker
        doc.write('דה מרקר:\n')

        doc.close()  # this closes the file.

# TODO: send it to the kindle
        exit()  # this one to be eliminated

        time.sleep(60)  # this makes sure it runs once a day
        # TODO: write a script that deletes the
# QUESTION figure out whether you want the program to end?
    if now.year == 2019:
        run = False
# QUESTION send an abortion email when the loop stops?
