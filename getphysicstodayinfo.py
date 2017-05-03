#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getphysicstodayinfo(url, html):
    """Convert HTML from a Physics Today page to a preprint object."""

    from BeautifulSoup import BeautifulSoup
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
        paper.title = str(soup.find('header',  {'class':'publicationContentTitle'}).text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    print(paper.title + '\n')
    
    ## Grab date
    try:
        date_str = str(soup.find('span', {'class':'date'}).text.encode("utf-8"))
        
        date = datetime.datetime.strptime(date_str, '%B %Y')

        paper.date = date.strftime('%b %Y')
    except:
        paper.errors = "0"
        paper.date = "Error Grabbing Date"

    # print(date_str)
    # print(paper.date)

    ## Grab authors
    try:
        authors = soup.find('div', {'class':'entryAuthor'})
        authors = authors.findAll('a')
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
        head_soup = soup.find('div',{'class':'hlFld-Fulltext'})
        abstract_ps = head_soup.findAll('div',{'class':'NLM_paragraph'})

        abstract = ''
        abstract += abstract_ps[0].text.encode("utf-8") + '\n'

        paper.abstract = abstract
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"

    # print(paper.abstract)
   
    ## Grab sources
    try:
        base_url = 'http://physicstoday.scitation.org'

        sources_list = []
        
        sources = soup.find('div',{'class':'pull-right toolbar'}).findAll('a')    
        
        for source in sources:
            source_url = source['href']
            if 'pdf' in source_url:
                sources_list.append('<a href={0}{1}>PDF</a>'.format(base_url, source_url))
            elif 'full' in source_url:
                sources_list.append('<a href={0}{1}>Full HTML</a>'.format(base_url, source_url))
        paper.sources = ' '.join(sources_list)
    except:
        paper.errors = "0"
        paper.sources = " "

    # print(paper.sources)

    # ## Grab subject
    # try:
    #     keywords = str(soup.find('div',  {'class':'kword'}).text.encode("utf-8"))
    #     keywords = keywords.replace('Key words:', '')
    #
    #     paper.subject = keywords
    #
    # except:
    #     paper.errors = "1"
    #     paper.subject   = "Error Grabbing Subject"

    return paper
