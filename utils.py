#coding:utf-8

import re

import requests
from lxml import etree


def get_top_domain(content):
    google_tree = etree.HTML(content)
    google_result = google_tree.xpath('//cite')

    from urlparse import urlparse
    for e in google_result:
        string_href = etree.tostring(e)
        if not string_href:
            continue
        text = re.sub('<[^(<>)]*>', '', string_href)
        if not text:
            continue
        if  not text.startswith('http'):
            text = "http://%s"%text
        url_parse = urlparse(text)
        with open('result.txt', 'a') as f:
            hostname = url_parse.hostname
            if hostname:
                f.write(hostname.encode('utf-8'))
                f.write('\n')
                
                
    

def query_google(request_session, url, referer, user_agent, proxies):
    header = {'User-Agent': user_agent,
              'Accept':"text/html,application/xhtml+x…lication/xml;q=0.9,*/*;q=0.8",
              "Accept-Language":"en-US,en;q=0.5",
              "Accept-Encoding":"deflate",
              'Connection': 'keep-alive',
              }
    if referer:
        header['Referer'] = referer
    req = request_session.get(url, headers=header,verify=False, timeout=10)
    return req.url, req.content


def get_ips():
    """ 获取ip """
    proxy_api = 'http://filefab.com/api.php?l=W10BDsmkeAX36_7UhZyWiXFne-1gp7agLlic_1L0z1c'
    content = requests.get(proxy_api).content
    content = content.replace('</pre>', '').replace('<pre>', '')
    content = content.strip()
    ips = content.split('\n')
    return ips