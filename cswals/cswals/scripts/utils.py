## -*- coding: utf-8 -*-
#"""Application controller"""
#import logging
#log = logging.getLogger('glottolog')

#import os
#import re
#import tempfile

##PYLONS
#from pylons import tmpl_context as c
#from pylons import config, request
#from pylons.controllers.util import abort, redirect

##PYTHON
#from operator import itemgetter, attrgetter

##SQLALCHEMY
#from sqlalchemy.sql import *
##from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.orm import relation, mapper, aliased

##PROJECT
#from cswals.lib.base import BaseController, respond
#from cswals.lib.modelutils import getLanguages, getFeatures, getFeatureString, getValues, getLanguageInfo, getMapData,\
				    #getAllLanguages, getAllFeatures, getCreatorStats
#from cswals.lib import walsmatrix

#from cswals import model
#from cswals.model.meta import DBSession1

##maker1 = None

##from cswals.model import Refbase 
#from cswals.lib.app_globals import Globals as g
#from cswals.lib import helpers as h

#import time
#import string

#
# the application:
#
#class ApplicationController(BaseController):

    #def welcome(self):
	#"""
	#show the welcome page
	#""" 
	#c.home = {'class': 'activetablvl1'}    
	#c.welcome = {'class': 'activetablvl2'}    
        #return respond(None, dict(xhtml='fragments/welcomePane.xhtml'))
                
    #def upload(self):
	#"""
	#show the upload page
	#"""   
        #return respond(None, dict(xhtml='fragments/upload.xhtml'))
        
    
    #def showlanguage(self, id_):
	#walscode = id_
	#c.walscode = walscode
	#c.features = getFeatures(walscode)
	#c.languageinfo = getLanguageInfo(walscode)
        #return respond(None, dict(xhtml='fragments/language.xhtml')) 
    
    #def showfeature(self, id_): 		    
	#featurename = id_
	#c.featurename = featurename
	#c.featurestring = getFeatureString(featurename)
	#c.values = getValues(featurename)	
	#c.languages = getLanguages(featurename)
	#c.mapdata = getMapData(featurename)  
	#c.datasets = list(set([x['dataset'] for x in c.mapdata if x['dataset']!=None])) 
        #return respond(None, dict(xhtml='fragments/feature.xhtml')) 
    
    #def showvalue(self):
	#pass    

    #def getGoogleDoc(self):
	#key = request.params.get('key')
	#wm = walsmatrix.WalsMatrix()
	#wm.fromGoogleDoc(key) 
	#c.uploadedvalues = h.flattenValues(wm.dictionary)
	#c.rdffile = wm.rdffile
        #return respond(None, dict(xhtml='fragments/uploadstatus.xhtml')) 
	
    #def getEthercalc(self):
	#key = request.params.get('key')
	#creator = request.params.get('creator', 'Anonymous')
	#wm = walsmatrix.WalsMatrix()
	#wm.fromEthercalc(key,creator) 
	#c.uploadedvalues = h.flattenValues(wm.dictionary)
	#c.rdffile = wm.rdffile
        #return respond(None, dict(xhtml='fragments/uploadstatus.xhtml')) 
     
    
    #def getOfficeSpreadsheet(self):
	#creator = request.POST['creator']   
	#spreadsheet = request.POST['spreadsheet'] 
	#filename =  repr(spreadsheet).split(", u'")[-1][:-2] #evil hack to get filename
	#f = spreadsheet.file
	#txt = f.read()
	#tmpfile = tempfile.NamedTemporaryFile() 
	#tmpfile.write(txt)
	#tmpfile.flush() 
	#wm = walsmatrix.WalsMatrix()	
	#if filename.lower().endswith('.xls'):
	    #wm.fromXLS(tmpfile.name, creator, originalfilename=filename.lower().split('/')[-1][:-4])
	#if filename.lower().endswith('csv'):
	    #wm.fromCSV(tmpfile.name, creator, originalfilename=filename.lower().split('/')[-1][:-4])
	#tmpfile.close()
	#c.uploadedvalues = h.flattenValues(wm.dictionary)
	#c.rdffile = wm.rdffile
        #return respond(None, dict(xhtml='fragments/uploadstatus.xhtml')) 
	
    #def collection(self):
	#c.languages = getAllLanguages()
	#c.features = getAllFeatures()
	#c.creators = getCreatorStats()
        #return respond(None, dict(xhtml='fragments/collection.xhtml')) 
	
    #def getWebSpreadsheet(self):    
	#pass