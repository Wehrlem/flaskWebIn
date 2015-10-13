import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kakakak der gejt'
    SSL_DISABLE = False
    ORIENTDB_HOST = 'localhost'
    ORIENTDB_PORT = 2424

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ORIENTDB_SERVER_PASSWORD = os.environ.get('ORIENT_PW') or 'jaja'
    ORIENTDB_SERVER_USERNAME = os.environ.get('ORIENT_UN') or 'jaja'


class ProductionConfig(Config):
    DEBUG = False
    ORIENTDB_SERVER_PASSWORD = os.environ.get('ORIENT_PW') or 'jaja'
    ORIENTDB_SERVER_USERNAME = os.environ.get('ORIENT_UN') or 'jaja'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class TestingConfig(Config):
    Testing = True
    ORIENTDB_SERVER_PASSWORD = os.environ.get('ORIENT_PW') or 'jaja'
    ORIENTDB_SERVER_USERNAME = os.environ.get('ORIENT_UN') or 'jaja'

class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production':ProductionConfig,
    'default': DevelopmentConfig,
    'unix': UnixConfig,
    'db_name' : 'history',
    'db_type' : 'plocal',
}