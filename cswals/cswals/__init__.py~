from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('welcome', '/')
    #config.add_route('contact', '/contact')
    config.add_route('upload', '/upload')
    #config.add_route('collection', '/collection')
    #config.add_route('getgoogledoc', '/getgoogledoc')
    config.add_route('getethercalc', '/action/getethercalc')
    #config.add_route('getofficespreadsheet', '/getofficespreadsheet')
    #config.add_route('getwebspreadsheet', '/getwebspreadsheet')
    #config.add_route('feature', '/feature')
    config.add_route('language', '/language/walscode/{walscode}')
    #config.add_route('language', '/language')
    config.add_route('feature', '/feature/ID/{ID}')
    config.add_route('featurevalue', '/featurevalue/ID/{ID}')
    #config.add_route('featurevalue', '/featurevalue')
    #config.add_route('value', '/value')
    config.scan()
    return config.make_wsgi_app()
      
     
