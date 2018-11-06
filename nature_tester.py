#!/usr/bin/env python

from getnatureinfo import getnatureinfo
from get_nature_info import get_nature_info
import urllib2

url = 'http://www.nature.com/articles/s41550-017-0166'
url = 'https://www.nature.com/articles/s41550-017-0224-z'
url = 'https://www.nature.com/articles/nature25149'
url = 'https://www.nature.com/articles/s41550-018-0603-0'
id = url
html = ''
# HTTP request for a webpage URL
try:
    ## Add headers to HTTP request so don't get 403 error
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    request = urllib2.Request(id, headers=hdr)
    
    html = urllib2.urlopen(request).read()
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
            html = urllib2.urlopen(urlpage).read()
        except:
            # Ok...try adding www. if it's not there
            if (urlpage.startswith('http://www.') is False):
                urlpage = 'http://www.' + id
            try:
                html = urllib2.urlopen(urlpage).read()
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

paper = get_nature_info(url, html)
print(paper.title + '\n')
print(paper.author + '\n')
print(paper.date + '\n')
print(paper.abstract + '\n')
print(paper.sources + '\n')
print(paper.subject + '\n')
print(paper.url + '\n')
