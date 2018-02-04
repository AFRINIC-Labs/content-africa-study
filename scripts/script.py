#!/usr/bin/env python

import BeautifulSoup
import re
from collections import defaultdict
import urllib2
import httplib
import csv
import json

MOBILE_USER_AGENT='Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
DESKTOP_USER_AGENT='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
GEOLOC_URL='https://stat.ripe.net/data/geoloc/data.json?resource='


#retrieve the country of location as per ripe/maxmind
def getGeolocation(domain):
    
    url = GEOLOC_URL + domain    
    res = None

    try:
        res = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
    	print 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
    	print 'URLError = ' + str(e.reason)
    except httplib.HTTPException, e:
    	print 'HTTPException'
    except Exception:
    	import traceback
    	print 'generic exception: ' + traceback.format_exc()   
 
    if res:
    	data = json.loads(res.read())
    
    country = ''    

    try:
    	location = data['data']['locations'][0]
	country = location['country']
    except IndexError, e:
	print e 

    return country
    
#page size
def getPageSize(url, myuseragent):
    
    contentLength = None
    res = None
    
    req = urllib2.Request(url)
    req.add_header('User-agent', myuseragent)
    
    try:
        res = urllib2.urlopen(req)
    except Exception, e:
        print e
    #except urllib2.HTTPError, e:
    #    print e.code
    #except urllib2.URLError, e:
    #    print e.args

    
    if not res:
        return -1
    
    contentLength = res.headers.get('content-length')
    
    if contentLength:
        return contentLength
    else:
        return len(res.read())    
    
def getWebObjects(url):
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    images = soup.findAll('img')
    
    for i in images:
        link = i['src']
        m = re.search('.*://(.+?)/.*', link)
        if m:
            print m.group[1]

file = open('../data/domain.csv','rb')
file2 = open('../data/geoloc.sql','w')

for domain in file:
    line = 'update news set geoloc_cc=\''+ getGeolocation(domain) + "\' where domain=\'" + domain.strip() + "\';\n"
    print line
    file2.write(line)
file.close()
file2.close()

