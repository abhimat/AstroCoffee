#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getwebinfo(url, html):
    """Convert HTML from a random webpage to a preprint object."""
    # 2010-04-05       RTH: Created
    # 2016-04-06    Abhimat: Switch over to using Instaparser
    # 2016-11-18    Abhimat: Switch back to using BeautifulSoup (Instaparser discontinued :(…)

    from bs4 import BeautifulSoup
    import re
    from astroph import preprint
    import datetime
    
    # import json
    # import requests
    
    paper = preprint()
    
    # paper.errors = "0"
    #
    # # Use Instaparser to parse the article
    # ip_api_key = 'b4a72359c1ba49569df55a9ccfcc1390'
    #
    # ip_params = {'api_key': ip_api_key, 'url': url}
    #
    # try:
    #     ip_response = requests.get('https://www.instaparser.com/api/1/article', params=ip_params)
    #     ip_data = json.loads(ip_response.text)
    # except:
    #     paper.errors = "1"
    #     print("Error grabbing webpage from Instaparser")
    #
    # # print(ip_response.url)
    # # print(ip_response.status_code)
    # # print(ip_data)
    # # print(ip_data['title'])
    # # print(ip_data['author'])
    # # print(ip_data['description'].encode("utf-8"))
    #
    # paper.url = url
    #
    # paper.sources = 'Web Article'
    # paper.subject = ''
    # paper.comments = ''
    #
    # try:
    #     paper.title = ip_data['title'].encode("utf-8")
    #     print(paper.title)
    # except:
    #     paper.errors = "0"
    #     paper.title = "[Error grabbing title]"
    #     print("Error grabbing title")
    #
    # try:
    #     date = ip_data['date']
    #     # print(date)
    #     paper.date = datetime.datetime.fromtimestamp(int(date)).strftime('%d %b %Y')
    # except:
    #     paper.errors = "0"
    #     paper.date = " "
    #     # print("Error grabbing Date")
    #
    # try:
    #     paper.numauth = 1
    #     paper.author = ip_data['author'].encode("utf-8")
    # except:
    #     paper.errors = "0"
    #     paper.author = " "
    #     # print("Error grabbing authors")
    #
    # try:
    #     paper.abstract = ip_data['description'].encode("utf-8")
    # except:
    #     paper.errors = "0"
    #     paper.abstract = " "
    #     # print("Error grabbing description")
    
    paper.url = url
    # Remove all the muck that screws up the BeautifulSoup parser
    # Will fail on PDF submission, so take care of that exception first
    try:
        fhtml =re.sub(re.compile("<!--.*?-->", re.DOTALL), "", html)
        soup = BeautifulSoup(fhtml, from_encoding='utf-8')
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
    
    # print(soup.head.title)
    
    # Grab the Title from the title tag
    try:
        paper.title = soup.head.title.text.encode("utf-8")
    except:
        paper.errors = "1"
        paper.title = 'Error Grabbing Title'
    
    print('')
    print(url)
    print(paper.title)
    print('')
    
    paper.numauth = 1
    paper.date = '[ Date ]'
    paper.author = ''
    paper.abstract = ''
    paper.sources = 'Web Article'
    paper.subject = ''
    paper.comments = ''
    
    return paper
