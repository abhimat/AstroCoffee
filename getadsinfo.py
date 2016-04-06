#!/usr/bin/env python


def getadsinfo(url, html):
    """Convert HTML from an ADS page to a preprint object."""
    # 2010-04-11       RTH: Created
    # 2010-05-02       RTH: Fixed accent bug, but removed direct author links

    from bs4 import BeautifulSoup
    import re
    import datetime
    import urllib
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

    # Grab the Title, Date, and Authors from the metadata in the header
    try:
        paper.title = soup.find(attrs={"name": "dc.title"})['content']
    except:
        paper.errors = "1"
        paper.title = "Error Grabbing Title"

    # Put the date in the same format as arXiv for consistency
    try:
        paper.date = soup.find(attrs={"name": "dc.date"})['content']
        dpart = paper.date.split('-')
        if len(dpart) == 3:   # If find 3 parts, then it's YYYY-MM-DD
            newdate = datetime.date(int(dpart[0]),
                      int(dpart[1]), int(dpart[2]))
            paper.date = newdate.strftime("%d %b %Y")
        elif len(dpart) == 2:  # If find 2 parts, then it's YYYY-MM
            newdate = datetime.date(int(dpart[0]), int(dpart[1]), 1)
            paper.date = newdate.strftime("%b %Y")
    except:
        paper.errors = "1"
        paper.date = "Error Grabbing Date"

    try:
        # Change accented characters into HTML friendly equivalents
        # I hate that this line is so long, but it kinda has to be.
        authors = unicode(soup.find(attrs={"name": "citation_authors"})['content']).encode('ascii', 'xmlcharrefreplace').split('.;')
        paper.numauth = len(authors)
        # Convert the authors to strings only, then print only some of them
        alist = []
        for i in authors:
            alist.append(i)
        paper.author = ', '.join(alist[0:4])
    except:
        paper.errors = "1"
        paper.numauth = 1
        paper.author = "Error Grabbing Authors"

    try:
        abstr = str(soup.dt.table.tr.td.a['href'])
        # Some hacks since I'm extracting an abstract from an <a href=...>
        abstr = abstr.rpartition('&')[0]  # Avoid ending &title=
        abstr = abstr.rpartition('&')[2].replace('text=', '', 1)
        abstr = urllib.unquote(abstr)  # Change %stuff to chars
        abstr = abstr.replace('\n', ' ')
        # Strip the HTML tags so we don't bork the look of the output
        abstr = BeautifulSoup(abstr)
        paper.abstract = ''.join(abstr.findAll(text=True))
    except:
        paper.errors = "1"
        paper.abstract = "Error Grabbing Abstract"

    htmllink = ''
    pdflink = ''
    arxivlink = ''
    giflink = ''
    try:
        rawlinks = soup.findAll('dt')
        for link in rawlinks[1:len(rawlinks)-1]:
            if 'link_type=EJOURNAL' in str(link):
                htmllink = str(link.a)
                # I've seen at least two different text labels for this so far
                htmllink = htmllink.replace(
                            'Electronic Refereed Journal Article (HTML)',
                            'HTML')
                htmllink = htmllink.replace(
                            'Electronic On-line Article (HTML)',
                            'HTML')
            elif 'link_type=ARTICLE' in str(link):
                pdflink = str(link.a)
                pdflink = pdflink.replace(
                            'Full Printable Article (PDF/Postscript)',
                            'PDF/PS')
                pdflink = pdflink.replace(
                            'Full Refereed Journal Article (PDF/Postscript)',
                            'PDF/PS')
            elif 'link_type=GIF' in str(link):
                giflink = str(link.a)
                giflink = giflink.replace(
                            'Full Refereed Scanned Article (GIF)', 'GIF')
                giflink = giflink.replace('Scanned Article (GIF)', 'GIF')
            elif 'link_type=PREPRINT' in str(link):
                arxivlink = str(link.a)
                arxivlink = arxivlink.replace('arXiv e-print', 'arXiv')
            else:
                pass
    except:
        pass

    paper.sources = htmllink + ' ' + pdflink + ' ' + giflink + ' ' + arxivlink

    return paper
