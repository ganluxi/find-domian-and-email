#coding:utf-8
import random
import traceback
from __builtin__ import str

import MySQLdb
import config


class Sqlmanger(object):
    def __init__(self):
        conninfo= config.config()
        info=conninfo.get_sql_connect_info()      
        self.conn=MySQLdb.connect(host=info['host'],port=info['port'], user=info['user'],passwd=info['passwd'],db=info['db'],charset=info['charset'])
        self.cursor=self.conn.cursor()


    #获取待谷歌爬取的关键字
    def getkeywords(self):
        sql='SELECT * FROM keyword where usecount=0 LIMIT 100'
        self.cursor.execute(sql)
        keyres=self.cursor.fetchall()
        keywords=set()
        for keyword in keyres:
            #keyword=str(keyword[1])
        
            keywords.add(keyword[1])
        return keywords

    #把爬取回来的域名保存到数据库
    def insert_top_domains(self,tsites):
        
        badwords = self.get_bad_domains()  # 获取过滤关键字 
        for tsite in tsites:#剔除掉不符合要求关键字
            is_insert=1
            tsite=encode('utf-8') if isinstance(tsite, unicode) else tsite    
                   
            for filterword in badwords:
                filterword = filterword.encode('utf-8') if isinstance(filterword, unicode) else filterword
                
                if tsite.find(filterword)>-1:
                    print filterword+'-------'+tsite
                    is_insert=0
                    break
            
            if is_insert>0:     
                sql='insert into domain(domain) values("'+tsite+'")'
                try:
                    self.cursor.execute(sql)
                    print 'new domain:--'+tsite
                except:
                    pass



    def update_keyword_use(self,keyword):
        
        sql='update keyword set usecount=usecount+1 where keyword="'+keyword+'";'
        self.cursor.execute(sql)
    

 


    #获取微未进行内部爬取的域名
    def getdomains(self,start_num,end_num):
        start_num=str(start_num)
        end_num=str(end_num)
        sql='select domain from domain where usecount=0 LIMIT '+start_num+','+end_num

        self.cursor.execute(sql)
        domins=self.cursor.fetchall()
        domains=set()
        for domain in domins:
            domains.add(domain[0])
        return domains
    
    #更新使用过的域名标题
    def update_domain_use(self,domain,title):
        
        sql='update domain set title="%s" where domain="%s"'%(title, domain)
        print sql
        self.cursor.execute(sql)  

    #更新使用过的域名的是否使用字段
    def update_domain_use_before_check(self,domain):
        sql='update domain set usecount=1 where domain="%s"'%domain
        print sql
        self.cursor.execute(sql) 
 


    #提取标题中含有目标关键字的域名
    def get_good_domains(self):
        #self.cursor.execute("call del_bad_domains()") 
        
        sql="SELECT domain from domain where usecount=0 LIMIT 100"  
        print 'get good domains from database'       
        self.cursor.execute(sql)
        doms=self.cursor.fetchall()
        domains=[]
        for domain in doms:
            domains.append(domain[0])
        return domains
            

    
    #更新查找到的邮箱数
    def insert_emails(self,emails,domain):
        i=0
            
        for email in emails:
            try:                          
                sql="insert into edm_email_list(email,from_domain) values('"+email+"','"+domain+"')"
                self.cursor.execute(sql)
                print domain+'---'+'great we get new email '+email
            except:
                print domain+'---'+'this email already exist: '+email
            
            
            try:
                pid=str(self.get_domain_id(domain))
                sql2="insert into base_email(email,from_domain,pid) values('"+email+"','"+domain+"',"+pid+")" 
                self.cursor.execute(sql2)
                print "you get a email "+email
            except:
                traceback.print_exc()
            i=i+1
            if i>8:
                break
                   
        findcount=str(self.get_find_count(domain))
        self.update_find_count(findcount, domain)
            
    #更新实用过的域名
    def domain_inner_crawl(self,domain):
        try:
            sql="update domain set IsInnerCrawl=1 where domain='"+domain+"'"
            self.cursor.execute(sql)  
            print 'update inneruser '+domain+' done'          
        except:
            traceback.print_exc()
    
    
    
    #获取原始关键字(未添加地理位置的后缀的)
    def get_orkeywords(self):
        sql='select keyword from keyword_base'

        self.cursor.execute(sql)
        keyres=self.cursor.fetchall()
        keywords=set()
        for keyword in keyres:
            #keyword=str(keyword[1])
        
            keywords.add(keyword[0])
        return keywords

    #更新标题包含关键字的域名
    def update_title_match(self,keyword):
        sql="UPDATE domain set title_macth=1 and usecount=1 where match_check=0 and title LIKE '%"+keyword+"%'"
        self.cursor.execute(sql)
        

    
    def update_match_check(self):
        sql='UPDATE domain set match_check=1 where usecount=1'
        self.cursor.execute(sql)

    




    
    def update_match_keyword(self,domain,match_keyword):
        
        sql='update domain set match_keyword="%s",title_macth=1 where domain="%s"'%(match_keyword, domain)
        print sql
        self.cursor.execute(sql)
        


    def get_send_mails(self):
        sql = 'select email from send_list '
        self.cursor.execute(sql)
        email_res=self.cursor.fetchall()
        emails=[]
        for email in email_res:        
            emails.append(email[0])
        return emails

    
    def send_count(self,email):
        sql='update edm_email_list set send_count=send_count+1 where email="'+email+'"'
        self.cursor.execute(sql) 

    
    def update_send_success(self,email):
        sql='update edm_email_list set send_success=send_success+1 where email="'+email+'"'
        print 'send email '+email+' success'
        self.cursor.execute(sql)

    
    def update_send_fail(self,email):
        sql='update edm_email_list set send_fall=send_fall+1 where email="'+email+'"'
        print 'send email '+email+' fail'
        self.cursor.execute(sql)
    
    
    def get_mailcontent(self):
        sql='select subject,body from mailcontent'
        self.cursor.execute(sql)
        content=self.cursor.fetchall()
            
        tsq=random.randint(0,8)
        return content[tsq]

    
    def del_bad_domains(self):
        sql='call del_bad_domains()'
        self.cursor.execute(sql)
        print 'delete bad domain success'

    #get base keyword key table keyword
    def get_badwords(self):
        sql='select keyword from badwords'

        self.cursor.execute(sql)
        keyres=self.cursor.fetchall()
        keywords=set()
        for keyword in keyres:
            #keyword=str(keyword[1])
        
            keywords.add(keyword[0])
        return keywords
    
    def get_bad_domains(self):
        sql='select keyword from bad_domains'

        self.cursor.execute(sql)
        keyres=self.cursor.fetchall()
        keywords=set()
        for keyword in keyres:
            #keyword=str(keyword[1])
        
            keywords.add(keyword[0])
        return keywords
    
    def get_bad_titles(self):
        sql='select keyword from bad_titles'
        self.cursor.execute(sql)
        keyres=self.cursor.fetchall()
        keywords=set()
        for keyword in keyres:
            #keyword=str(keyword[1])
        
            keywords.add(keyword[0])
        return keywords 
       
    
    def get_domain_id(self,domain):
        sql="select id from domain where domain='"+domain+"'"
        self.cursor.execute(sql)
        pidarr=self.cursor.fetchall()
        pid=pidarr[0][0]
        return pid
    
    def get_find_count(self,domain):
        sql="select count(*) from base_email where from_domain like'"+domain+"'"
        self.cursor.execute(sql)
        pidarr=self.cursor.fetchall()
        return pidarr[0][0]       
        

    def update_find_count(self,find_count,domain):
        
        sql="UPDATE domain set findcount="+find_count+" where domain='"+domain+"'"
        print sql
        self.cursor.execute(sql) 
    
    def get_from_domains(self):
        sql ="SELECT DISTINCT from_domain from base_email;"    
        self.cursor.execute(sql)
        doms=self.cursor.fetchall()
        domains=[]
        for domain in doms:
            domains.append(domain[0])
        return domains
    
    def get_match_domains(self):   
        sql="SELECT domain from domain where title_macth=1"  
        print 'get good domains from database'       
        self.cursor.execute(sql)
        doms=self.cursor.fetchall()
        domains=[]
        for domain in doms:
            domains.append(domain[0])
        return domains        

    def commit(self):
        try:
            self.conn.commit()
            self.cursor.close()
            self.cursor = self.conn.cursor()
        except Exception as e:
            print e

