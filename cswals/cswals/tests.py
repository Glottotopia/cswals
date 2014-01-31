# -*- encoding: utf-8 -*- 

import unittest
import transaction

import urllib2

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from .models import DBSession
 
        
class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///cswals.sqlite')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        #with transaction.manager:
            #model = MyModel(name='one', value=55)
            #DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    #def test_passing_view(self):
        #from .views import welcome
        #request = testing.DummyRequest()
        #info = welcome(request) 
        #self.assertEqual(info['project'], 'cswals')
        
 
    def testLanguage(self):
        from .views import showlanguage
	codes = ('aba','ibi','deu','cat')
        for code in codes:  
	    request = testing.DummyRequest()
	    request.matchdict['walscode'] = code 
	    info = showlanguage(request)  
	    self.assertGreaterEqual(len(info['features']), 1) 
	noncodes = ('qqq','ab','cdef','gh1','JKL','lMn', u'äüö')
	for noncode in noncodes: 
	    request = testing.DummyRequest()
	    request.matchdict['walscode'] = noncode  
	    self.assertRaises(HTTPNotFound, showlanguage , request) 
	    
    
    
    #def WalsISOCodes(self):
	#codes = ('abc','def','ghi','jkl','lmn')
	#for code in codes:
	    #iso = getISO(code)
	    #wals = getWALS(iso)
	    #assert_true(code==wals)
	    
    #def IsoCodes(self):
	#pass
    
    def testFeature(self):
        from .views import showfeature
	for i in range(1,144): 
	    request = testing.DummyRequest()
	    request.matchdict['ID'] = '%sA'%i 
	    info = showfeature(request)  
	    self.assertGreaterEqual(len(info['languages']), 5) 
    
    #def testFeatureValue(self):
	#for i in range(189):
	    #for j in range(2):
		#urllib2.urlopen('http://localhost:6543/feature/ID/%s/value/%sA'%(i,j))
    
    #def testGoogleDocs(self):
	#gkey = ''
	#gurl = '%s' % gkey
	#content = urllib2.open(gkey).read()
	#for i in range(1,199):
	    #re.match('[0-9]{,3}[ABCD]',content[0][i].strip())
	#for i in range(1,199):
	    #re.match('[a-z]{3}',content[i][0].strip())
	#for i in range(1,99):
	    #for j in range(1,99):
		#int(content[i][j])
	#wm = walsmatrix(content)
	    
    
    #def testEthercalc(self):
	#gkey = ''
	#gurl = '%s' % gkey
	#content = urllib2.urlopen(gkey).read()
	#for i in range(1,199):
	    #re.match('[0-9]{,3}[ABCD]',content[0][i].strip())
	#for i in range(1,199):
	    #re.match('[a-z]{3}',content[i][0].strip())
	#for i in range(1,99):
	    #for j in range(1,99):
		#int(content[i][j])
	#wm = walsmatrix(content)
    
    #def testRDFlanguage(self):
	#urllib2.urlopen('http://localhost:6543/language/walscode/uru.rdf')
	#urllib2.urlopen('http://localhost:6543/language/walscode/iri&format=rdf')
	##sys.exec('curl -accept-headers:RDF http://localhost:6543/language/walscode/oro' )
    
    #def testRDFfeature(self):
	#urllib2.urlopen('http://localhost:6543/feature/ID/23A.rdf')
	#urllib2.urlopen('http://localhost:6543/feature/ID/23A&format=rdf')
	##sys.exec('curl -accept-headers:RDF http://localhost:6543/feature/ID/23A' )
    
    
    #def testRDFfeaturevalue:
	#urllib2.urlopen('http://localhost:6543/featurevalue/ID/23A.rdf')
	#urllib2.urlopen('http://localhost:6543/featurevalue/ID/23A&format=rdf')
	#sys.exec('curl -accept-headers:RDF http://localhost:6543/feature/ID/23A' )
    
    #def testHTML(self):
	#pass
    
    #def testConneg(self):
	#pass
    ##303
    
    #def testGoogleMap(self):
	#pass
    
    #def testAddValues(self):
	#pass
    
    #def testSupersedeValues(self):
	#pass
    
 


#class TestMyViewFailureCondition(unittest.TestCase):
    #def setUp(self):
        #self.config = testing.setUp()
        #from sqlalchemy import create_engine
        #engine = create_engine('sqlite://')
        #from .models import (
            #Base,
            #MyModel,
            #)
        #DBSession.configure(bind=engine)

    #def tearDown(self):
        #DBSession.remove()
        #testing.tearDown()

    #def test_failing_view(self):
        #from .views import welcome
        #request = testing.DummyRequest()
        #info = welcome(request)
        #self.assertEqual(info.status_int, 500)