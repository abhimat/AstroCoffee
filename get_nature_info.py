#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

def get_nature_info(url, html):
    """Convert HTML from a Nature journal page to a preprint object."""

    from BeautifulSoup import BeautifulSoup
    import re
    import datetime
    from astroph import preprint

    paper = preprint()
    paper.url = url
    
    # Remove all the muck that screws up the BeautifulSoup parser
    # Will fail on PDF submission, so take care of that exception first
    try:
        fhtml =re.sub(re.compile("<!--.*?-->", re.DOTALL), "", html)
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
        paper.title = str(soup.find('h1', {'itemprop':'name headline'}).text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    print paper.title + "\n"
    
    ## Grab date
    try:
        date_str = str(soup.find('h5', {'class':'pub-info'}).text.encode("utf-8"))
        
        date_prefix = 'Published '
        date_index = date_str.rindex(date_prefix) + len(date_prefix)
        
        date_str = date_str[date_index:]
        
        date = datetime.datetime.strptime(date_str, '%d %B %Y')

        paper.date = date.strftime('%d %b %Y')
    except:
        paper.errors = "0"
        paper.date = "Error Grabbing Date"
    
    
    ## Grab the date
    try:
        paper.date = soup.find(attrs={"name":
                                      re.compile("dc.date", re.I)})['content']
        # Try to convert the old style first
        # Put the date in the same format as arXiv for consistency
        try:
            dpart = paper.date.split('-')
            newdate = datetime.date(int(dpart[0]), int(dpart[1]),
                                    int(dpart[2]))
            paper.date = newdate.strftime("%d %b %Y")
        except:
            pass
        if paper.date == "":  # If the old style isn't found, try the new style
            cdate = soup.find("dl",
                              attrs={"class": re.compile("citation", re.I)})
            cdate = str(cdate.findAll("dd")[3].next)  # Fragile...
            paper.date = cdate.replace('(', '').replace(')', '')
    except:
        paper.errors = "1"
        paper.date = "Error Grabbing Date"
    
    
    ## Grab the authors
    try:
        authors = soup.findAll(attrs={"name": re.compile("dc.creator", re.I)})
        paper.numauth = len(authors)
        # Convert the authors to strings only, then print only up to 8 of them
        alist = []
        for i in authors:
            # Also .encode method to replace accent characters with html equiv.
            alist[paper.numauth:] = \
                    [unicode(i['content']).encode('ascii', 'xmlcharrefreplace')]
        paper.author = ', '.join(alist[0:4])
    except:
        paper.errors = "1"
        paper.numauth = 1
        paper.author = "Error Grabbing Authors"
    
    
    ## Grab abstract
    try:
        abstract_str = str(soup.find('div',{'id':'abstract-content'}).find('p').text.encode("utf-8"))
        
        paper.abstract = abstract_str
        # paper.abstract = paper.abstract.replace('<p>', '')
        # paper.abstract = paper.abstract.replace('</p>', '')
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"
        
    ## Paper and abstract cleanup
    paper.title = paper.title.replace('|[thinsp]|', ' ')
    paper.abstract = paper.abstract.replace('|[thinsp]|', ' ')
    paper.abstract = paper.abstract.replace('[plusmn]', '+/-')
    
    ## Grab sources
    htmllink = ''
    pdflink = ''

    try:
        htmllink = ''.join(soup.find('a', {'class': 'fulltext'}))
    except:
        try:
            htmllink = soup.find('li', {'class': 'full-text'}).next
            htmllink = str(htmllink)
            htmllink = htmllink.replace('/nature/',
                                        'https://www.nature.com/nature/')
        except:
            htmllink = '<a href=\"' + paper.url + '\">HTML</a>'

    try:
        pdflink = ''.join(soup.find('a', {'class': 'download-pdf'}))
    except:
        try:
            pdflink = soup.find('li', {'class': 'download-pdf'}).next
            pdflink = str(pdflink)
            pdflink = pdflink.replace('/nature/',
                                      'https://www.nature.com/nature/')
            pdflink = pdflink.replace('Download PDF', 'PDF')
        except:
            try:
                pdflink = soup.find('li', {'class': 'pdf'}).next
                pdflink = str(pdflink)
                pdflink = pdflink.replace('/news/',
                                          'https://www.nature.com/news/')
                pdflink = pdflink.replace('PDF Format', 'PDF')
            except:
                pdflink = '<a href=\"' + paper.url + '.pdf' + '\">PDF</a>'

    if pdflink == 'None':
        pdflink = ''

    htmllink = htmllink.replace('Full text', 'HTML')
    paper.sources = htmllink + ' ' + pdflink
    
    return paper
