# -*-coding:utf-8 -*-
# data = 15-12-1
from lxml import etree
import random
import requests
import time
from utils import get_top_domain, get_google_emails,query_google

__author__ = 'Tesla.yang'


user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
]

first_url = "https://www.google.com"
timeout = 10


from subprocess import Popen, PIPE, STDOUT
class MyException(Exception):
    pass


"scutil --nc start pptp  --password wutaobao99"
def _do_cmd(cmd):
    try:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        while p.poll() is None:
            for line in iter(p.stdout.readline, b''):
                print line
            p.stdout.close()
        p.wait()
        p.kill()
        return
    except:
        pass

        # route add -net 116.236.168.0 netmask 255.255.255.0 gw 69.171.76.1
        # route add -net 103.79.76.0 netmask 255.255.255.0 gw 69.171.76.1
        # route add -net  27.38.32.0 netmask 255.255.255.0 gw 69.171.76.1
"""
ip route add    64.18.0.0/20   dev ppp0
"ip route add    64.233.160.0/19  dev ppp0"
"ip route add    66.102.0.0/20  dev ppp0"
"ip route add    66.249.80.0/20  dev ppp0"
"ip route add    72.14.192.0/18  dev ppp0"
"ip route add    74.125.0.0/16  dev ppp0"
"ip route add    108.177.8.0/21  dev ppp0"
"ip route add    173.194.0.0/16  dev ppp0"
"ip route add    207.126.144.0/20  dev ppp0"
"ip route add    209.85.128.0/17  dev ppp0"
"ip route add    216.58.192.0/19  dev ppp0"
"ip route add    216.239.32.0/19  dev ppp0"
"""

def main():
    import SqlManager
    sql_manager = SqlManager.Sqlmanger()
    domains=sql_manager.get_match_domains()#获取未使用的关键字
    for domain in domains:
        domain=domain.replace('www.','')
        search_word=domain+" keyword"
        print 'start vpn... for search email  ----'+keyword
    
    
    

    keywords = sql_manager.getkeywords()  # 获取未使用的关键字

    for keyword in keywords:
        print 'start vpn... for keyword  ----'+keyword
        _do_cmd('/usr/bin/poff pptp01')
        _do_cmd('/usr/bin/pon pptp01')
        time.sleep(10)
        _do_cmd('ip route add    64.18.0.0/20   dev ppp0')
        _do_cmd("ip route add    64.233.160.0/19  dev ppp0")
        _do_cmd("ip route add    66.102.0.0/20  dev ppp0")
        _do_cmd("ip route add    66.249.80.0/20  dev ppp0")
        _do_cmd("ip route add    72.14.192.0/18  dev ppp0")
        _do_cmd("ip route add    74.125.0.0/16  dev ppp0")
        _do_cmd("ip route add    108.177.8.0/21  dev ppp0")
        _do_cmd("ip route add    173.194.0.0/16  dev ppp0")
        _do_cmd("ip route add    207.126.144.0/20  dev ppp0")
        _do_cmd("ip route add    209.85.128.0/17  dev ppp0")
        _do_cmd("ip route add    216.58.192.0/19  dev ppp0")
        _do_cmd("ip route add    216.239.32.0/19  dev ppp0")


        try:
            spider(keyword)
        except Exception as e:
            print e
            continue
        _do_cmd('/usr/bin/poff pptp01')
        time.sleep(1)
        sql_manager.update_keyword_use(keyword)
        sql_manager.commit()
        # _do_cmd('route add  default gw  69.171.76.1')

def spider(keyword):
    # ips = get_ips()
    # if len(ips) > 0:
    #     proxy_ip = ips.pop()
    # else:
    #     ips = get_ips()
    #     proxy_ip = ips.pop()
    # proxy_ip  = proxy_ip.strip()
    request_session = requests.session()
    # request_session.proxies = {'http': 'socks5://%s'%proxy_ip,
    #                    'https': 'socks5://%s'%proxy_ip}

    # print request_session.proxies
    user_agent = random.choice(user_agents)

    old_url, content = query_google(request_session,
                           first_url,
                           referer=None,
                           proxies=None,
                           user_agent =user_agent)

    time.sleep(random.choice([1.1, 0.5, 0.55, 0.3, 2]))

    next_url = "https://www.google.com/search?source=hp&q=%s&btnK=Google+Search"%keyword

    old_url, content = query_google(request_session,
                           next_url,
                           referer=old_url,
                           proxies=None,
                           user_agent =user_agent)
    lxml_tree = etree.HTML(content)
    url_content = lxml_tree.xpath(u'//noscript/meta')[0].get('content') #0;url=/search?q=123123&gbv=1&sei=e2WWWcOxJOWb0gLUz6zACw

    next_url = first_url + url_content[6:]
    for i in range(1, 12):
        print next_url
        old_url, content = query_google(request_session,
                     next_url,
                     referer=old_url,
                     proxies=None,
                     user_agent=user_agent)
        get_top_domain(content)
        google_tree = etree.HTML(content)
        try:
            next_url =first_url +  google_tree.xpath("//td/a[@class='fl']")[-1].attrib.get('href')
        except Exception as e:
            print e
            raise
        time.sleep(random.choice([1.1, 0.5, 0.55, 0.3, 2]))
 
 
 
 
 
 
 
         
                
def spiser_email(keyword):

    request_session = requests.session()
    user_agent = random.choice(user_agents)
    old_url, content = query_google(request_session,
                           first_url,
                           referer=None,
                           proxies=None,
                           user_agent =user_agent)

    time.sleep(random.choice([1.1, 0.5, 0.55, 0.3, 2]))
    next_url = "https://www.google.com/search?source=hp&q=%s&btnK=Google+Search"%keyword
    old_url, content = query_google(request_session,
                           next_url,
                           referer=old_url,
                           proxies=None,
                           user_agent =user_agent)
    lxml_tree = etree.HTML(content)
    url_content = lxml_tree.xpath(u'//noscript/meta')[0].get('content') 

    next_url = first_url + url_content[6:]
    for i in range(1, 3):
        print next_url
        old_url, content = query_google(request_session,
                     next_url,
                     referer=old_url,
                     proxies=None,
                     user_agent=user_agent)
        get_top_domain(content)
        google_tree = etree.HTML(content)
        try:
            next_url =first_url +  google_tree.xpath("//td/a[@class='fl']")[-1].attrib.get('href')
        except Exception as e:
            print e
            raise
        time.sleep(random.choice([1.1, 0.5, 0.55, 0.3, 2]))    

if __name__ == '__main__':
    main()