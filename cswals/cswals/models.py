from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

  
class Featurevalues(Base):
    """
    a fully specified set of everything relating to a feature value
    """
    
    __tablename__  = 'featurevalues'

    ID = Column(Integer, primary_key=True)
    walscode = Column(Text, index=True)
    featurename = Column(Text, index=True)
    featurevalue = Column(Text, index=True)
    creator = Column(Text, index=True) 
    dataset = Column(Text, index=True) 
    #time = Column(Float) 
    
class Features(Base):
    """
    Basic information about a feature
    """
    
    __tablename__  = 'features'
 
    featurename = Column(Text, primary_key=True)
    featurestring = Column(Text, index=True)
    
    
 
class Languages(Base):
    """
    Basic information about a language
    """
    
    __tablename__  = 'languages' 
    
    walscode = Column(Text, primary_key=True)
    name = Column(Text, index=True)
    latitude = Column(Text, index=True)
    longitude = Column(Text, index=True)
    genus = Column(Text, index=True)
    family = Column(Text, index=True)
    subfamily = Column(Text, index=True)
    isocodes = Column(Text, index=True)
    
class Values(Base):
    """
    Basic information about a language
    """
    
    __tablename__  = 'values' 
    
    featurename = Column(Text, primary_key=True)
    featurevalue = Column(Integer(), primary_key=True)
    description = Column(Text)
    longdescription = Column(Text) 
        
    
    
##class Geolocations(Base):
    ##"""
    ##Basic information about a languoid
    ##"""
    
    ##__tablename__  = 'geolocations'

    ##ID = Column(Integer(), primary_key=True)
    ##walscode = Column(Text, index=True) 
    ##longitude = Column(Float()) 
    ##latitude = Column(Float())  
