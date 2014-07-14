#! /usr/bin/python2
# Author mycinbrin@gmail.com
import lxml.html.soupparser as soupparser
import cookielib
import urllib2
import urllib
import re
import os
import traceback
import sys
class Leetcode:
  SITE_URL = 'https://oj.leetcode.com/'
  LOGIN_URL = 'https://oj.leetcode.com/accounts/login/'
  PROBLEM_URL = 'https://oj.leetcode.com/problems/'
  TOKEN_XPATH = "//*[@name='csrfmiddlewaretoken']/@value"
  SUBMISSION_XPATH = "//a[contains(@class,'status-accepted')]/@href"
  PROBLEM_XPATH = "//tr[td/span/@class='ac']/td[2]/a/@href"
  SUBMISSION_URL = SITE_URL+'problems/%s/submissions/'
  CPP_REGEX = "scope.code.cpp[^']*'([^']*)'"
  def __init__(self,user_name,password,folder='code'):
    print "loging in..."
    self.user_name = user_name
    self.password = password
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    login_page = self.opener.open(self.LOGIN_URL).read()
    dom = soupparser.fromstring(login_page)
    token = dom.xpath(self.TOKEN_XPATH)[0]
    data ={'login':self.user_name, 'password':self.password,'csrfmiddlewaretoken':token}
    req = urllib2.Request(self.LOGIN_URL)
    self.update_referer(self.LOGIN_URL)
    problem_page = self.opener.open(req,urllib.urlencode(data)).read()
    problem_urls = soupparser.fromstring(problem_page).xpath(self.PROBLEM_XPATH)
    if not problem_urls:
        print "problems cannot be found. Username or password may not be right"
        sys.exit(-1)
    self.problems = map(lambda url:url.split('/')[-2],problem_urls)
    self.folder = folder
    if not os.path.isdir(folder):
      os.mkdir(folder)
  def update_referer(self,last_page):
    self.opener.addheaders = \
      [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'),
      ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13'),
      ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
      ('Accept-Language', 'en-gb,en;q=0.5'),
      ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
      ('Keep-Alive', '115'),
      ('Connection', 'keep-alive'),
      ('Origin','https://oj.leetcode.com'),
      ('Cache-Control', 'max-age=0')] + [('Referer',last_page)]
  def download_one(self,problem_name):
    try:
      print 'downloading',problem_name
      if os.path.isfile(problem_name):
        print 'exist,skip'
        return
      self.update_referer(self.PROBLEM_URL)
      print self.SUBMISSION_URL%problem_name
      submission_page = self.opener.open(self.SUBMISSION_URL%problem_name).read()
      results = soupparser.fromstring(submission_page).xpath(self.SUBMISSION_XPATH)
      if not results:
        print 'accepted submission cannot be found on the first page'
        return
      self.update_referer(self.SUBMISSION_URL%problem_name)
      detail_page = self.opener.open(self.SITE_URL+results[0]).read()
      match_results = re.search(self.CPP_REGEX,detail_page)
      code = match_results.group(1).decode('unicode-escape')
      with open(self.folder+'/'+problem_name+'.cpp','w') as w:
        w.write(code)
    except:
      traceback.print_exc()
  def download_all(self):
    map(self.download_one,self.problems)

if __name__ == '__main__':
  if len(sys.argv) != 3:
      print 'Usage ./leetcode_downloader.py USERNAME PASSWORD'
      sys.exit(0)
  Leetcode(sys.argv[1],sys.argv[2]).download_all()
