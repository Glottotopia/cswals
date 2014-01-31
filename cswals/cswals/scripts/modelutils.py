# -*- coding: utf-8 -*- 
#import sys
import time
import pprint

##SQLALCHEMY
from sqlalchemy import create_engine
from sqlalchemy.sql import func
#from sqlalchemy.sql.expression import desc
#from sqlalchemy.orm import aliased
#from sqlalchemy import or_
#from sqlalchemy import not_

 
#from sqlalchemy.orm  import scoped_session, sessionmaker 
#from operator import itemgetter, attrgetter

#from pylons import config

##PROJECT
from cswals import models
from cswals.models  import DBSession
from cswals.models import Featurevalues, Values, Languages, Features

from cswals.scripts import helpers as h
 

def getLanguages(featurename): 
    result = DBSession.query(Featurevalues.walscode,Featurevalues.featurevalue, Featurevalues.creator, Values.longdescription)\
		    .filter(Featurevalues.featurename == featurename)\
		    .filter(Featurevalues.featurename == Values.featurename)\
		    .filter(Featurevalues.featurevalue == Values.featurevalue)\
		    .distinct()\
		    .order_by(Featurevalues.walscode)\
		    .order_by(Featurevalues.creator)\
		    .all()   
    return result 

def getFeatures(walscode): 
    result = DBSession.query(Featurevalues.featurename,Featurevalues.featurevalue, Featurevalues.creator)\
		    .filter(Featurevalues.walscode == walscode)\
		    .distinct()\
		    .order_by(Featurevalues.featurename)\
		    .order_by(Featurevalues.creator)\
		    .all()   
    return result 
 
def getFeatureString(featurename):
    result = DBSession.query(Features.featurestring)\
			.filter(Features.featurename==featurename)\
			.first()		    
    return result[0]
    
    
def getValues(featurename):
    result = DBSession.query(Values)\
			.filter(Values.featurename==featurename)\
			.all()		
    r = [x.__dict__ for x in result]
    for s in r: 
	colorstring = h.getColorstring(s['featurevalue']) 
	s['colorstring'] = colorstring 
    return r
    
    return [x.__dict__.update({'colorcode':h.getColorstring(x.featurevalue)}) for x in result]
    
def getLanguageInfo(walscode):  
    result = DBSession.query(Languages)\
			.filter(Languages.walscode==walscode)\
			.all()    
    try:
	d = result[0].__dict__
	del d['_sa_instance_state']
	return d  
    except IndexError:
	return None
    
    
def getWalsFeatures():
    """return a dictionary of walsfeatures with an array of accepted values per feature"""
    
    featurenames = [x[0].upper() for x in DBSession.query(Features.featurename).all()]
    d = {}
    for fn in featurenames:
	d[fn] = [str(y[0]) for y in DBSession.query(Values.featurevalue).filter(Values.featurename==fn).all()]
    return d
     
    
def write2db(dictionary, creator, dataset):  
    walsfeatures = getWalsFeatures()
    walscodes = [x[0] for x in DBSession.query(Languages.walscode).all()] 
    insertarr = []
    #print walsfeatures
    for walscode in dictionary:
	#print walscode
	if walscode not in walscodes: 
	    continue
	for featurename in dictionary[walscode]['values']: 
	    #print featurename
	    featurename = featurename.upper()
	    if featurename not in walsfeatures: 
		#print -2
		continue
	    featurevalue = str(dictionary[walscode]['values'][featurename])
	    #print featurevalue
	    if featurevalue not in walsfeatures[featurename]:
		#print -3
		continue
	    insertarr.append(dict(walscode=walscode, 
				    featurename=featurename.upper(), 
				    featurevalue=featurevalue,
				    creator=creator,
				    dataset=dataset,
				    time=time.time())) 
				    
    db = create_engine('sqlite:///%(here)s/../cswals.sqlite')  
    connection = db.connect()
    connection.execute(models.Featurevalues.__table__.insert(), insertarr) 
    connection.close()
 
def getMapData(featurename):
    result = DBSession.query(Languages.name, 
			    Languages.walscode, 
			    Languages.latitude, 
			    Languages.longitude,  
			    Values.description,
			    Featurevalues.featurevalue,
			    Featurevalues.creator,
			    Featurevalues.dataset,
			    #Featurevalues.time
			    )\
			.filter(Featurevalues.featurename==featurename)\
			.filter(Featurevalues.walscode==Languages.walscode)\
			.filter(Values.featurename==Featurevalues.featurename)\
			.filter(Values.featurevalue==Featurevalues.featurevalue)\
			.filter(Languages.walscode==Featurevalues.walscode)\
			.all()  
    r =  [x.__dict__ for x in result] 
    for s in r: 
	imgurl = h.getImgUrl(s['featurevalue'], s['creator']) 
	s['imgurl'] = imgurl 
    return r
    
def getAllLanguages():
    result = DBSession.query(Languages)\
	    .all()
    return [x.__dict__ for x in result ]
    
def getAllFeatures():
    result = DBSession.query(Features)\
	    .all()
    return [x.__dict__ for x in result ]
    

    
def getCreatorStats():
    result = DBSession.query(Featurevalues.creator,func.count(Featurevalues.creator))\
			.group_by(Featurevalues.creator)\
			.all()
    return [{'name':x[0],'count':x[1]} for x in result ] 