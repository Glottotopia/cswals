from pyramid.response import Response
from pyramid.view import view_config
import pprint

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )
     
    
from .scripts.modelutils import getFeatures, getLanguageInfo, getFeatureString, getLanguages, getMapData, getValues
from scripts import walsmatrix
from scripts import helpers as h



 

@view_config(route_name='welcome', renderer='templates/welcome.pt') 
def welcome(request): 
    return {'project': 'cswals'}

@view_config(route_name='upload', renderer='templates/upload.pt') 
def upload(request): 
    return {'project': 'cswals'}
    
@view_config(route_name='language', renderer='templates/language.pt') 
def showlanguage(request):  
    walscode = request.matchdict.get('walscode','' )  
    features = getFeatures(walscode)
    languageinfo = getLanguageInfo(walscode)
    return {'project': 'cswals',
	'walscode':walscode,
	'features':features,
	'languageinfo':languageinfo
    }

@view_config(route_name='feature', renderer='templates/feature.pt') 
def showfeature(request): 		    
    ID = request.matchdict.get('ID','' )
    #c.featurename = featurename
    #c.featurestring = getFeatureString(featurename)
    #c.values = getValues(featurename)	
    #c.languages = getLanguages(featurename)
    #c.mapdata = getMapData(featurename)  
    #c.datasets = list(set([x['dataset'] for x in c.mapdata if x['dataset']!=None])) 
    mapdata = getMapData(ID) 
    datasets = list(set([x['dataset'] for x in mapdata if x['dataset']!=None])) 
    pprint.pprint(mapdata)
    return {'project': 'cswals',
	'featurename':ID,
	'featurestring':getFeatureString(ID),
	'values':getValues(ID),
	'languages':getLanguages(ID),
	'mapdata': mapdata,
	'datasets': datasets
    } 

#def showvalue(self):
    #pass    

#def getGoogleDoc(self):
    #key = request.params.get('key')
    #wm = walsmatrix.WalsMatrix()
    #wm.fromGoogleDoc(key) 
    #c.uploadedvalues = h.flattenValues(wm.dictionary)
    #c.rdffile = wm.rdffile
    #return respond(None, dict(xhtml='fragments/uploadstatus.xhtml')) 
    
@view_config(route_name='getethercalc', renderer='templates/uploadstatus.pt') 
def getEthercalc(request):
    key = request.params.get('key')
    creator = request.params.get('creator', 'Anonymous')
    wm = walsmatrix.WalsMatrix()
    wm.fromEthercalc(key,creator) 
    uploadedvalues = h.flattenValues(wm.dictionary)
    rdffile = wm.rdffile
    return {'project': 'cswals',
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
    
#def collection(self):
    #c.languages = getAllLanguages()
    #c.features = getAllFeatures()
    #c.creators = getCreatorStats()
    #return respond(None, dict(xhtml='fragments/collection.xhtml')) 
    
#def getWebSpreadsheet(self):    
    #pass

    
