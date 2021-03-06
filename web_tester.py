#!/usr/bin/env python

from getwebinfo import getwebinfo
import cookielib, urllib2

url = 'https://astrobites.org/2016/04/12/pursuing-eternal-youth-stellar-cannibalism-in-the-wilds-of-our-galaxy/'
url = 'http://www.sciencemag.org/news/2016/04/no-pressure-nsf-test-finds-eliminating-deadlines-halves-number-grant-proposals'
url = 'http://physicstoday.scitation.org/doi/full/10.1063/PT.3.3536'
url = 'http://www.preposterousuniverse.com/blog/2017/06/18/a-response-to-on-the-time-lags-of-the-ligo-signals-guest-post/'
url = 'http://iopscience.iop.org/article/10.3847/1538-4357/aa74e3/'

id = url
html = ''
# HTTP request for a webpage URL
try:
    ## Cookies Support
    cookies = cookielib.LWPCookieJar()
    handlers = [
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(cookies)
        ]
    opener = urllib2.build_opener(*handlers)
    
    ## Add headers to HTTP request so don't get 403 error
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    
    
    request = urllib2.Request(id, headers=hdr)
    
    html = opener.open(request).read()
    urlpage = id  # For compatibility down lower in the code
except urllib2.HTTPError, e:
    print e.code
    html = e.read()
    urlpage = id
    servererr = True
except:
    # Hm...didn't open, and not a 404 or something; try adding http://
    if (id.startswith('http://') is False):
        urlpage = 'http://' + id
        try:
            html = urllib3.urlopen(urlpage).read()
        except:
            # Ok...try adding www. if it's not there
            if (urlpage.startswith('http://www.') is False):
                urlpage = 'http://www.' + id
            try:
                html = urllib3.urlopen(urlpage).read()
            except:
                html = '<html><head>' + \
                       '<title>BAD LINK: ' + id + \
                       '</title>' + \
                       '</head><body></body></html>'
                servererr = True
    else:
        html = '<html><head>' + \
               '<title>BAD LINK: ' + id + \
               '</title>' + \
               '</head><body></body></html>'

paper = getwebinfo(url, html)
print(paper.title + '\n')
print(paper.author + '\n')
print(paper.date + '\n')
print(paper.abstract + '\n')
print(paper.sources + '\n')
print(paper.subject + '\n')
print(paper.url + '\n')
print(paper.errors + '\n')
