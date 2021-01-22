#!/usr/bin/env python

def getvixrainfo(url, html):
    """Convert HTML from a viXra page to a preprint object."""

    from bs4 import BeautifulSoup
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
    
    ## Grab title
    try:
        paper.title = 'viXra: ' + soup.find('div',  {'id':'flow'}).h2.string
    except:
        paper.errors = "1"
        paper.title = "Error Grabbing Title"
    
    # print(paper.title + '\n')
    
    ## Grab authors
    try:
        authors = soup.find('div',  {'id':'flow'}).p
        authors = authors.findAll('a')
        paper.numauth = len(authors)
        # Convert the authors to strings only and replace the relative links
        alist=[]
        for i in authors:
            alist.append(str(i).replace('/author/','http://vixra.org/author/'))
        paper.author = ', '.join(alist[0:4])
        # Kill all affiliation marks since some have them and some don't;
        #   done in two steps to take care of nested parens
        paper.author = re.sub(r'\([^()]*\)','',paper.author)
        paper.author = re.sub(r'\([^()]*\)','',paper.author)
    except:
        paper.errors = "1"
        paper.author = "Error Grabbing Authors"
    
    # print(paper.author + "\n")
    
    ## Grab dates
    try:
        ## Go through flow text
        date = soup.find('div', {'id':'flow'})
        date = date.findAll('p')
        
        ## Look through p tags until we get to the date text
        date_index = 0
        while not((date[date_index].text).startswith('[v1]')):
            date_index += 1
        
        ## Pull out the most recent date
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        date = date[date_index].findAll(text=True)  # Remove HTML tags
        date = date[len(date) - 2]                  # Last date will be second to last item
        split_date = date.split()
        split_date = split_date[1].split('-')
        paper.date = '{0} {1} {2}'.format(split_date[2], months[int(split_date[1]) - 1], split_date[0])
    except:
        paper.errors = "1"
        paper.date = "Error Grabbing Date"
    
    # print(paper.date + '\n')
    
    ## Grab abstract
    try:
        paper.abstract = soup.find('div',{'id':'abstract'}).text
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"

    # print(paper.abstract + '\n')
    
    ## Grab sources
    try:
        ## Go through flow text
        sources = soup.find('div', {'id':'flow'})
        sources = sources.findAll('p')
        
        ## Look through p tags until we get to the data text
        sources_index = 0
        while not((sources[sources_index].text).startswith('Download')):
            sources_index += 1
        
        sources = sources[sources_index].findAll('a')
        slist = []
        
        for i in sources:
            curstring = str(i)
            curstring = curstring.replace('/ps','http://vixra.org/ps')
            curstring = curstring.replace('/pdf','http://vixra.org/pdf')
            curstring = curstring.replace('/format','http://vixra.org/format')
            curstring = curstring.replace('<b>PDF</b>','PDF')
            curstring = curstring.replace('<b>PostScript</b>','PS')
            curstring = curstring.replace('<b>Other formats</b>','Other')
            slist.append(curstring)
        
        paper.sources = ' '.join(slist)
    except:
        paper.errors = "1"
        paper.sources = ''

    # print(paper.sources + '\n')
    
    ## Grab subject
    try:
        paper.subject = soup.find('div',  {'id':'category'}).td.h2.string
    except:
        paper.errors = "1"
        paper.subject = "Error Grabbing Subject"
    
    # print(paper.subject + '\n')
    
    ## Grab paper ID and generate paper URL
    paperid = soup.find(attrs={"name":re.compile("citation_vixra_id",re.I)})['content']
    # print(paperid)
    
    paper.url = 'http://vixra.org/abs/' + paperid
    
    return paper
