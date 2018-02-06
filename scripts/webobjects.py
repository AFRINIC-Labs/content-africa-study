#!/usr/bin/env python

from bs4 import BeautifulSoup
import re
from collections import defaultdict
import urllib2
import urllib
import csv
import json

MOBILE_USER_AGENT='Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
DESKTOP_USER_AGENT='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
GEOLOC_URL='https://stat.ripe.net/data/geoloc/data.json?resource='


def main():
	f1 = open("data/domain.csv","r")
	f2 = open("data/webobjects.sql", "a+")
	f3 = open("data/webobjects.csv", "a+")
	
	geolocDict = {}	

	for domain in f1:
	    
	    print "############ " + domain.strip() + " ############" 
	
	    if domain in f3:
		continue
	    else:
		f3.write(domain)
	    
	    object_dict = getWebObjects(domain.strip(), MOBILE_USER_AGENT)
		
	    keys = []
	    
	    try:
		keys =  object_dict.keys()
	    except:
		continue

	    for object_type in keys:

		for i in object_dict[object_type]:

		    try:
		    	object_url = i['src']
		    except:
			continue

		    if "http" not in object_url:
			continue

		    search = re.search('[(http)(https)].\/\/(.*?)\/', object_url)
		    object_domain = ""

		    if search:
			object_domain = search.group(1)

		    object_size = getPageSize(object_url, MOBILE_USER_AGENT)

		    object_loc_cc = geolocDict.get(object_domain)
		    
		    if not object_loc_cc:
		    	object_loc_cc = getGeolocation(object_domain)
			geolocDict[object_domain] = object_loc_cc

		    row = "insert into webobjects values ('%s','%s','%s','%s','%s','%s')\n" % (domain.strip(), object_type, object_url, object_domain, object_size, object_loc_cc)
		    try:	
		    	f2.write(row.encode('utf-8'))
		    except:
			continue

	f1.close()
	f2.close()
	f3.close()
	print "done"



#retrieve the country of location as per ripe/maxmind
def getGeolocation(domain):
    
    url = GEOLOC_URL + domain    
    try:
        res = urllib2.urlopen(url)
    except Exception, e:
        print e
	return "NULL"
    
    data = json.loads(res.read())
    location = {}    

    try:
	location = data['data']['locations'][0]
    except:
	return "NULL"  

    return location['country']
    

    

#page size
def getPageSize(url, myuseragent):
    
    contentLength = None
    res = None
    
    req = urllib2.Request(url)
    
    if myuseragent:
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
    
def getWebObjects(domain, myuseragent):
    
    res = None
    
    req = urllib2.Request("http://" + domain)
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
    
    soup = BeautifulSoup(res, "html.parser")
    images = soup.findAll('img')
    videos = soup.findAll('video')
    audios = soup.findAll('audio')
    scripts = soup.findAll('script')
    styles = soup.findAll('style')
    
    object_dict = {}
    
    object_dict['image'] = soup.findAll('img')
    object_dict['video'] = soup.findAll('video')
    object_dict['audio'] = soup.findAll('audio')
    object_dict['script'] = soup.findAll('script')
    object_dict['style'] = soup.findAll('style')
    
    return object_dict


if __name__ == "__main__":
    main()
