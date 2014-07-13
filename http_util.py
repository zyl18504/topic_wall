#coding=utf8

import urllib2,random
from constants import *
from tornado.escape import url_escape

request_headers = {
    HTTP_USER_AGENT:'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    HTTP_REFER:'http://huati.weibo.com',
    X_REQUEST_WITH:'XMLHttpRequest'
}

def get_topic_response(topic):
    proxy_url = random.choice(PROXY_URL_LIST)
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy_url}),urllib2.HTTPHandler(debuglevel=0))
    urllib2.install_opener(opener)
    topic_info_url = "".join((TOPIC_URL,url_escape(topic)))
    req = urllib2.Request(topic_info_url,None,request_headers)
    try:
        resp = urllib2.urlopen(req)
        return resp.read()
    except urllib2.URLError,e:
        print " request error @:%s" % proxy_url