#!/usr/bin/env python

# Test ApJ article parser
# ---
# Abhimat Gautam

from getarxivinfo import getarxivinfo
import urllib2, ssl

url = 'https://arxiv.org/abs/1904.10977'
url = 'https://arxiv.org/abs/2004.06685'
id = url
html = ''
# HTTP request for a webpage URL

## Add headers to HTTP request so don't get 403 error
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


ssl._create_default_https_context = ssl._create_unverified_context
context = ssl._create_unverified_context()

request = urllib2.Request(id, headers=hdr)

html = urllib2.urlopen(request, context=context).read()

urlpage = id  # For compatibility down lower in the code
    
try:
    ## Add headers to HTTP request so don't get 403 error
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


    ssl._create_default_https_context = ssl._create_unverified_context
    context = ssl._create_unverified_context()

    request = urllib2.Request(id, headers=hdr)

    html = urllib2.urlopen(request, context=context).read()
    
    urlpage = id  # For compatibility down lower in the code
except urllib2.HTTPError, e:
    print e.code
    html = e.read()
    urlpage = id
    servererr = True
except:
    # Hm...didn't open, and not a 404 or something; try adding https://        
    if (id.startswith('https://') is False):
        urlpage = 'https://' + id
        try:
            html = urllib2.urlopen(urlpage).read()
        except:
            # Ok...try adding www. if it's not there
            if (urlpage.startswith('https://www.') is False):
                urlpage = 'https://www.' + id
            try:
                html = requests.get(urlpage).text
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
    urlpage = id

paper = getarxivinfo(url, html)
print(paper.title + '\n')
print(paper.author + '\n')
print(paper.date + '\n')
print(paper.abstract + '\n')
print(paper.sources + '\n')
print(paper.subject + '\n')
print(paper.url + '\n')
print(paper.errors + '\n')
