#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

# Get ATel article information
# ---
# Abhimat Gautam

def get_atel_info(url, html):
    """Convert HTML from an ApJ journal page to a preprint object."""

    from bs4 import BeautifulSoup
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
        paper.title = str(soup.find('h1', {'class':'title'}).text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    # print(paper.title)
    
    ## Grab authors and date block
    try:
        credits_block = (soup.find('div', {'id':'telegram'}).findAll('p', {'align':'CENTER'}))[1]
    except:
        paper.errors = "0"
        paper.date = 'Error Grabbing Date'
        paper.author = 'Error Grabbing Authors'
    
    # print(credits_block)
    
    ## Grab date
    try:
        date_str = str(((credits_block.findAll('strong'))[1]).text.encode("utf-8"))

        date_suffix = ';'
        date_index = date_str.rindex(date_suffix)

        date_str = date_str[:date_index]
        
        date = datetime.datetime.strptime(date_str, '%d %b %Y')
        
        paper.date = date.strftime('%d %b %Y')
    except:
        paper.errors = "0"
        paper.date = "Error Grabbing Date"

    # print(date_str)
    # print(paper.date)

    ## Grab authors
    try:
        author_str = str(((credits_block.findAll('strong'))[0]).text.encode("utf-8"))
        
        # Strip out affiliations
        author_str = re.sub(r" ?\([^)]+\)", "", author_str)
        
        # Split author string on commas
        authors = author_str.split(',')
        paper.numauth = len(authors)
        
        # Convert the authors to stripped strings
        alist=[]
        for author in authors:
            alist.append(author.strip())
        paper.author = ', '.join(alist[0:4])
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"

    # print(paper.author)
    # print(paper.numauth)
    
    ## Grab abstract
    try:
        abstract_pars = (soup.find('div', {'id':'telegram'}).findAll('p'))[2:]
        abstract_str = ''
        
        for cur_par in abstract_pars:
            cur_par_str = cur_par.text.encode("utf-8").strip()
            
            if (cur_par == '' or
                (cur_par_str.startswith('Subjects:') or
                 cur_par_str.startswith('Tweet') or
                 cur_par_str.startswith('Referred to by'))):
                continue
            
            abstract_str = abstract_str + cur_par_str + '\n' 
        
        paper.abstract = abstract_str
    except:
        paper.errors = "0"
        paper.abstract = "Error Grabbing Abstract"

    # print(paper.abstract)
    
    ## Grab sources
    try:
        sources_list = []

        # PDF_href = soup.find('div',{'class':'btn-multi-block mb-1'}).a.get('href')
        # if PDF_href != None:
        #     PDF_link = '<a href="{0}">PDF</a>'.format(PDF_href)
        #     sources_list.append(PDF_link)

        HTML_link = '<a href="{0}">ATel</a>'.format(url)
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
