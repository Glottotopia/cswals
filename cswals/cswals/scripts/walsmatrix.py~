import os
import sys

import socket
import logging
import atom.service
import gdata.service
import gdata.spreadsheet
import gdata.spreadsheet.service
import gdata.spreadsheet.text_db


import zipfile
import xlrd
import urllib2
import time

from cswals.scripts.modelutils import write2db
from cswals.scripts import helpers as h

from modelutils import getWalsFeatures

class WalsMatrix:
    """ a matrix which holds feature value for WALS"""

    template = """
## Turtle Content Start ##

## Prefix Declaration Section -- you don't need to touch this

@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . 
@prefix datapoint: <http://wals.info/datapoint/> .
@prefix value: <http://wals.info/value/> .
@prefix lingtyp: <http://www.glottotopia.de/ontologies/lingtyp.owl#> .
@prefix dcterms: <http://purl.org/dc/elements/1.1/> .  
@prefix glottologref: <http://www.glottolog.org/ontologies/glottolog.owl#> .
@prefix:<#>.

<> a lingtyp:Datapoint .


### start here
 
<> rdfs:label "WALS datapoint %(featurenumber)s-%(walscode)s" .
<> lingtyp:hasValue value:f%(featurenumber)s-%(featurevalue)s .
<> dcterms:creator "%(creator)s" .
<> dcterms:isPartOf "%(dataset)s" .
"""

    collectiontemplate = """
## Turtle Content Start ##

## Prefix Declaration Section -- you don't need to touch this
 
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .   
@prefix dcterms: <http://purl.org/dc/elements/1.1/> . 
## you have to change  12345678 in the line below to reflect your dropbox user id
@prefix mycswals: <http://linkeddata.uriburner.com/about/html/https/dl.dropbox.com/u/12345678/<http://purl.org/dc/elements/1.1/> .
@prefix:<#>.

<> a rdf:Description .
 
### start here
  
<> dcterms:label "%s" . 
<> dcterms:creator "%s" . 
"""

    
    def __init__(self, creator, collection, dictionary):
	self.creator = creator
	self.collection = collection
	self.dictionary = dictionary
	
    def __init__(self):
	self.creator = ''
	self.collection = '' 
	self.dictionary = {}
	pass
    
    def processFields(self, fields):	
	walscodeindex = None
	glottologrefindex = None
	isbnindex = None
	for i, cell in enumerate(fields[0]):
	    if cell.strip() == 'walscode':
		walscodeindex = i
		continue
	    if cell.strip() == 'glottologref':
		glottologrefindex = i
		continue
	    if cell.strip() == 'isbn':		
		isbnindex = i
		continue
	if walscodeindex == None:
	    return 
	for l in fields[1:]:
	    walscode = l[walscodeindex] 
	    glottologref = False
	    isbnref = False
	    self.dictionary[walscode] = {}
	    if glottologrefindex:
		glottologrefcode = l[glottologrefindex].strip().lower()
		if glottologrefcode.startswith('r'):
		    glottologrefcode = glottologrefcode[1:]
		try:
		    int(glottologrefcode)
		    glottologref = "glottolog:r%s" % glottologrefcode
		except:
		    pass 
	    self.dictionary[walscode]['glottologref'] =  glottologref
	    if isbnindex:
		isbnrefcode = l[isbnindex]
		if isbnrefcode != '':
		    isbnref = "<urn:isbn:%s>" % isbnrefcode
	    self.dictionary[walscode]['isbnref'] = isbnref
	     
	    self.dictionary[walscode]['values'] = {}
	    walsfeatures =  getWalsFeatures() 
	    for i,value in enumerate(l):
		if i == 0:
		    continue
		if value:
		    try:
			value = str(int(value))
		    except ValueError:
			continue
		    featurenumber = fields[0][i].strip().upper()
		    if featurenumber.startswith('F'):
			featurenumber = featurenumber[1:]   
		    if featurenumber not in walsfeatures:  
			continue 
		    if value not in walsfeatures[featurenumber]: 
			continue
		    try:
			self.dictionary[walscode]['values'][featurenumber] = int(value)
		    except TypeError:
			pass
		    except ValueError:
			pass 
    
	
    def fromEthercalc(self,key,creator):
	self.creator = creator
	self.dataset = key
	lines = urllib2.urlopen('https://ethercalc.org/%s.csv'%key).readlines()
	fields  =  [l.split(',') for l in lines]
	self.processFields(fields) 
	write2db(self.dictionary,self.creator,self.dataset)
	self.dumpRDF()
		    
    def fromGoogleDoc(self,gdockey):  #0Apb_EoY8u4imdDFXMDJDdUNGLXZCNVp4aEtpZnpnYlE 
	#self.__init__() 
	gd_client = gdata.spreadsheet.service.SpreadsheetsService()
	gd_client.email = 'glottotopia@gmail.com'
	gd_client.password = open('gpw').read()
	gd_client.source = 'getwals'                                     

	try:                    
	    # log in
	    gd_client.ProgrammaticLogin()
	except socket.sslerror, e:
	    logging.error('Spreadsheet socket.sslerror: ' + str(e))
	    return False
	    
	key = gdockey
	wksht_id = '1'
	 
	
	q = gdata.spreadsheet.service.ListQuery() 
	try: 
	    # fetch the spreadsheet data 
	    fd = gd_client.GetWorksheetsFeed(key=gdockey)
	    self.dataset =  fd.title.text 
	    feed = gd_client.GetListFeed(key, wksht_id, query=q)	    
	    authors =  feed.author 
	    self.creator = '; '.join([author.name.text for author in authors])
	except gdata.service.RequestError, e:
	    logging.error('Spreadsheet gdata.service.RequestError: ' + str(e))
	    return False
	except socket.sslerror, e:
	    logging.error('Spreadsheet socket.sslerror: ' + str(e))
	    return False
	
	for row_entry in feed.entry: 
	    dico = gdata.spreadsheet.text_db.Record(row_entry=row_entry).content 
	    d = {} 
	    walscode = dico['wals'] 
	    self.dictionary[walscode] = {}
	    self.dictionary[walscode]['glottologref'] = False
	    self.dictionary[walscode]['isbnref'] = False 
	    self.dictionary[walscode]['values'] = {}
	    for k in dico:
		try:		
		    featurenumber = k.upper()
		    if featurenumber.startswith('F'):
			featurenumber = featurenumber[1:] 
		    if featurenumber.upper() not in getWalsFeatures():
			continue		    
		    featurevalue = int(dico[k]) 
		except ValueError:
		    continue
		except TypeError:
		    continue 
		self.dictionary[walscode]['values'][featurenumber] = featurevalue
	write2db(self.dictionary,self.creator,self.dataset)
	self.dumpRDF()
	 
	
    def fromXLS(self, xlsfile, creator, originalfilename = False): 
	self.creator = creator	
	self.dataset = xlsfile.split('/')[-1]
	if originalfilename:
	    self.dataset = originalfilename
	book = xlrd.open_workbook(xlsfile) 
	sheet = book.sheet_by_index(0) 
	fields = [[sheet.cell(row_index,col_index).value for col_index in range(0,sheet.ncols) ] for row_index in range(sheet.nrows) ]	
	self.processFields(fields) 
	write2db(self.dictionary,self.creator,self.dataset)
	self.dumpRDF()
	
    def fromCSV(self, filename, creator, originalfilename = False):   
	self.creator = creator
	self.dataset = filename.split('/')[-1]
	if originalfilename:
	    self.dataset = originalfilename
	lines = open(filename).readlines()
	separator = h.getSeparator(lines[0])
	fields =  [l.split(separator) for l in lines] 
	self.processFields(fields) 
	write2db(self.dictionary,self.creator,self.dataset)
	self.dumpRDF()
		    
    def dumpRDF(self):
	fn = '%s.zip' % time.strftime("cswals%Y%b%d_%Hh%M_%S", time.gmtime())
	zipfilename = './cswals/public/datasets/%s' % fn
	a = []
	zf = zipfile.ZipFile(zipfilename, mode='w')
	for walscode in self.dictionary:
	    for featurenumber in self.dictionary[walscode]['values']:
		featurevalue = self.dictionary[walscode]['values'][featurenumber]
		d = dict(walscode=walscode, featurenumber=featurenumber, featurevalue=featurevalue, creator=self.creator, dataset=self.dataset)
		filename = "/tmp/wals-%(walscode)s-%(featurenumber)s.ttl" %d
		a.append((walscode,featurenumber))
		out = open(filename,'w')
		out.write(self.template % d ) 
		if self.dictionary[walscode]['glottologref']: 
		    out.write("""<> dcterms:references  %s .\n""" % self.dictionary[walscode]['glottologref']) 
		if self.dictionary[walscode]['isbnref']: 
		    out.write("""<> dcterms:references %s .\n""" % self.dictionary[walscode]['isbnref'])	 
		out.close() 
		zf.write(filename) 
		os.remove(filename)
	collectionfilename = "/tmp/%s.ttl" % self.dataset
	collectionfile =  open(collectionfilename, 'w')
	collectionfile.write("<> a  rdf:Description\n")
	collectionfile.write(self.collectiontemplate % (self.dataset,self.creator))
	for walscode, featurenumber in a:
	    collectionfile.write("<> dcterms:hasPart mycswals:wals-%s-%s\n" % (walscode, featurenumber)) 
	collectionfile.close()
	zf.write(collectionfilename) 
	os.remove(collectionfilename)
	zf.close()   
	self.rdffile = fn 