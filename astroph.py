#!/usr/bin/env python
# encoding: utf-8
"""
A module to generate HTML code using specified ArXiV file IDs.

The main function is:
   docoffee -- read in a file of arxiv IDs or interesting URLs, and
               write HTML code to specified file.

There should be no need to edit this file or any of the asssociated parsing
functions (get*.py). There is a wrapper script, runcoffee.py, that does most
of the front-end organization and contains the user changable variables.

Initially created on 2010-02-05 at UCLA by Ian J. Crossfield and Nathaniel
Ross. Modified by Ryan T. Hamilton at New Mexico State University.

This version under development by Abhimat K. Gautam at UCLA.

Contribute or fork on GitHub at https://github.com/abhimat/AstroCoffee
"""
# 2010-10-20       RTH: v0.98: Spun off parsers into own files.  Removed all
#                                changes to the CHANGELOG/online repository

__version__ = '0.98.9'


class preprint(object):
    """Empty object container for preprints"""
    def __init__(self):
        self.url = ''
        self.author = ''
        self.numauth = ''
        self.title = ''
        self.date = ''
        self.abstract = ''
        self.subject = ''
        self.comments = ''
        self.sources = ''
        self.commentid = ''
        self.errors = '0'


def getunique(seq):
    """Take an input list and return list of unique elements, order preserved
    """
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked

# Takes an arxiv pdf link and extracts the id
# assumes all arxiv links of the form "asdfasdfadsf/pdf/idnumber.pdf"
def clean_arxiv_id(id):
    pdf_ind = id.find("pdf/")
    id = id.rstrip('.pdf')  # Remove .pdf at end, if there
    id = id[pdf_ind + 4:]   # Extract arXiv id from remaining text
    return id

def getinfo(id, server='http://arxiv.org/abs/'):
    """Take an ArXiV ID and return the title, authors, abstract, sub. date

    INPUT:
       id -- (str): ArXiV ID (e.g. '1002.0504v1' or 1002.0504)
              _OR_
             (str) URL, from which TITLE tag will be extracted.

    OUTPUT:
       a preprint-class object.
    """
    from getaandainfo import getaandainfo
    from getadsinfo import getadsinfo
    from getarxivinfo import getarxivinfo
    from getmnrasinfo import getmnrasinfo
    from getvixrainfo import getvixrainfo
    from getnatureinfo import getnatureinfo
    from getscienceinfo import getscienceinfo
    from getphysicstodayinfo import getphysicstodayinfo
    from get_prl_info import get_prl_info
    from getvoxchartainfo import getvoxchartainfo
    from getwebinfo import getwebinfo
    import urllib2, cookielib
    
    servererr = False
    # Set up the ID
    id = str(id).strip()
    
    
    # Clean up various paper IDs before continuing
    ## Check if arXiv ID is a pdf
    if id.find("pdf") > -1 and id.find("arxiv.org") > -1:
        id = clean_arxiv_id(id)
    ## Check if Science ID is not link to full article
    if id.find('science.sciencemag.org') > -1 and id.find('.full') == -1:
        id = id + '.full'
    ## Check if PRL submission is a pdf
    if id.find("/pdf/") > -1 and id.find("journals.aps.org/prl") > -1:
        id = id.replace('/pdf/', '/abstract/')
    
    # Check for the various types of arXiv identifiers
    try:
        # Check for plain numbers with no lead/trail and a period in it
        if (id.find('.') > -1):
            idnum = float(id[0:9])
            isValidArxiv = len(id) >= 9
            # Ok, it's just a number so put the proper url stuff in front of it
            id = server + id
            servererr = False
    except:
        # Ok, wasn't just numbers.  Look for arxiv:###... style, but not
        #   valid arxiv.org addresses that were submitted
        if (id.find('arxiv')>-1 or id.find('arXiv')>-1) and \
           (id.find('.org') == -1) and \
           (id.find('.gov') == -1):
            isValidArxiv = True
            id = server + id
        elif (id.find('astro-ph') > -1) and \
           (id.find('.org') == -1) and \
           (id.find('.gov') == -1):
            isValidArxiv = True
            id = 'http://arxiv.org/abs/' + id
        else:
            isValidArxiv = False
    
    # HTTP request for a webpage URL
    try:
        ## Cookies Support
        cookies = cookielib.LWPCookieJar()
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
            ]
        opener = urllib2.build_opener(*handlers)
    
        ## Add headers to HTTP request so don't get 403 error
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
    
    
        request = urllib2.Request(id, headers=hdr)
    
        html = opener.open(request).read()
        urlpage = id  # For compatibility down lower in the code
    except urllib2.HTTPError, e:
        print e.code
        html = e.read()
        urlpage = id
        servererr = True
    except:
        # Hm...didn't open, and not a 404 or something; try adding http://
        if (id.startswith('http://') is False):
            urlpage = 'http://' + id
            try:
                html = urllib2.urlopen(urlpage).read()
            except:
                # Ok...try adding www. if it's not there
                if (urlpage.startswith('http://www.') is False):
                    urlpage = 'http://www.' + id
                try:
                    html = urllib2.urlopen(urlpage).read()
                except:
                    html = '<html><head>' + \
                           '<title>BAD LINK: ' + id + \
                           '</title>' + \
                           '</head><body></body></html>'
                    servererr = True
        else:
            html = '<html><head>' + \
                   '<title>BAD LINK: ' + id + \
                   '</title>' + \
                   '</head><body></body></html>'
    
    if servererr == False:
        # Nature Article
        if urlpage.find('nature.com')>-1:
            if urlpage.find('nature.com/news/')>-1:
                thispaper = getwebinfo(urlpage, html)
                if thispaper.errors == '0':
                    thispaper.errors = 'Success reading ' + urlpage
                else:
                    thispaper.errors = 'Some ERRORS reading ' + urlpage
                thispaper.id = ''
            else:
                thispaper = getnatureinfo(urlpage, html)
                if thispaper.errors == '0':
                    thispaper.errors = 'Success reading ' + urlpage
                else:
                    thispaper.errors = 'Some ERRORS reading ' + urlpage
                thispaper.id = ''
        # ADS Result
        elif urlpage.find('adsabs.harvard.edu')>-1:
            thispaper = getadsinfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # arXiv Article
        elif urlpage.find('arxiv.org')>-1    or \
             urlpage.find('xxx.lanl.gov')>-1 or \
             (isValidArxiv): 
            thispaper = getarxivinfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # A&A Article
        elif urlpage.find('aanda.org')>-1:
            thispaper = getaandainfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # MNRAS Article
        elif urlpage.find('mnras.oxfordjournals.org')>-1:
            thispaper = getmnrasinfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # Science Article
        elif urlpage.find('science.sciencemag.org')>-1:
            thispaper = getscienceinfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # Physics Today Article
        elif urlpage.find('physicstoday.scitation.org')>-1:
            thispaper = getphysicstodayinfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # Physical Review Letters Article
        elif urlpage.find('journals.aps.org/prl/')>-1:
            thispaper = get_prl_info(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # Vox Charta Article
        elif urlpage.find('voxcharta.org')>-1: 
            thispaper = getvoxchartainfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # viXra Article
        elif urlpage.find('vixra.org')>-1: 
            thispaper = getvixrainfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
        # Anything Else
        else: 
            thispaper = getwebinfo(urlpage, html)
            if thispaper.errors == '0':
                thispaper.errors = 'Success reading ' + urlpage
            else:
                thispaper.errors = 'Some ERRORS reading ' + urlpage
            thispaper.id = ''
    # Error Handler
    else:
        thispaper = getwebinfo(urlpage, html)
        thispaper.errors = 'ERRORS reading ' + id
        thispaper.id = ''
        thispaper.url = id
    
    return thispaper


def readlist(filelist, sleep=60):
    """Get data for all papers with IDs or URLs specified.

    INPUT:
        filelist:  one of the following:
           (list) python list of IDs for astroph.getinfo
           (str) filename of an ascii file containing IDs

    OPTIONAL INPUT:
        sleep -- (float) number of seconds to wait between URL
                 requests, so aRxIv doesn't think you're a robot and
                 ban your connection.

    OUTPUT:
        a list of preprint-class objects
    """
    import time
    papers = []
    errors = ''

    if isinstance(filelist, list):
        ids = filelist
    else:  # Must be the name of a file to read:
        ids, errors = read_file(filelist)
    
    for id in ids:
        if len(id) > 5:
            thispaper = getinfo(id)
            errors = errors + thispaper.errors + "\n"
            if isinstance(thispaper, preprint):
                papers.append(thispaper)
                time.sleep(sleep)

    return errors, papers

def read_file(file):
    """Get data for all papers with IDs or URLs specified.

    INPUT:
        filelist:   (str) filename of an ascii file containing IDs
    
    OUTPUT:
        a python list of individual paper IDs
    """
    ids = []
    errors = ''
    
    try:
        f = open(file, 'r')
        ids = f.readlines()
        f.close()
        
        new_ids = []
        for cur_id in ids:
            cur_id = cur_id.rstrip('\n')
            cur_id = cur_id.rstrip('\r')
            new_ids.append(cur_id)
        ids = new_ids
        
    except:
        errors = "Could not open file: %s" % filelist
        # print "Could not open file: %s" % filelist
        ids = ['']
    
    return ids, errors

def read_volunteers_file(file):
    try:
        f = open(file, 'r')
        
        lines = f.readlines()
        if len(lines) > 0:
            lines = lines[1:]
        
        f.close()
        
        papers_volunteers = {}
    
        for line_index in range(len(lines) / 2):
            cur_id = lines[line_index * 2].rstrip('\n').rstrip('\r')
            cur_vol = lines[line_index * 2 + 1].rstrip('\n').rstrip('\r')
        
            if cur_id in papers_volunteers:
                papers_volunteers[cur_id].append(cur_vol)
            else:
                papers_volunteers[cur_id] = [cur_vol]
    except:
        papers_volunteers = {}
    
    return papers_volunteers
    

def paper_lists_checker(papers_ids, papers_discussed_ids, papers_next_ids):
    # Make sure papers on discussed list are in the original paper lists (i.e. not from previous weeks)
    new_papers_discussed_ids = []
    
    for paper_id in papers_discussed_ids:
        if (paper_id in papers_ids) or (paper_id in papers_next_ids):
            new_papers_discussed_ids.append(paper_id)
    
    # Edit list of paper IDs, removing those already discussed
    new_papers_ids = []

    for paper_id in papers_ids:
        if not(paper_id in new_papers_discussed_ids):
            new_papers_ids.append(paper_id)
    
    # Edit list of next week's paper IDs, removing those already discussed
    new_papers_next_ids = []
    
    for paper_id in papers_next_ids:
        if not(paper_id in new_papers_discussed_ids):
            new_papers_next_ids.append(paper_id)
    
    # Return the new lists
    return new_papers_ids, new_papers_discussed_ids, new_papers_next_ids

def getnextduedate(d, h, m):
    """Get the next due date for meeting.

    INPUT:
        d:  datetime object day of the week to meet
        h:  datetime object hour of day to meet (24h)
        m:  datetime object minute of hour to meet

    OUTPUT:
        datetime of next meeting
    """

    import datetime
    from dateutil.relativedelta import relativedelta, \
        MO, TU, WE, TH, FR, SA, SU

    today = datetime.datetime.now()
    nextmeet1 = today+relativedelta(weeks=+1, weekday=d, hour=h+1,
                                    minute=m, second=0, microsecond=0)
    nextmeet2 = today+relativedelta(weekday=d, hour=h+1, minute=m, second=0,
                                    microsecond=0)
    msg = ''

    if abs(nextmeet2.day-today.day) < 1 and today < nextmeet2:
        nextmeet = nextmeet2
        msg = "Less than one day difference, so the next meeting is today"
    elif today < nextmeet2:
        nextmeet = nextmeet2
    else:
        nextmeet = nextmeet1

    return msg, nextmeet


def getprevduedate(d, h, m):
    """Get the previous date for meeting.

    INPUT:
        d:  datetime object day of the week to meet
        h:  datetime object hour of day to meet (24h)
        m:  datetime object minute of hour to meet

    OUTPUT:
        datetime of the previous meeting
    """

    import datetime
    from dateutil.relativedelta import relativedelta, \
        MO, TU, WE, TH, FR, SA, SU

    # Get current date
    today = datetime.datetime.now()
    prevmeet1 = today+relativedelta(weeks=-1, weekday=d, hour=h+1, minute=m,
                                    second=0, microsecond=0)
    prevmeet2 = today+relativedelta(weekday=d, hour=h+1, minute=m, second=0,
                                    microsecond=0)
    msg = ''

#    print prevmeet1, prevmeet2

    if abs(prevmeet2.day-today.day) < 1 and today > prevmeet2:
        prevmeet = prevmeet2
        msg = "Less than one day difference, so the last meeting was today"
    else:
        prevmeet = prevmeet1

    return msg, prevmeet


def makeheader(day, hour, min, php=False):
    """Return the HTML header info.  If specified, use PHP and submission form.
    """

    import datetime
    from dateutil.relativedelta import relativedelta, \
        MO, TU, WE, TH, FR, SA, SU
    
    head = []
    head_next = []
    
    titleString1 = '<article class="block small">'
    
    # If there is only one meeting
    # Need this dummy return value because of the way I write the status file
    mgs = ''
    msg, nextdate = getnextduedate(day, hour, min)#+relativedelta(minutes=-60)
    nextdate = nextdate + relativedelta(hours=-1)
    datestr = nextdate.strftime('%a, %b %d, %Y')
    datestr_next = (nextdate + relativedelta(days=+7)).strftime('%a, %b %d, %Y')

    timestr = nextdate.strftime('%I:%M %p')

    titleString2 = '<center><p>Suggested papers for<br><strong>{0}</strong> at <strong>{1}</strong></p></center>\n'.format(datestr, timestr)
    titeString2_next = '<hr><center><p>Suggested papers for<br><strong>{0}</strong> at <strong>{1}</strong></p></center>\n'.format(datestr_next, timestr)

    # If there are two meetings, use following
    ## Get previous date astro-ph coffee is held in week
    nextdate_early_0 = nextdate+relativedelta(days=-1)
    datestr_early_0 = nextdate_early_0.strftime('%a, %b %d, %Y')
    datestr_next_early_0 = (nextdate_early_0 + relativedelta(days=+7)).strftime('%a, %b %d, %Y')

    titleString2 = '<center><p>Suggested papers for<br><strong>{0}</strong> and <strong>{1}</strong> at <strong>{2}</strong></p></center>\n'.format(datestr_early_0, datestr, timestr)
    titleString2_next = '<hr><center><p>Suggested papers for<br><strong>{0}</strong> and <strong>{1}</strong> at <strong>{2}</strong></p></center>\n'.format(datestr_next_early_0, datestr_next, timestr)
    
    # If there are three meetings, use following
    ## Get previous date astro-ph coffee is held in week
    nextdate_early_1 = nextdate+relativedelta(days=-3)
    datestr_early_1 = nextdate_early_1.strftime('%a, %b %d, %Y')
    datestr_next_early_1 = (nextdate_early_1 + relativedelta(days=+7)).strftime('%a, %b %d, %Y')
    
    titleString2 = '<center><p>Suggested papers for<br><strong>{0}</strong> at <strong>11 am</strong><br><strong>{1}</strong> at <strong>1 pm</strong><br><strong>{2}</strong> at <strong>11 am</strong></p></center>\n'.format(datestr_early_1, datestr_early_0, datestr, timestr)
    titleString2_next = '<hr><center><p>Suggested papers for<br><strong>{0}</strong>,  <strong>{1}</strong>, and <strong>{2}</strong></p></center>\n'.format(datestr_next_early_1, datestr_next_early_0, datestr_next, timestr)
    
    
    # Construct header from title strings
    
    head.append(titleString1)
    head.append(titleString2)
    
    head_next.append(titleString1)
    head_next.append(titleString2_next)
    
    head.append('</article>\n')
    head_next.append('</article>\n')

    return head, head_next


def makefooter(php=False):
    """
    Return the HTML footer (list of str).  If called, append PHP scripting.
    """

    from time import localtime
    f = []
    yr, mo, day, hr, min, sec, wd, yd, ii = localtime()
    f.append("<article class=\"block\">")
    f.append('<hr><center><p class="small">')
    # f.append("<a href='http://astronomy.nmsu.edu/rthamilt/astrocoffee/'>")
    # f.append("astroph.py v%s</a> based on the " % __version__)
    # f.append("<a href='http://www.astro.ucla.edu/~ianc/astroph.shtml'>")
    # f.append("original astroph.py</a>.  ")
    f.append("Updated %i/%02i/%02i %02i:%02i:%02i</p></center>" %
            (yr, mo, day, hr, min, sec))
    f.append("</article>")
    
    foot = [line+'\n' for line in f]

    return foot


def makehtml(papers, papers_ids, papers_discussed, papers_discussed_ids, papers_next, papers_next_ids, papers_volunteers, day, hour, min, idcomments=False, php=False):
    """Return HTML code for a public ArXiV web page from paper list.

    INPUT:
       papers -- (list) python list of preprint-class objects.

    OPTIONAL INPUT:
       php -- (bool) whether to generate HTML containing PHP scripting
                for paper submissions

    OUTPUT:
       html -- HTML code for generating a web page
    """

    import time
    import re

    # Generate header
    h, h_next = makeheader(day, hour, min, php=php)

    # Generate footer
    f = makefooter(php=php)

    # Generate text from preprints
    body = []
    date = ''
    
    ## Write out the newest papers (papers_next) first
    if len(papers_next) > 0:
        paper_indices = range(len(papers_next))
        
        # body = body + h_next
        
        for paper_index in reversed(paper_indices):
            paper = papers_next[paper_index]
            
            ## Constructing action text
            paper_id = papers_next_ids[paper_index]
            
            volunteer_text = '<a href="http://coffee.astro.ucla.edu/volunteer/volunteer.php?ID={0}">Volunteer to discuss</a><br>'.format(paper_id)
            if paper_id in papers_volunteers:
                cur_vols = papers_volunteers[paper_id]
                vols_names = cur_vols[0]
                if len(cur_vols) > 1:
                    for vol in cur_vols[1:]:
                        vols_names += ', {0}'.format(vol)
            
                volunteer_text = 'Volunteers: {0} | <a href="http://coffee.astro.ucla.edu/volunteer/volunteer.php?ID={1}">Volunteer to discuss</a><br>'.format(vols_names, paper_id)
        
            discussed_link = '<a href="http://coffee.astro.ucla.edu/discussed/discussed.php?ID={0}">Mark paper as discussed</a>'.format(paper_id)
            
            action_text = '<p class="small">' + volunteer_text + discussed_link + '</p>'
                
        
            date = paper.date
            if isinstance(paper, preprint):
                if paper.errors.startswith("Success"):
                    if paper.sources != '':
                        if date != "":
                            body.append('<article class="block">')
                            body.append('<div class="date small">%s</div>' % paper.date)
                        # Remove any stray/extra whitespaces
                        paper.sources = paper.sources.lstrip()
                        paper.sources = paper.sources.rstrip()
                        body.append('<div class="links small">[ %s ]</div>' %
                                    paper.sources)
                        title = '<h3><a href="%s">%s</a></h3>' \
                                % (paper.url, paper.title)
                    else:
                        if date != "":
                            body.append('<article class="block">')
                            body.append('<div class="date small">%s</div>' % paper.date)
                        title = '<h3><a href="%s">%s</a></h3>' % (paper.url, paper.title)
                    body.append('%s' % title)
                    if paper.numauth > 5 and \
                       paper.author != "Error Grabbing Authors":
                        authremain = paper.numauth-5
                        aexstring = ", + " + str(authremain) + " more"
                        paper.author = paper.author + aexstring
                    body.append('<div class="authors small">%s</div>' % paper.author)
                    # Limit the length of the abstract displayed, and if its
                    #   shorter then just display the whole thing
                    abslength = 500
                    # Hopefully remove links and other HTML things in there
                    if len(paper.abstract) > abslength:
                        paper.shortabs = paper.abstract[0:abslength] + '...'
                        paper.shortabs = paper.shortabs.rstrip()
                    else:
                        paper.shortabs = paper.abstract
                    paper.shortabs = paper.shortabs.lstrip()
                    paper.shortabs = paper.shortabs.rstrip()
                    body.append('<div id="abstract"><p>%s</p></div>' % paper.shortabs)
                    body.append(action_text)
                    body.append('</article>')
                else:
                    body.append('<article class="block">')
                    if (paper.url.find('.pdf') > -1):
                        paper.date = "Please Do NOT Submit Direct PDF Links:"
                    else:
                        paper.date = "Unknown Submission/Link:"
                    body.append('<div class="date small">%s</div>' % paper.date)
                    title = '<h3><a href="%s">%s</a></h3>' % (paper.url, paper.url)
                    body.append('%s' % title)
                    body.append(discussed_link)
                    body.append('</article>')
    
    ## Write out current papers (papers)
    paper_indices = range(len(papers))
    
    for paper_index in reversed(paper_indices):
        paper = papers[paper_index]
        
        ## Constructing action text
        paper_id = papers_ids[paper_index]
        
        volunteer_text = '<a href="http://coffee.astro.ucla.edu/volunteer/volunteer.php?ID={0}">Volunteer to discuss</a><br>'.format(paper_id)
        if paper_id in papers_volunteers:
            cur_vols = papers_volunteers[paper_id]
            vols_names = cur_vols[0]
            if len(cur_vols) > 1:
                for vol in cur_vols[1:]:
                    vols_names += ', {0}'.format(vol)
            
            volunteer_text = 'Volunteers: {0} | <a href="http://coffee.astro.ucla.edu/volunteer/volunteer.php?ID={1}">Volunteer to discuss</a><br>'.format(vols_names, paper_id)
        
        discussed_link = '<a href="http://coffee.astro.ucla.edu/discussed/discussed.php?ID={0}">Mark paper as discussed</a>'.format(paper_id)
        
        action_text = '<p class="small">' + volunteer_text + discussed_link + '</p>'
        
        date = paper.date
        if isinstance(paper, preprint):
            if paper.errors.startswith("Success"):
                if paper.sources != '':
                    if date != "":
                        body.append('<article class="block">')
                        body.append('<div class="date small">%s</div>' % paper.date)
                    # Remove any stray/extra whitespaces
                    paper.sources = paper.sources.lstrip()
                    paper.sources = paper.sources.rstrip()
                    body.append('<div class="links small">[ %s ]</div>' %
                                paper.sources)
                    title = '<h3><a href="%s">%s</a></h3>' \
                            % (paper.url, paper.title)
                else:
                    if date != "":
                        body.append('<article class="block">')
                        body.append('<div class="date small">%s</div>' % paper.date)
                    title = '<h3><a href="%s">%s</a></h3>' % (paper.url, paper.title)
                body.append('%s' % title)
                if paper.numauth > 5 and \
                   paper.author != "Error Grabbing Authors":
                    authremain = paper.numauth-5
                    aexstring = ", + " + str(authremain) + " more"
                    paper.author = paper.author + aexstring
                body.append('<div class="authors small">%s</div>' % paper.author)
                # Limit the length of the abstract displayed, and if its
                #   shorter then just display the whole thing
                abslength = 500
                # Hopefully remove links and other HTML things in there
                if len(paper.abstract) > abslength:
                    paper.shortabs = paper.abstract[0:abslength] + '...'
                    paper.shortabs = paper.shortabs.rstrip()
                else:
                    paper.shortabs = paper.abstract
                paper.shortabs = paper.shortabs.lstrip()
                paper.shortabs = paper.shortabs.rstrip()
                body.append('<div id="abstract"><p>%s</p></div>' % paper.shortabs)
                body.append(action_text)
                body.append('</article>')
            else:
                body.append('<article class="block">')
                if (paper.url.find('.pdf') > -1):
                    paper.date = "Please Do NOT Submit Direct PDF Links:"
                else:
                    paper.date = "Unknown Submission/Link:"
                body.append('<div class="date small">%s</div>' % paper.date)
                title = '<h3><a href="%s">%s</a></h3>' % (paper.url, paper.url)
                body.append('%s' % title)
                body.append(discussed_link)
                body.append('</article>')
    
    # Finish up and return if no papers in discussed list
    if len(papers_discussed) == 0:
        body.append('<article class="block"><hr>')
        body.append('<center><p>No papers discussed yet</p></center>')
        body.append('<img src="./images/SadPaper_2x.png" srcset="./images/SadPaper_1x.png 1x, ../images/SadPaper_2x.png 2x" alt="Sad Paper :("/></article>')
        
        body = [line+'\n' for line in body]

        # Concatenate everything together
        html = h + body + f

        return html
    
    body.append('<hr>')
    body.append('<center><p><strong>Papers already discussed</strong></p></center>')
    
    paper_indices = range(len(papers_discussed))
    
    for paper_index in reversed(paper_indices):
        paper = papers_discussed[paper_index]
        
        # ## Constructing discussed link
        # paper_id = papers_discussed[paper_index]
        # discussed_link = ' <a href="http://coffee.astro.ucla.edu/discussed/discussed.php?ID={0}">Discussed?</a>'.format(paper_id)
        # paper.sources.append(discussed_link)
        
        date = paper.date
        if isinstance(paper, preprint):
            if paper.errors.startswith("Success"):
                if paper.sources != '':
                    if date != "":
                        body.append('<article class="block">')
                        body.append('<div class="date small">%s</div>' % paper.date)
                    # Remove any stray/extra whitespaces
                    paper.sources = paper.sources.lstrip()
                    paper.sources = paper.sources.rstrip()
                    body.append('<div class="links small">[ %s ]</div>' %
                                paper.sources)
                    title = '<h3><a href="%s">%s</a></h3>' \
                            % (paper.url, paper.title)
                else:
                    if date != "":
                        body.append('<article class="block">')
                        body.append('<div class="date small">%s</div>' % paper.date)
                    title = '<h3><a href="%s">%s</a></h3>' % (paper.url, paper.title)
                body.append('%s' % title)
                if paper.numauth > 5 and \
                   paper.author != "Error Grabbing Authors":
                    authremain = paper.numauth-5
                    aexstring = ", + " + str(authremain) + " more"
                    paper.author = paper.author + aexstring
                body.append('<div class="authors small">%s</div>' % paper.author)
                # Limit the length of the abstract displayed, and if its
                #   shorter then just display the whole thing
                abslength = 500
                # Hopefully remove links and other HTML things in there
                if len(paper.abstract) > abslength:
                    paper.shortabs = paper.abstract[0:abslength] + '...'
                    paper.shortabs = paper.shortabs.rstrip()
                else:
                    paper.shortabs = paper.abstract
                paper.shortabs = paper.shortabs.lstrip()
                paper.shortabs = paper.shortabs.rstrip()
                body.append('<div id="abstract"><p>%s</p></div>' % paper.shortabs)
                body.append('</article>')
            else:
                body.append('<article class="block">')
                if (paper.url.find('.pdf') > -1):
                    paper.date = "Please Do NOT Submit Direct PDF Links:"
                else:
                    paper.date = "Unknown Submission/Link:"
                body.append('<div class="date small">%s</div>' % paper.date)
                title = '<h3><a href="%s">%s</a></h3>' % (paper.url, paper.url)
                body.append('%s' % title)
                body.append('</article>')
    
    
    new_body = []

    for line in body:
        try:
            new_body.append(line + '\n')
        except:
            new_body.append(line.encode('utf-8') + '\n')

    body = new_body
    
    # Concatenate everything together
    html = h + body + f

    return html


def doarchivepage(papers_ids, papers_discussed_ids, papers_next_ids, papers_volunteers, file, discussed_file, next_file, volunteers_file, outfile):
    """Create the archive file, clear the papers file

    INPUTS:
       file: (str) path to the papers file
       outfile: (str) path to archive file to create
    """

    import glob
    import shutil
    import re

    arcstat = ''

    try:
        f = open(outfile)
        arcstat = "Old papers already archived\n\n"
        f.close()
    except:
        arcstat = "Past previous deadline, so archiving old papers\n\n"

        # Easy file concatenation:
        f = open(outfile, 'wb')
        shutil.copyfileobj(open('./archive_top.php', 'rb'), f)
        shutil.copyfileobj(open('./astro_coffee.php', 'rb'), f)
        shutil.copyfileobj(open('./archive_bottom.php', 'rb'), f)
        f.close()

        # Get a list of all the current archived papers
        archived = glob.glob('./archive/*papers.php')
        # Now make the index page for archive, the long way since we add html
        page = open('./archive_top.php', 'r').read()
        page = page + '                <ul style="columns: 2; list-style-type: none;">\n'
        arclinks = ''
        for files in reversed(sorted(archived)):
            files = re.sub(r'\./archive\/', '', files)
            linkname = re.sub(r'[\.\-]papers\.php', '', files)
            arclinks = arclinks + '                    <li><a href="' + files + '">' + \
                       linkname + '</a></li>\n'
        page = page + arclinks
        page = page + '</ul>\n'
        page = page + open('./archive_bottom.php', 'r').read()
        # Append it to our output file
        outfile = './archive/index.php'
        f = open(outfile, 'w')
        f.write(page)
        f.close()

        try:
            # Move next week's papers to current week
            new_papers_ids = []
            
            f = open(file, 'w')
            for cur_id in papers_next_ids:
                if cur_id not in papers_discussed_ids:
                    f.write(cur_id + '\n')
                    new_papers_ids.append(cur_id)
            f.close()
            
            # Clear next week's papers list
            next_f = open(next_file, 'w')
            next_f.write('\n')
            next_f.close()
            
            # Clear discussed papers list
            disc_f = open(discussed_file, 'w')
            disc_f.write('\n')
            disc_f.close()
            
            # Clear volunteers list
            volun_f = open(volunteers_file, 'w')
            volun_f.write('--')
            volun_f.close()
            
            papers_ids = new_papers_ids
            papers_discussed_ids = []
            papers_next_ids = []
            papers_volunteers = {}
        except:
            html = ['Could not get the papers info in the archive loop']
            papers = []
            arcstat = arcstat + "Could not get paper info in archive loop\n\n"
    return arcstat, papers_ids, papers_discussed_ids, papers_next_ids, papers_volunteers


def docoffeepage(file, discussed_file, next_file, volunteers_file, url, day, hour, min, sleep=60, idid=False, php=False):
    """Read in arxiv IDs from a specified ASCII file, and write HTML.

    INPUTS:
       file: (str) path of ASCII file with arxiv IDs
       discussed_file:  (str) path of ASCII file with IDs of discussed papers
       url:  (str) path of HTML file to write
       day:  (dateutil) day of meeting time
       hour: (flt) hour of meeting time
       min:  (flt) minute of meeting time

    OPTIONAL INPUT:
        sleep -- (float) number of seconds to wait between URL
                 requests, so aRxIv doesn't think you're a robot and
                 ban your connection.
    """
    
    import datetime
    
    today = datetime.datetime.now()
    msg1, prevdate = getprevduedate(day, hour, min)
    msg2, nextdate = getnextduedate(day, hour, min)
    
    outstat = msg1 + "\n" + msg2
    outstat = outstat + "\nPrevious: " + prevdate.strftime('%Y-%m-%d')
    outstat = outstat + "\nNow:      " + today.strftime('%Y-%m-%d %H:%M:%S')
    outstat = outstat + "\nNext:     " + nextdate.strftime('%Y-%m-%d') + "\n\n"
    
    # Read in paper IDs and discussed paper IDs as lists
    papers_ids, paper_id_errors = read_file(file)
    papers_discussed_ids, paper_discussed_id_errors = read_file(discussed_file)
    papers_next_ids, paper_next_id_errors = read_file(next_file)
    papers_volunteers = read_volunteers_file(volunteers_file)
    
    # Check papers against discussed papers list
    papers_ids, papers_discussed_ids, papers_next_ids = paper_lists_checker(papers_ids, papers_discussed_ids, papers_next_ids)
    
    # Make archive page if necessary
    outfile='./archive/' + prevdate.strftime('%Y-%m-%d') + '-papers.php'
    arcstat, papers_ids, papers_discussed_ids, papers_next_ids, papers_volunteers = doarchivepage(papers_ids, papers_discussed_ids, papers_next_ids, papers_volunteers, file, discussed_file, next_file, volunteers_file, outfile)
    paperrs = ''
    
    # Read in the papers
    try:
        paperrs, papers = readlist(papers_ids, sleep=sleep)
        paperrs_discussed, papers_discussed = readlist(papers_discussed_ids, sleep=sleep)
        paperrs_next, papers_next = readlist(papers_next_ids, sleep=sleep)
        html = []
    except Exception, why:
        html = ['Could not get the papers info']
        papers = []
        papers_discussed = []
        papers_next = []
        outstat = outstat + 'Could not get the paper info\n\n'
        outstat += str(why) + "\n\n"
    
    # Make html for the page
    html = makehtml(papers, papers_ids, papers_discussed, papers_discussed_ids, papers_next, papers_next_ids, papers_volunteers, day, hour, min, idcomments=idid, php=php)
    # try:
    #     html = makehtml(papers, papers_ids, papers_discussed, papers_discussed_ids, day, hour, min, idcomments=idid, php=php)
    # except:
    #     html.append('Could not generate HTML')
    #     outstat = outstat + 'Could not generate HTML code\n\n'

    # Write the file
    
    # with open(url, 'w') as f:
    #     f.writelines(html)
    
    try:
        f = open(url, 'w')
        f.writelines(html)
        f.close()
    except:
        outstat = outstat + 'Could not write HTML code to file ' + url + "\n\n"

    outstat = str(outstat) + str(arcstat) + str(paperrs)
    return (html, outstat)
