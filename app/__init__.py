from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.pagedown import PageDown
from config import config
from flask.ext.orientdb import OrientDB
from flask_material import Material
from flask.ext.elasticsearch import FlaskElasticsearch

from flask.ext.cache import Cache
import sys
import os

#set default to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

#load the objects
material = Material()
cache = Cache()
pagedown = PageDown()
client = OrientDB()
es = FlaskElasticsearch()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    client.init_app(app,server_un='jaja', server_pw='jaja')
    config[config_name].init_app(app)
    material.init_app(app)
    pagedown.init_app(app)
    es.init_app(app)
    client.set_db(config['db_name'])
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    #with app.app_context():
    #    cache.clear()
    from .surface import surface as surface_blueprint
    app.register_blueprint(surface_blueprint)
    from .experts import experts as experts_blueprint
    app.register_blueprint(experts_blueprint)
    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)
    from .functions import functions as functions_blueprint
    app.register_blueprint(functions_blueprint)
    from .graph import graph as graph_blueprint
    app.register_blueprint(graph_blueprint)
    from .granules import granules as granules_blueprint
    app.register_blueprint(granules_blueprint)
    from .orientdb import orient as orient_blueprint
    app.register_blueprint(orient_blueprint)
    return app

if __name__ == "__main__":
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(debug=True)