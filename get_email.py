# coding=utf8
from gevent import monkey
from __builtin__ import str
from compiler.syntax import check
monkey.patch_all()
from gevent.pool import Pool

import requests
import re
from urlparse import urlparse
import copy

import SqlManager
import htmlparser

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0',
          'Accept': "text/html,application/xhtml+x…lication/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.5",
          "Accept-Encoding": "deflate",
          'Connection': 'keep-alive',
          }

class Crawler(object):
    def __init__(self, url, domain):
        self.crawlername = ''
        self.domain = domain
        self.url = url
        self.g_queueURL = set()  # 等待爬取的url链接列表
        self.g_existURL = set()  # 已经爬取过的url链接列表
        self.g_failedURL = []    # 下载失败的url链接列表
        self.g_queueURL.add(self.url)
        self.depth = 0
        self.root = True
        self.parse_email = SearchEmail()
        self.root_host = urlparse(url)
        self.SqlManager = SqlManager.Sqlmanger()

    def craw(self):
        
        print self.crawlername + "启动..."        
        self.SqlManager.update_domain_use_before_check(self.domain)#更新使用域名        
        homepagecontent=self.get_home_page_content(self.domain)
        match_keyword=self.parse_email.parse_root_html(homepagecontent, self.domain)
        
        if len(match_keyword) > 4:  # 如果抓取到匹配关键字则进行内部抓:
            self.SqlManager.update_match_keyword(self.domain, match_keyword)#更新匹配域名
            emails=set()      
            while self.g_queueURL:
                self.depth += 1
                print 'Searching depth ', self.depth, '...\n\n'
                g_queueURL = copy.deepcopy(self.g_queueURL)
                for url in g_queueURL:
                    self.g_queueURL.remove(url)
                    if url in self.g_existURL:
                        continue
                    content = self.download(url)                    
                    mails=self.parse_email.parse_html(content, self.domain)
                    if len(mails):
                        for mail in mails:
                            emails.add(mail)
                if self.depth > 1:
                    break
            self.SqlManager.insert_emails(emails,self.domain)
    
    def get_home_page_content(self,root_url):#获取首页关键字
        url="http://"+root_url
        page = requests.get(url, headers=header, verify=False, timeout=20)
        html = page.content
        return html
    
    def download(self, root_url):
        page = requests.get(root_url, headers=header, verify=False, timeout=13)
        html = page.content
        reg = "(?<=href=\")[^\"]+"
        regob = re.compile(reg, re.DOTALL)
        urllist = regob.findall(html)
        for url in urllist:
            url = url.strip()
            if not url:
                continue
            if not url.startswith('/') and not url.startswith('http'):
                continue

            if url.startswith('/'):
                url = "http://%s%s"%(self.root_host.hostname,url)
            if "%s"%self.root_host.hostname not in url:
                continue
            parse_result = urlparse(url)
            if parse_result.path.lower().endswith(".jpg") or \
                    parse_result.path.lower().endswith(".jpeg") or \
                    parse_result.path.lower().endswith(".png") or \
                    parse_result.path.lower().endswith(".gif") or \
                    parse_result.path.lower().endswith(".css") or \
                    parse_result.path.lower().endswith(".js") or \
                    parse_result.path.lower().endswith(".mp4") or \
                    parse_result.path.lower().endswith(".ico"):
                continue
            if url not in self.g_existURL:
                self.g_queueURL.add(url)
        self.g_existURL.add(root_url)
        return html


class SearchEmail(object):  # 爬去站内的邮箱帐号
    def __init__(self):
        self.SqlManager = SqlManager.Sqlmanger()
        self.htmlParser =htmlparser.parser()
        self.keyword_base = SqlManager.Sqlmanger().get_orkeywords()  # h获取基础关键字， 用于检查下载的文本是否匹配基础关键字
        self.badwords = SqlManager.Sqlmanger().get_badwords()  # 获取过滤关键字
        self.bad_titles= SqlManager.Sqlmanger().get_bad_titles()


    def check_content_match(self, text):  # 检查网页代码是否包含匹配关键字
        return_keyword = set()
        for keyword in self.keyword_base:
            keyword = keyword.encode('utf-8') if isinstance(keyword, unicode) else keyword
            if text.find(keyword.lower()) > 0:
                print keyword
                return_keyword.add(keyword)

        match_keyword = ', '.join(return_keyword)
        print match_keyword
        return match_keyword

    def check_bad_words(self, web_code_text):  # 检查网页代码是否包含过滤关键字
        return_filterword = set()
        for filterword in self.badwords:
            filterword = filterword.encode('utf-8') if isinstance(filterword, unicode) else filterword

            if web_code_text.find(filterword) > 0:
                print 'bad--keyword-------'+filterword
                return_filterword.add(filterword)
        return return_filterword
    
    
    def check_bad_titles(self, title):  # 检查网页代码是否包含中国网址的关键字
        return_filterword = set()
        title=title.encode('utf-8') if isinstance(title, unicode) else title
        for filterword in self.bad_titles:
            filterword = filterword.encode('utf-8') if isinstance(filterword, unicode) else filterword

            if title.find(filterword) > 0:
                print 'bad--title-------'+filterword
                return_filterword.add(filterword)
        return return_filterword
    
    def parse_root_html(self, homepagecode ,domain):
        title = self.htmlParser.get_domain_tile(homepagecode)  # 获取王站点首页的标题      
        self.SqlManager.update_domain_use(domain, title)  # 更新标题使用情况
        
        web_code_text = homepagecode.lower()  # 获取源码文本并全部转化大小写
        badwords = self.check_bad_words(web_code_text)
        bad_titles = self.check_bad_titles(title)  
        match_keyword = self.check_content_match(homepagecode)
        print "match keyword is -------"
        print match_keyword
            
        if len(badwords) > 0 or len(bad_titles)>0:
            match_keyword=""
        
        return match_keyword


    def parse_html(self, homepagecode, domain):
        emails = set()  # 色绘制email素组
        #content = self.htmlParser.get_domain_text(homepagecode)
        mails = self.htmlParser.get_emails(homepagecode)
        for mail in mails:
            emails.add(mail)
        
        return emails
        
        


def find_email(domain):
    root_url = "http://%s"%domain
    # print root_url
    c = Crawler(root_url, domain)
    c.craw()

if __name__ == "__main__":
    sqlm = SqlManager.Sqlmanger()
    # sqlm.del_bad_domains()
    domains = sqlm.get_good_domains()
    
    p = Pool(60)
    basename = 'get_email-thread-'
    n=0
    for domain in domains:
        # p.apply_async(find_email, (domain,))
        try:
            p.apply_async(find_email, (domain,))
        except KeyboardInterrupt:
            import sys
            sys.exit(200)
        except:
            pass
    p.join()
