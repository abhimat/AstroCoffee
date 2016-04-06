#!/usr/bin/env python


def getwebinfo(url, html):
    """Convert HTML from a random webpage to a preprint object."""
    # 2010-04-05       RTH: Created

    from bs4 import BeautifulSoup
    import re
    from astroph import preprint
    
    import json
    import requests
    
    paper = preprint()
    
    # Use Instaparser to parse the article
    ip_api_key = 'b4a72359c1ba49569df55a9ccfcc1390'
    
    ip_params = {'api_key': ip_api_key, 'url': url}
    
    ip_response = requests.get('https://www.instaparser.com/api/1/article', params=payload)
    ip_data = json.loads(ip_response.text)
    
    paper.url = ip_data['url']
    paper.title = ip_data['title']
    paper.numauth = 1
    paper.author = ip_data['author']
    paper.abstract = ip_data['description']
    paper.date = 'Web Article:'
    paper.sources = ''
    paper.subject = ''
    paper.comments = ''
    
    # paper.url = url
    # # Remove all the muck that screws up the BeautifulSoup parser
    # # Will fail on PDF submission, so take care of that exception first
    # try:
    #     fhtml =re.sub(re.compile("<!--.*?-->", re.DOTALL), "", html)
    #     soup = BeautifulSoup(fhtml)
    #     paper.errors = "0"
    # except:
    #     paper.errors = "1"
    #     paper.title = "Error Grabbing Title"
    #     paper.author = "Error Grabbing Authors"
    #     paper.numauth = "1"
    #     paper.date = "Error Grabbing Date"
    #     paper.abstract = "Error Grabbing Abstract"
    #     paper.sources = " "
    #     paper.subject = "Error Grabbing Subject"
    #     paper.comments = "Error Grabbing Comments"
    #     return paper
    #
    # # Grab the Title from the title tag
    # try:
    #     paper.title = soup.head.title.string
    # except:
    #     paper.errors = 1
    #     paper.title = 'Error Grabbing Title'
    #
    # paper.numauth = 1
    # paper.date = 'Web Article:'
    # paper.author = ''
    # paper.abstract = ''
    # paper.sources = ''
    # paper.subject = ''
    # paper.comments = ''

    return paper
