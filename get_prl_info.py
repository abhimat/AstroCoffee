#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_prl_info(url, html):
    """Convert HTML from a MNRAS journal page to a preprint object."""

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
        paper.title = str(soup.find('h3').text.encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"
    
    # print(paper.title)
    
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

    # print(date_str)
    # print(paper.date)

    ## Grab authors
    try:
        authors_str = str(soup.find('h5', {'class':'authors'}).text.encode("utf-8"))
        
        ### Find authors in the authors_str
        author_list = []
        
        etAl_index = authors_str.find('et al.')
        if etAl_index > -1:
            author_list.append(authors_str[0:etAl_index])
            author_list.append('et al.')
        else:
            split_authors = authors_str.split(', ')
            for author in split_authors:
                par_index = author.find('(')
                if par_index > -1:
                    author = author[0:par_index]
                author = author.replace('and ', '')
                author = author.strip()
                author_list.append(author)
        
        paper.numauth = len(author_list)
        paper.author = ', '.join(author_list[0:4])
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"

    # print(paper.author)

    ## Grab abstract
    try:
        abstract_str = str(soup.find('section',{'class':'article open abstract'}).find('div',{'class':'content'}).find('p'))
        
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

        PDF_link = str(soup.find('div',{'class':'article-nav-actions'}).a)
        # print(PDF_link)
        if PDF_link != 'None':
            PDF_link = PDF_link.replace(' class="small button"', '')
            PDF_link = PDF_link.replace('/prl/', 'http://journals.aps.org/prl/')
            PDF_link = PDF_link.replace('.pdf+html', '.pdf')
            sources_list.append(PDF_link)
       
        HTML_link = str(soup.find('div',{'class':'article-nav-actions'}).find('a',{'id':'fulltext-button'}))
        if HTML_link != 'None':
            HTML_link = HTML_link.replace(' class="small button show-for-medium-up"', '')
            HTML_link = HTML_link.replace(' id="fulltext-button"', '')
            HTML_link = HTML_link.replace('/prl/', 'http://journals.aps.org/prl/')
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
    
    return paper
