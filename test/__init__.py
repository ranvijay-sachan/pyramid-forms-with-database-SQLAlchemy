from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession, Base

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='test.models.Root')
    config.include('pyramid_chameleon')
    config.add_route('my_view', '/')
    config.add_route('mypage_add', '/add')
    config.add_route('mypage_view', '/records')
    config.add_route('delete_record', '/{id}/delete')
    config.add_route('delete_record_ajax', 'id')
    config.add_static_view('deform_static', 'deform:static/')
    config.scan('.views')
    return config.make_wsgi_app()