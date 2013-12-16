# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
#from pylons import url as pylons_url
#from pylons import config
#from random import *
#import hashlib
#import latex
#import re
#import string
#import collections
#import sys
#from operator import itemgetter, attrgetter


stopwords = ['a',
'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your', 'digitized', 'Google', 'byGoogle', 'pro', 'see', 'not', 'are', 'second', 'place', 'different', 'each', 'before', 'those'
, 'does', 'after', 'what', 'three', 'occur', 'see', 'example', 'number', 'found', 'many', 'him', 'here', 'about', 'any', 'very', 'most', 'use', 'like', 'man', 'people', 'both', 'time', 'out', 'then', 'following', 'where', 'had', 'same', 'would', 'into', 'its', 'first', 'than', 'such', 'person', 'them', 'who', 'see', 'when', 'between', 'more', 'his', 'form', 'been', 'you', 'were', 'will', 'some', 'language', 'these', 'used', 'only', 'all', 'may', 'can', 'there', 'languages', 'their', 'two', 'other', 'also', 'but', 'has', 'was', 'they', 'one', 'have', 'this', 'from', 'which', 'not', 'for', 'with', 'are', 'that', 'and', 'the']
linguiststopwords = ['one', 'two', 'three', 'found', 'such', 'attested', 'though', 'seems', 'whether', 'those', 'same', 'both', 'see', 'perhaps', 'language', 'languages', 'more', 'less', 'under']
stopwords += linguiststopwords
STOPDIC = dict(zip(stopwords,[True for i in range(len(stopwords))]))
    
def url(*args, **kwargs):
    """
    wrap pylons url object to make sure it returns full absolute URLs which
    we want in particular for our LinkedData. 
    """ 
    _url = pylons_url(*args, **kwargs)
    if not _url.startswith('http'):
        _host = config['host']
        _port = config['port']
        #_prefix = config['myprefix']
        _prefix = ''
	#if _prefix == '':
	    #prefix = '/'
	#if _url.startswith('%s/' % _prefix): #evil hack to undo stupid pylons_url behaviour
	    #_prefix = '' 
        #_url = "http://%s:%s%s%s" % (_host, _port, _prefix, _url) 
	if str(_port) == '80':
	    _url = "http://%s%s" % (_host, _url) 
	else:
	    _url = "http://%s:%s%s" % (_host, _port, _url) 
    return _url

def getColorstring(value):   
    orientation = value/8
    color = int(bin(value%8)[2:])
    colorstring = "%s-%03d" % (orientation, color)
    return colorstring
    
def getImgUrl(value,creator):
    colorstring = getColorstring(value) 
    provenance = 'w'
    if creator != 'WALS':
	provenance = 'p'
    return "%s%s.png" % (provenance, colorstring)
	
def getSeparator(s):
    """find the separating character of a csv spreadsheet """
    chars = collections.Counter(s).most_common()
    unwanted = string.ascii_uppercase + string.ascii_lowercase + string.digits
    for char in chars: 
	if char[0] not in unwanted:
	    return char[0]
    return None

def flattenValues(d):
    """get a triple of walscode, feature, value where Value is not none""" 
    a = []
    for walscode in d:
	for featurenumber in d[walscode]['values']: 
	    featurevalue = d[walscode]['values'][featurenumber]
	    a.append((walscode, featurenumber,featurevalue)) 
    return a