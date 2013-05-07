#!/usr/bin/env python
#-*-coding:utf-8-*-

import re
import hashlib
import urllib2
from threadpool import ThreadPool
import parser
from BeautifulSoup import BeautifulSoup

class Spider(object):

    def __init__(self,seed,depth,pool_size=10):
        
        self.seed = seed
        self.depth = depth
        self.all_url_list = [seed]
        self.finished_url_list = []
        self.failure_url_list = []
        self.pool = ThreadPool(pool_size)

    def crawl(self):
        base_deep_size = 0
        while base_deep_size <= self.depth:
            for url in self.all_url_list:
                if url not in self.finished_url_list:
                    self.pool.add_task(self.download,url)
            self.pool.close()
            self.depth-=1

    def download(self,url):
        try:
            data = urllib2.urlopen(url)
            page = data.read()
            self.finished_url_list.append(url)
            links = self.get_urls(page)
            return page,links
        except Exception as e:
            print 'open url:%s raise exception(%s)'%(url,e)
            return None

    def get_urls(self,page):
        soup = BeautifulSoup(page,fromEncoding="gb18030")
        if soup.title:
            print soup.title.string
        links = []
        for item in soup.findAll('a'):
            link=item.get('href')
            if link and link.startswith('http://') and link not in self.finished_url_list:
                links.append(link)
        print links
        return links

    def get_next_url(self):
        pass
    

s = Spider('http://www.sina.com.cn',1)
s.crawl()
print s.all_url_list
print s.finished_url_list
    
def hash(url):
    return hashlib.sha1(url).hexdigest()

def crawl(url):
    data = urllib2.urlopen(url)
    soup = BeautifulSoup(data,fromEncoding="gb18030")
    s = soup.findAll(text=re.compile("地震".decode('utf-8')))
    for res in s:
       print res
    pass

if __name__=="__main__":
    pass

