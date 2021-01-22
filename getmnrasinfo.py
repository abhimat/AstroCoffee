#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getmnrasinfo(url, html):
    """Convert HTML from a MNRAS journal page to a preprint object."""

    from bs4 import BeautifulSoup
    import re
    import datetime
    from astroph import preprint

    paper = preprint()
    paper.url = url
    # Remove all the muck that screws up the BeautifulSoup parser
    # Will fail on PDF submission, so take care of that exception first
    try:
        fhtml =re.sub(re.compile("<!--.*?-->",re.DOTALL),"",html)
        soup = BeautifulSoup(fhtml)
        paper.errors = "0"
    except:
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
    
    # Grab the paper info
    
    ## Grab title
    try:
        paper.title = str(soup.find('h1',  {'id':'article-title-1'}).text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    # print(paper.title)
    
    ## Grab date
    try:
        date_str = str(soup.find('span', {'class':'slug-ahead-of-print-date'}).text.encode("utf-8"))
    
        date = datetime.datetime.strptime(date_str, '%B %d, %Y')
    
        paper.date = date.strftime('%d %b %Y')
    except:
        paper.errors = "0"
        paper.date = "Error Grabbing Date"
    
    # print(date_str)
    # print(paper.date)
    
    ## Grab authors
    try:
        authors = soup.findAll('a', {'class':'name-search'})
        paper.numauth = len(authors)
    
        ### Convert authors to strings and replace relative links
        author_list = []
        for i in authors:
            cur_auth_link = str(i)
            cur_auth_link = cur_auth_link.replace('/search?', 'http://mnras.oxfordjournals.org/search?')
            cur_auth_link = cur_auth_link.replace(' class="name-search"', '')
            author_list.append(cur_auth_link)
    
        paper.author = ', '.join(author_list[0:4])
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"
    
    # print(paper.author)
    
    
    ## Grab abstract
    try:
        paper.abstract = str(soup.find('p',{'id':'p-1'}))
        paper.abstract = paper.abstract.lstrip('<p id="p-1">')
        paper.abstract = paper.abstract.rstrip('</p>')
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"
    
    # print(paper.abstract)
    
    ## Grab sources
    try:
        sources_list = []

        PDF_link = str(soup.find('a',{'rel':'view-full-text.pdf'}))
        if PDF_link != 'None':
            PDF_link = PDF_link.replace('/content/', 'http://mnras.oxfordjournals.org/content/')
            PDF_link = PDF_link.replace('.pdf+html', '.pdf')
            PDF_link = PDF_link.replace(' rel="view-full-text.pdf"', '')
            PDF_link = PDF_link.replace('Full Text (PDF)', 'PDF')
            sources_list.append(PDF_link)

        HTML_link = str(soup.find('a',{'rel':'view-full-text'}))
        if HTML_link != 'None':
            HTML_link = HTML_link.replace('/content/', 'http://mnras.oxfordjournals.org/content/')
            HTML_link = HTML_link.replace(' rel="view-full-text"', '')
            HTML_link = HTML_link.replace('Full Text (HTML)', 'HTML')
            sources_list.append(HTML_link)

        paper.sources = ' '.join(sources_list)
    except:
        paper.errors = "0"
        paper.sources = " "
    
    # print(paper.sources)
    
    ## Grab subject
    try:
        paper.subject = str(soup.find('a',  {'class':'kwd-search'}).text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.subject   = "Error Grabbing Subject"
    
    return paper
