#coding:utf-8
from bs4 import BeautifulSoup
import re
import urlparse
class parser(object):
       
    
    def trim_links(self,url):
        a=url.replace('http://','')
        b=a.replace('https://','')
        position=b.find('/')
        if position>2:
            return b[0:position]
        else:
            return b    
#get top topdomian from result
    def get_top_domains(self,html):
        
        soup=BeautifulSoup(html,'html.parser')
        links=soup.find_all('font',color="green")
        top_domains=set()
        
        for link in links:
            link=link.get_text()
            top_domain=self.trim_links(link)
            top_domains.add(top_domain)
        return top_domains
#get pages in search result   
    def getpages(self,html,sengine):
        psoup=BeautifulSoup(html,'html.parser')
        pages_res=psoup.find_all('a',href=re.compile(r'start'))
        pages=set()
        i=1
        for page in pages_res:
            if i==1:
                i=i+1
                continue
            page=urlparse.urljoin(sengine,page['href'])
            pages.add(page)
        return pages
    

    
    def get_domain_descript(self,content):
        pass

    
    def get_domain_tile(self,content):
        try:
            soup=BeautifulSoup(content,"html.parser")
            title=soup.title
            title=title.encode('utf8')                          
            title=title[7:-8]
            title=unicode(title,'utf8')
            title=title.replace('"','' )
            title=title.replace("'","'")
        except:       
            title='null'
            
 
            
        return title


    
    def get_domain_keywords(self,content):
        pass

    
    def get_emails(self,content):
        
        content=content.replace('<', ' ')
        content=content.replace('>', ' ')
        content=content.replace('"', ' ')
        content=content.replace('=', ' ')
        content=content.replace("'", " ")
        
        regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)          
        emails = re.findall(regex, content)
        new_mails=set()
        if len(emails)>0:
            max_mail_length=8
            i=0
            for email in emails:
                new_mails.add(email)
                i=i+1
                if i>max_mail_length:
                    break
        return new_mails
            
            

    
    def get_home_page_urls(self,html,domain):
        try:
            psoup=BeautifulSoup(html,'html.parser')
        except:
            try:
                psoup=BeautifulSoup(html.encode('utf-8'),'html.parser')
            except:
                html='null'
                psoup=BeautifulSoup('null','html.parser')
                        
            
        
        urls_res=psoup.find_all('a')
        urls=set()
        for url in urls_res:
            try:
                url=urlparse.urljoin(domain,url['href'])
            except:
                continue
           
            if url.find(domain[8:13])>0:
                urls.add(url)
        return urls

    
    def get_domain_text(self,homepagecode):
        soup = BeautifulSoup(homepagecode,"html.parser")
        
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())       
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    
    
    
    
    
    
    
    
    
    
    
    
        
            
    
    
    





