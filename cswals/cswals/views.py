from pyramid.response import Response
from pyramid.view import view_config 
from pyramid.renderers import get_renderer 
from pyramid.httpexceptions import HTTPNotFound

import pprint

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )
     
    
from .scripts.modelutils import getFeatures, getLanguageInfo, getFeatureString, getLanguages, getMapData, getValues, getAllLanguages, getAllFeatures, getCreatorStats
from scripts import walsmatrix
from scripts import helpers as h



 

@view_config(route_name='welcome', renderer='templates/welcome.pt') 
def welcome(request): 
    main = get_renderer('templates/master.pt').implementation() 
    return {'project': 'cswals','main':main}

@view_config(route_name='upload', renderer='templates/upload.pt') 
def upload(request): 
    main = get_renderer('templates/master.pt').implementation()     
    return {'project': 'cswals','main':main}
    
    
@view_config(route_name='collection', renderer='templates/collection.pt') 
def collection(self):
    main = get_renderer('templates/master.pt').implementation() 
    languages = getAllLanguages()
    features = getAllFeatures()
    creators = getCreatorStats() 
    return {'project': 'cswals','main':main,
	'languages':languages,
	'features':features,
	'creators':creators
    }

    
@view_config(route_name='language', renderer='templates/language.pt') 
def showlanguage(request):   
    main = get_renderer('templates/master.pt').implementation() 
    walscode = request.matchdict.get('walscode','' )   
    features = getFeatures(walscode)
    languageinfo = getLanguageInfo(walscode)
    if languageinfo == None:
	raise HTTPNotFound()  
    return {'main':main,
	'project': 'cswals',
	'walscode':walscode,
	'features':features,
	'languageinfo':languageinfo
    }

@view_config(route_name='feature', renderer='templates/feature.pt') 
def showfeature(request): 		    
    main = get_renderer('templates/master.pt').implementation() 
    ID = request.matchdict.get('ID','' ) 
    mapdata = getMapData(ID) 
    datasets = list(set([x['dataset'] for x in mapdata if x['dataset']!=None])) 
    return {'main':main,
	'project': 'cswals',
	'featurename':ID,
	'featurestring':getFeatureString(ID),
	'values':getValues(ID),
	'languages':getLanguages(ID),
	'mapdata': mapdata,
	'datasets': datasets
    } 

#def showvalue(self):
    #pass    

@view_config(route_name='getgoogledoc', renderer='templates/uploadstatus.pt') 
def getGoogleDoc(request):
    main = get_renderer('templates/master.pt').implementation() 
    key = request.params.get('key') 
    wm = walsmatrix.WalsMatrix()
    wm.fromGoogleDoc(key) 
    uploadedvalues = h.flattenValues(wm.dictionary)
    rdffile = wm.rdffile 
    return {'project': 'cswals','main':main,
	'uploadedvalues':uploadedvalues,
	'rdffile':rdffile 
    }  
    
@view_config(route_name='getethercalc', renderer='templates/uploadstatus.pt') 
def getEthercalc(request):
    main = get_renderer('templates/master.pt').implementation() 
    key = request.params.get('key') 
    creator = request.params.get('creator', 'Anonymous')
    wm = walsmatrix.WalsMatrix()
    wm.fromEthercalc(key,creator) 
    uploadedvalues = h.flattenValues(wm.dictionary)
    rdffile = wm.rdffile
    return {'project': 'cswals','main':main,
	'uploadedvalues':uploadedvalues,
	'rdffile':rdffile 
    }  
    

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
    
    
#def getWebSpreadsheet(self):    
    #pass

    
