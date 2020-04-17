#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

# Get ApJ article information
# ---
# Abhimat Gautam

def get_apj_info(url, html):
    """Convert HTML from an ApJ journal page to a preprint object."""

    from BeautifulSoup import BeautifulSoup
    import re
    import datetime
    from astroph import preprint
    
    paper = preprint()
    paper.url = url
    
    try:
        # # Use Selenium to download html, because ApJ found out we're a bot (oh no)
        # from selenium import webdriver
        # import pdb
        #
        # driver = webdriver.Safari()
        # driver.get(url)
        # html = driver.page_source
        # # pdb.set_trace()
        # driver.close()
        
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
        paper.title = str(soup.find('h1').text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    # print(paper.title)
    
    ## Grab date
    try:
        date_str = str(soup.find('span', {'class':'wd-jnl-art-pub-date'}).text.encode("utf-8"))
        
        date_prefix = 'Published '
        date_index = date_str.rindex(date_prefix) + len(date_prefix)
        
        date_str = date_str[date_index:]
        
        date = datetime.datetime.strptime(date_str, '%Y %B %d')

        paper.date = date.strftime('%d %b %Y')
    except:
        paper.errors = "0"
        paper.date = "Error Grabbing Date"

    # print(date_str)
    # print(paper.date)

    ## Grab authors
    try:
        authors = soup.find('p', {'class':'mb-0'}).findAll('span', {'itemprop':'name'})
        paper.numauth = len(authors)
        
        
        # Convert the authors to strings only
        alist=[]
        for i in authors:
            alist.append(i.text.encode("utf-8"))
        paper.author = ', '.join(alist[0:4])
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"

    # print(paper.author)
    # print(paper.numauth)

    ## Grab abstract
    try:
        abstract_str = str(soup.find('div',{'class':'article-text wd-jnl-art-abstract cf'}).find('p'))
        
        paper.abstract = abstract_str
        paper.abstract = paper.abstract.replace('<p>', '')
        paper.abstract = paper.abstract.replace('</p>', '')
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"

    # print(paper.abstract)

    ## Grab sources
    try:
        sources_list = []
        
        PDF_href = soup.find('div',{'class':'btn-multi-block mb-1'}).a.get('href')
        if PDF_href != None:
            PDF_link = '<a href="{0}">PDF</a>'.format(PDF_href)
            sources_list.append(PDF_link)
       
        HTML_link = '<a href="{0}">HTML</a>'.format(url)
        if HTML_link != 'None':
            sources_list.append(HTML_link)

        paper.sources = ' '.join(sources_list)
    except:
        paper.errors = "0"
        paper.sources = " "

    # print(paper.sources)

    # ## Grab subject
    # try:
    #     paper.subject = str(soup.find('a',  {'class':'kwd-search'}).text.encode("utf-8"))
    # except:
    #     paper.errors = "1"
    #     paper.subject   = "Error Grabbing Subject"
    
    print('')
    print(paper.title)
    print('')
    
    return paper
