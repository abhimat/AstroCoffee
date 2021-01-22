#!/usr/bin/env python
# encoding: utf-8

def getscienceinfo(url, html):
    """Convert HTML from a Science journal page to a preprint object."""
    # 2015-3-6 First attempt at making this work. (FBD)

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

    # Grab the title
    try:
        paper.title = str(soup.find(attrs={"name":re.compile("DC.Title",re.I)})['content'].encode("utf-8"))
    except:
        paper.errors = "1"
        paper.title   = "Error Grabbing Title"

    print paper.title

    # Grab the date
    try:
        paper.date = soup.find(\
                     attrs={"name":re.compile("DC.Date",re.I)})['content']
        # Try to convert the old style first
        # Put the date in the same format as arXiv for consistency
        try:
            dpart = paper.date.split('-')
            newdate = datetime.date(int(dpart[0]), int(dpart[1]), int(dpart[2]))
            paper.date = newdate.strftime("%d %b %Y")
        except:
            pass 
        if paper.date == "": # If the old style isn't found, try the new style
            cdate = soup.find("dl", attrs={"class":re.compile("citation",re.I)})
            cdate = str(cdate.findAll("dd")[3].next) # Fragile...
            paper.date = cdate.replace('(','').replace(')','')
    except:
        paper.errors = "1"
        paper.date = "Error Grabbing Date"
#    print paper.date

    # Grab the authors
    try:
        authors = soup.findAll(attrs={"name":re.compile("DC.Contributor",re.I)})
        paper.numauth = len(authors)
        # Convert the authors to strings only, then print only up to 8 of them
        alist=[]
        for i in authors:
            # Also .encode method to replace accent characters with html equiv.
            alist[paper.numauth:] = \
                    [unicode(i['content']).encode('ascii','xmlcharrefreplace')] 
        paper.author = ', '.join(alist[0:4])
    except:
        paper.errors = "1"
        paper.numauth = 1
        paper.author = "Error Grabbing Authors"

    # Get the abstract as one big long string, sans any html or script crap
    #   this does keep the footnote numbers unfortunately, but big whoop
    paper.abstract = ''
    try:
        abstract_div = soup.find("div", attrs={"class":"section abstract"})
        paper.abstract = ''.join(abstract_div.find("p").findAll(text=True))
    except:
        try:
            paper.abstract = ''.join(soup.find("p", attrs={"id":"p-4"}).findAll(text=True))
        except:
            try:
                paper.abstract = ''.join(soup.find("p", attrs={"class":"intro"}).findAll(text=True))
            except:
                paper.abstract = ''.join(soup.find("meta", attrs={"name":"description"})['content'])

    if paper.abstract == 'None' or paper.abstract == '':
        paper.abstract = "Error Grabbing Abstract"
    else:
        # Convert Unicode chars to displayable characters
        paper.abstract = paper.abstract.encode('ascii','xmlcharrefreplace')

    # Could be more of these necessary in the future to purge their CSS things
    paper.title = paper.title.replace('|[thinsp]|',' ')
    paper.abstract = paper.abstract.replace('|[thinsp]|',' ')
    paper.abstract = paper.abstract.replace('[plusmn]','+/-')

    if url.endswith('.full'):
        paper.sources = '<a href=' + url + '>HTML </a>' + '<a href=' + url + '.pdf>PDF</a>'
    else:
        paper.sources = '<a href=' + url + '.full>HTML </a>' + '<a href=' + url + '.full.pdf>PDF</a>'
                

#    print paper.sources

    return paper
