import time
import datetime
import requests
import bs4
import logging
import traceback
import docx
import os
# this should get 3 atricles from 3 different site and send it to nevet vie gmail.
# FIXME: when the project is operetional i should addfilename='log.txt' to the logging.basicConfig line
logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
# this does everything but front page for davar1
def parsedavar(pagereq):
    davarsoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    # gets headline:
    davartitle = davarsoup.select('.headline')[0].getText()
    # gets author:
    davarauthor = davarsoup.select('.under-headline')[0].getText()
    # gets the content:
    davartext = davarsoup.select('.article-body')[0].getText()
    return (davartitle, davarauthor, davartext)

# TODO: build a parsing func for haaretz. LAST, PROB IMPOSSIBLE.
def parsehaaretz(pagereq):
    haaretzsoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    return

# parses makor1
def parsemakor(pagereq):
    # makor1 is a shit website, says its ISO when its UTF-8.
    pagereq.encoding = 'utf-8'
    makorsoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    # gets headline:
    makortitle = makorsoup.select('h1')[0].getText()
    # gets undertitle:
    makorunder = makorsoup.select('.jeg_post_subtitle')[0].getText()
    # gets author and date:
    makorauthor = makorsoup.select('.jeg_meta_author')[0].getText()
    #gets the content:
    makorcontent = makorsoup.select('.content-inner')[0].getText()
    return (makortitle, makorunder, makorauthor, makorcontent)

# a parsing func for the marker:
def parsemarker(pagereq):
    markersoup = bs4.BeautifulSoup(pagereq.text, 'lxml')
    # gets the headline:
    markertitle = markersoup.select('h1')[0].getText()
    # gets the description:
    markerunder = markersoup.select('p.t-delta')[0].getText()
    # gets author
    markerauthor = markersoup.select('a.js-stat-util-info')[0].get('data-statutil-writer')
    # gets the time
    markertime = markersoup.select('time')[0].get('datetime')
    # gets all the paragraphs
    contentlist = markersoup.select('.t-body-text')
    newlist = []
    for i in contentlist: # loops over the content list to turn it to text from tag.
         newlist.append(i.getText())
    markercontent = ''.join(newlist[3:])
    return (markertitle, markerauthor, markertime, markerunder, markercontent)

    def writefile(fileobject, content):
        for i in content:
            fileobject.write(i)
            return 'Done.'

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
            davarlinks = davarsoup.select('.headline > a') # gets only the links from the page
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

            logging.info('First article: %s' % davarlinks[0].get('href'))
            logging.info('Second article: %s' % davarlinks[1].get('href'))
            logging.info('Third article: %s' % davarlinks[3].get('href'))

            davarfirstcontent = parsedavar(davarfirst) # parse davarfirst:
            logging.info('Davarfirst title: ' + davarfirstcontent[0])
            logging.info('Davarfirst author: ' + davarfirstcontent[1])
            logging.info('Davarfirst text: ' + davarfirstcontent[2][0:50])
            davarsecondcontent = parsedavar(davarsecond) # parse davarsecond:
            logging.info('Davarsecond title: ' + davarsecondcontent[0])
            logging.info('Davarsecond author: ' + davarsecondcontent[1])
            logging.info('Davarsecond text: ' + davarsecondcontent[2][0:50])
            davarthirdcontent = parsedavar(davarthird) # parse davarthird:
            logging.info('Davarthird title: ' + davarthirdcontent[0])
            logging.info('Davarthird author: ' + davarthirdcontent[1])
            logging.info('Davarthird text: ' + davarthirdcontent[2][0:50])
            logging.debug('Got Davar1.')

        except:
            davarfirstcontent = 'error in davar first. check log.'
            davarsecondcontent = 'error in davarsecond. check log.'
            davarthirdcontent = 'error in davarthird. check log.'
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

            logging.info('Makorfirst adress: ' + makorlinks[0].get('href'))
            logging.info('Makorsecond address: ' + makorlinks[1].get('href'))
            logging.info('Makorthird address: ' + makorlinks[2].get('href'))

            # this parses makor1 top 3 articles.
            makorfirstcontent = parsemakor(makorfirst) # makorfirst:
            logging.info('Makorfirst title: ' + makorfirstcontent[0])
            logging.info('Makorfirst under: ' + makorfirstcontent[1][0:50])
            logging.info('Makorfirst author: ' + makorfirstcontent[2])
            logging.info('Makorfirst content: ' + makorfirstcontent[3][0:50])
            makorsecondcontent = parsemakor(makorsecond) # makorsecond:
            logging.info('Makorsecond title: ' + makorsecondcontent[0])
            logging.info('Makorsecond under: ' + makorsecondcontent[1][0:50])
            logging.info('Makorsecond author: ' + makorsecondcontent[2])
            logging.info('Makorsecond content: ' + makorsecondcontent[3][0:50])
            makorthirdcontent = parsemakor(makorthird) # makorthird:
            logging.info('Makorthird title: ' + makorthirdcontent[0])
            logging.info('Makorthird under: ' + makorthirdcontent[1][0:50])
            logging.info('Makorthird author: ' + makorthirdcontent[2])
            logging.info('Makorthird content: ' + makorthirdcontent[3][0:50])
        except:
            makorfirstcontent = 'error in makorfirst. check log.'
            makorsecondcontent = 'error in makorsecond. check log.'
            makorthirdcontent = 'error in makorthird. check log.'
            logging.error(traceback.format_exc())

# gets the article addresses from de marker
        try:
            marker = requests.get('https://www.themarker.com/')
            marker.raise_for_status()
            logging.debug('got De marker front')
            markersoup = bs4.BeautifulSoup(marker.text, 'lxml')
            markertop = markersoup.select('.hero__headline') # top needs different parsing protocole
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
            markerfirstcontent = 'error in markerfirst. check log.'
            markersecondcontent = 'error in markersecond. check log.'
            markerthirdcontent = 'error in markerthird. check log.'
            logging.error(traceback.format_exc())
# TODO: make it one .doc file
        doc = open(os.getcwd() + '\docs\File_%d/%d/%d.txt' % (now.day, now.month, now.year, 'w')
        writefile(doc, davarfirstcontent)
        writefile(doc, davarsecondcontent)
        writefile(doc, davarthirdcontent)
        exit() # to be eliminated when working on the mailing
# TODO: send it to the kindle

        time.sleep(60) # this makes sure it runs once a day

# QUESTION figure out whether you want the program to end?
    if now.year == 2019:
        run = False
# QUESTION send an abortion email when the loop stops?
