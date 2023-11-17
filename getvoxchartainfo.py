#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getvoxchartainfo(url, html):
    """Convert HTML from a Vox Charta page to a preprint object, via the getarxivinfo function"""
    
    from bs4 import BeautifulSoup
    import re
    import datetime
    from astroph import preprint, getunique
    
    import urllib2
    from getarxivinfo import getarxivinfo
    
    # Remove all the muck that screws up the BeautifulSoup parser
    # Will fail on PDF submission, so take care of that exception first
    try:
        fhtml =re.sub(re.compile("<!--.*?-->",re.DOTALL),"",html)
        soup = BeautifulSoup(fhtml)
    except:
        paper = preprint()
        paper.url = url
        paper.errors = "1"
        paper.title = "Error Grabbing Title"
        paper.author = "Error Grabbing Authors"
        paper.numauth = "1"
        paper.date = "Error Grabbing Date"
        paper.abstract = "Error Grabbing Abstract"
        paper.sources = " "
        paper.subject = "Error Grabbing Subject"
        paper.comments = "Error Grabbing Comments"
        return paper
    
    # Read through file to try to find arXiv link
    ptags = soup.findAll('p')
    
    # print ptags
    
    ## Look through p tags until we get to arXiv info
    info_index = 0
    while not((ptags[info_index].text.encode("utf-8")).startswith('ArXiv #:')):
        info_index += 1
    
    arxiv_info_string = str(ptags[info_index].text.encode("utf-8"))
    arxiv_id = arxiv_info_string[8:arxiv_info_string.find('(')]
    
    url = "http://arxiv.org/abs/" + arxiv_id
    id = url
    html = ''
    # HTTP request for the arXiv URL
    try:
        ## Add headers to HTTP request so don't get 403 error
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        request = urllib2.Request(id, headers=hdr)
    
        html = urllib2.urlopen(request).read()
        urlpage = id  # For compatibility down lower in the code
    except urllib2.HTTPError(e):
        print(e.code)
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
    
    paper = getarxivinfo(url, html)
    return paper
    
    # print(ptags[info_index].a.text)