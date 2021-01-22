#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getaandainfo(url, html):
    """Convert HTML from an A&A journal page to a preprint object."""

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
        paper.title = str(soup.find('h2',  {'class':'title'}).text.encode("utf-8"))
        paper.title = paper.title.rstrip(u'&#8902;')
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    print(paper.title + '\n')
    
    ## Grab date
    try:
        date_str = str(soup.find('p', {'class':'history'}).text.encode("utf-8"))
        
        pre_date_str = 'Accepted:'
        index_pre_date_str = date_str.index(pre_date_str)
        date_str = date_str[index_pre_date_str + len(pre_date_str):]
        
        date = datetime.datetime.strptime(date_str, '%d %B %Y')
        
        paper.date = date.strftime('%d %b %Y')
    except:
        paper.errors = "0"
        paper.date = "Error Grabbing Date"

    # print(date_str)
    # print(paper.date)

    ## Grab authors
    try:
        authors = soup.findAll('span', {'class':'author'})
        paper.numauth = len(authors)

        ### Convert authors to strings
        author_list = []
        for author in authors:
            author_list.append(author.text.encode("utf-8"))

        paper.author = ', '.join(author_list[0:4])
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"

    # print(paper.author)


    ## Grab abstract
    try:
        head_soup = soup.find('div',{'id':'contenu'}).find('div',{'id':'head'})
        abstract_ps = head_soup.findAll('p', {'class':None})
        
        abstract = ''
        for abstract_p in abstract_ps:
            abstract += abstract_p.text.encode("utf-8") + '\n'
        
        paper.abstract = abstract
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"

    # print(paper.abstract)

    ## Grab sources
    try:
        base_url = 'http://www.aanda.org'
        
        sources_list = []

        PDF_link_soup = soup.find('a',{'title':re.compile('PDF*')})
        PDF_link = str(PDF_link_soup)
        if PDF_link != 'None':
            PDF_text = PDF_link_soup['title']
            PDF_link = PDF_link.replace('href="', 'href="' + base_url)
            PDF_link = PDF_link.replace(PDF_text, 'PDF')
            PDF_link = PDF_link.replace(' title="PDF"', '')
            sources_list.append(PDF_link)
        
        HTML_link = str(soup.find('a',{'title':'Full HTML'}))
        if HTML_link != 'None':
            HTML_link = HTML_link.replace('href="', 'href="' + base_url)
            HTML_link = HTML_link.replace(' class="current_doc"', '')
            HTML_link = HTML_link.replace('Full HTML', 'HTML')
            HTML_link = HTML_link.replace(' title="HTML"', '')
            sources_list.append(HTML_link)

        paper.sources = ' '.join(sources_list)
    except:
        paper.errors = "0"
        paper.sources = " "

    # print(paper.sources)

    ## Grab subject
    try:
        keywords = str(soup.find('div',  {'class':'kword'}).text.encode("utf-8"))
        keywords = keywords.replace('Key words:', '')
        
        paper.subject = keywords
        
    except:
        paper.errors = "1"
        paper.subject   = "Error Grabbing Subject"
    
    return paper
