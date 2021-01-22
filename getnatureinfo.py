#!/usr/bin/env python


def getnatureinfo(url, html):
    """Convert HTML from a Nature journal page to a preprint object."""
    # 2010-03-26       RTH: Phoenix version, rewritten using BeautifulSoup
    # 2010-05-01       RTH: Why must Nature make such a gnarly page?
    #                         numerous fixes and changes, shouldn't bork the
    #                         entire page if something isn't found anymore

    from bs4 import BeautifulSoup
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
    
    # Grab the title
    try:
        paper.title = soup.find(attrs={"name": re.compile("dc.title", re.I)})['content']
    except:
        paper.errors = "1"
        paper.title = "Error Grabbing Title"
#    print paper.title

    # Grab the date
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
#    print paper.date

    # Grab the authors
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
    
    # Get the abstract as one big long string, sans any html or script crap
    #   this does keep the footnote numbers unfortunately, but big whoop
    paper.abstract = ''
    
    paper.abstract = ''.join(soup.find(
                             "div",
                             attrs={"id": "Abs1-content"}).findAll(text=True))
    print('I got here!')
    
    try:
        paper.abstract = ''.join(soup.find(
                                 "div",
                                 attrs={"id": "Abs1-content"}).findAll(text=True))
        print('I got here!')
    except:
        try:
            paper.abstract = ''.join(soup.find(
                             "p",
                             attrs={"class": "intro"}).findAll(text=True))
        except:
            paper.abstract = ''.join(soup.find(
                             "meta",
                             attrs={"name": "description"})['content'])
    
    if paper.abstract == 'None' or paper.abstract == '':
        paper.abstract = "Error Grabbing Abstract"
    else:
        # Convert Unicode chars to displayable characters
        paper.abstract = paper.abstract.encode('ascii', 'xmlcharrefreplace')

    # Could be more of these necessary in the future to purge their CSS things
    paper.title = paper.title.replace('|[thinsp]|', ' ')
    paper.abstract = paper.abstract.replace('|[thinsp]|', ' ')
    paper.abstract = paper.abstract.replace('[plusmn]', '+/-')

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
#    print htmllink

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
#    print pdflink

    if pdflink == 'None':
        pdflink = ''

    htmllink = htmllink.replace('Full text', 'HTML')
    paper.sources = htmllink + ' ' + pdflink
    
    # paper.errors = "0"
    print paper.abstract
    
    print('I got here!')
    
    return paper
