#!/usr/bin/env python
# encoding: utf-8

def getarxivinfo(url, html):
    """Convert HTML from a arXiv page to a preprint object."""
    # 2010-03-26       RTH: Phoenix version, rewritten using BeautifulSoup
    # 2010-04-06       RTH: Fixed bug in date grab, now grabs date of latest
    #                         submitted paper/revision
    # 2014~2015        FBD: Correctly parses the pages after mathjax update
    # 2015-03-17       FBD: Now uses the UCLA arXiv mirror

    from BeautifulSoup import BeautifulSoup
    # from bs4 import BeautifulSoup
    import re
    import datetime
    from astroph import preprint, getunique

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

    # Grab the Title, Date, and Authors, and all the other stuff
    try:
        paper.title = soup.find('h1',  {'class':'title mathjax'}).contents[1].string
    except:
        paper.errors = "1"
        paper.title = "Error Grabbing Title"

    print paper.title + "\n"

    try:
        authors = soup.find('div', {'class':'authors'})
        authors = authors.findAll('a')
        paper.numauth = len(authors)
        # Convert the authors to strings only and replace the relative links
        alist=[]
        for i in authors:
            alist.append(str(i).replace('/find/','http://arxiv.org/find/'))
        paper.author = ', '.join(alist[0:4])
        # Kill all affiliation marks since some have them and some don't;
        #   done in two steps to take care of nested parens
        paper.author = re.sub(r'\([^()]*\)','',paper.author)
        paper.author = re.sub(r'\([^()]*\)','',paper.author)
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"

    # print paper.errors + paper.author + "\n"


    try:
        date = soup.find('div', {'class':'submission-history'})
        date = date.findAll(text=True) # Remove HTML tags
        date = getunique(date) # Cheap way of ignoring multiple \n's
        date = date[-1].split() # Most recent revision date will be the last
        paper.date = date[1] + ' ' + date[2] + ' ' + date[3]
    except:
        paper.errors = "1"
        paper.date = "Error Grabbing Date"

    # print paper.errors + paper.date + "\n"


    try:
        paper.abstract = soup.find('blockquote',{'class':'abstract mathjax'}).contents[1].encode('utf-8')
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"

    # print paper.errors + paper.abstract + "\n"

    try:
        sources = soup.find('div', {'class':'full-text'})
        sources  = sources.findAll('a')
        slist=[]
        for i in sources:
            curstring = str(i)
            curstring = curstring.replace('/ps','http://arxiv.org/ps')
            curstring = curstring.replace('/pdf','http://arxiv.org/pdf')
            curstring = curstring.replace('/format','http://arxiv.org/format')
            curstring = curstring.replace('PostScript','PS')
            curstring = curstring.replace('Other formats','Other')
            if 'license' in curstring:
                continue
            slist.append(curstring)
        paper.sources = ' '.join(slist)
    except:
        paper.errors = "1"
        paper.sources = ''

    # print paper.errors + paper.sources + "\n"

    try:
        paper.subject = soup.find('span', {'class':'primary-subject'}).string
    except:
        paper.errors = "1"
        paper.subject = "Error Grabbing Subject"

    # print paper.errors + paper.subject + "\n"

    #try:
    #paper.comments = soup.find('td', {'class':'tablecell comments'}).string
    #except:
        #paper.errors = "1"
        #paper.comments = "Error Grabbing Comments"

    # print paper.errors + paper.comments + "\n"
    paperid = soup.find(attrs={"name":re.compile("citation_arxiv_id",re.I)})['content']
    paper.url = 'http://arxiv.org/abs/' + paperid

    return paper
